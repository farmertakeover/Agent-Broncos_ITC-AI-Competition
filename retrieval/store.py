"""FAISS-backed corpus retrieval with optional cross-encoder reranking."""
from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass
from typing import Any

import faiss
import numpy as np

from retrieval import config

_store_lock = threading.Lock()
_store: CorpusIndex | None = None


@dataclass
class Hit:
    chunk_id: str
    score: float
    source_path: str
    source_url: str | None
    heading: str
    text: str
    start_line: int


def _truncate(text: str, max_chars: int) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


class CorpusIndex:
    def __init__(self) -> None:
        self._index: faiss.Index | None = None
        self._rows: list[dict[str, Any]] = []
        self._url_by_relpath: dict[str, str] = {}
        self._embedder = None
        self._reranker = None
        self._loaded = False
        self._load_lock = threading.Lock()

    def ensure_loaded(self) -> None:
        if self._loaded:
            return
        with self._load_lock:
            if self._loaded:
                return
            if not os.path.isfile(config.FAISS_PATH) or not os.path.isfile(config.META_PATH):
                raise FileNotFoundError(
                    f"Index not found. Run: python scripts/build_index.py "
                    f"(expected {config.FAISS_PATH})"
                )
            self._index = faiss.read_index(config.FAISS_PATH)
            self._rows = []
            with open(config.META_PATH, encoding="utf-8") as f:
                for line in f:
                    self._rows.append(json.loads(line))
            if os.path.isfile(config.URL_MAP_PATH):
                with open(config.URL_MAP_PATH, encoding="utf-8") as f:
                    self._url_by_relpath = json.load(f)
            self._verify_embedding_model_matches_index()
            self._loaded = True

    def _verify_embedding_model_matches_index(self) -> None:
        """Fail fast if the embedder cannot load or vector dim ≠ FAISS index (bad RAG silently)."""
        assert self._index is not None
        d_index = int(self._index.d)
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(config.EMBEDDING_MODEL)
        except Exception as e:
            raise RuntimeError(
                f"Embedding model unavailable: could not load {config.EMBEDDING_MODEL!r}. "
                "Install dependencies (see README), set HF_TOKEN if the hub is private, "
                f"or fix CPP_EMBEDDING_MODEL. Underlying error: {e}"
            ) from e
        try:
            probe = model.encode(
                ["__retrieval_probe__"],
                convert_to_numpy=True,
                normalize_embeddings=True,
            ).astype("float32")
        except Exception as e:
            raise RuntimeError(
                f"Embedding model failed to encode a probe vector ({config.EMBEDDING_MODEL!r}). {e}"
            ) from e
        d_model = int(probe.shape[1])
        if d_model != d_index:
            raise RuntimeError(
                f"Embedding/index mismatch: FAISS index dimension is {d_index} but "
                f"{config.EMBEDDING_MODEL!r} produces dimension {d_model}. "
                "Retrieval would be wrong. Fix: set CPP_EMBEDDING_MODEL to the same model used when "
                "the index was built, then run `python scripts/build_index.py` (or rebuild after changing the model)."
            )
        self._embedder = model

    def _get_embedder(self):
        if self._embedder is None:
            from sentence_transformers import SentenceTransformer

            self._embedder = SentenceTransformer(config.EMBEDDING_MODEL)
        return self._embedder

    def _get_reranker(self):
        if not config.USE_RERANKER:
            return None
        if self._reranker is None:
            from sentence_transformers import CrossEncoder

            self._reranker = CrossEncoder(config.RERANKER_MODEL)
        return self._reranker

    def embed_query(self, query: str) -> np.ndarray:
        model = self._get_embedder()
        v = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        return v.astype("float32")

    def search(
        self,
        query: str,
        top_k: int | None = None,
        prefetch_k: int | None = None,
        max_chunk_chars: int | None = None,
    ) -> list[Hit]:
        self.ensure_loaded()
        assert self._index is not None
        k = min(top_k or config.DEFAULT_TOP_K, config.MAX_TOP_K)
        pre = min(prefetch_k or config.FAISS_PREFETCH_K, self._index.ntotal)
        pre = max(pre, k)

        q = self.embed_query(query)
        scores, idxs = self._index.search(q, pre)
        idxs = idxs[0].tolist()
        scores = scores[0].tolist()
        candidates: list[Hit] = []
        for i, sc in zip(idxs, scores):
            if i < 0:
                continue
            row = self._rows[i]
            rel = row["source_relpath"]
            url = self._url_by_relpath.get(rel)
            candidates.append(
                Hit(
                    chunk_id=row["chunk_id"],
                    score=float(sc),
                    source_path=rel,
                    source_url=url,
                    heading=row.get("heading") or "",
                    text=row["text"],
                    start_line=int(row.get("start_line", 0)),
                )
            )

        reranker = self._get_reranker()
        if reranker and len(candidates) > k:
            pairs = [[query, h.text[:2000]] for h in candidates]
            ce_scores = reranker.predict(pairs)
            order = np.argsort(-np.array(ce_scores))
            candidates = [candidates[int(j)] for j in order[:k]]
            for rank, j in enumerate(order[:k]):
                candidates[rank].score = float(ce_scores[int(j)])
        else:
            candidates = candidates[:k]

        mchars = max_chunk_chars or config.MAX_CHUNK_CHARS
        for h in candidates:
            h.text = _truncate(h.text, mchars)
        return candidates

    def get_chunk_by_id(self, chunk_id: str) -> Hit | None:
        self.ensure_loaded()
        for row in self._rows:
            if row["chunk_id"] == chunk_id:
                rel = row["source_relpath"]
                url = self._url_by_relpath.get(rel)
                return Hit(
                    chunk_id=row["chunk_id"],
                    score=0.0,
                    source_path=rel,
                    source_url=url,
                    heading=row.get("heading") or "",
                    text=row["text"],
                    start_line=int(row.get("start_line", 0)),
                )
        return None

    def excerpt_around_chunk(
        self,
        chunk_id: str,
        window: int | None = None,
    ) -> dict[str, Any] | None:
        hit = self.get_chunk_by_id(chunk_id)
        if not hit:
            return None
        w = window or config.EXCERPT_WINDOW_CHARS
        text = hit.text
        return {
            "chunk_id": chunk_id,
            "source_path": hit.source_path,
            "source_url": hit.source_url,
            "heading": hit.heading,
            "excerpt": _truncate(text, w),
            "start_line": hit.start_line,
        }

    def graph_neighbors_for_hits(self, hits: list[Hit]) -> dict[str, Any]:
        """Bipartite-style graph: document nodes linked to chunk ids from one retrieval."""
        docs: dict[str, dict[str, Any]] = {}
        for h in hits:
            doc = h.source_path
            if doc not in docs:
                docs[doc] = {
                    "id": doc,
                    "label": os.path.basename(doc),
                    "url": h.source_url,
                    "chunks": [],
                }
            docs[doc]["chunks"].append(h.chunk_id)
        nodes = [{"id": d["id"], "label": d["label"], "url": d["url"], "type": "doc"} for d in docs.values()]
        edges = []
        doc_ids = list(docs.keys())
        for i in range(len(doc_ids)):
            for j in range(i + 1, len(doc_ids)):
                a, b = doc_ids[i], doc_ids[j]
                edges.append({"source": a, "target": b, "weight": 1.0})
        return {"nodes": nodes, "edges": edges}


def get_store() -> CorpusIndex:
    global _store
    with _store_lock:
        if _store is None:
            _store = CorpusIndex()
        return _store
