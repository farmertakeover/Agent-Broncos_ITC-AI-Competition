#!/usr/bin/env python3
"""Chunk corpus markdown, embed with sentence-transformers, write FAISS + metadata."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Iterator

# Allow running from repo root without PYTHONPATH
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import faiss
import numpy as np
from tqdm import tqdm

from retrieval import config

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Install dependencies: pip install -r requirements.txt", file=sys.stderr)
    raise

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)


def load_url_map(corpus_dir: str) -> dict[str, str]:
    """Map corpus filename (as in index.json values) -> canonical URL."""
    idx_path = os.path.join(corpus_dir, "index.json")
    if not os.path.isfile(idx_path):
        return {}
    with open(idx_path, encoding="utf-8") as f:
        raw = json.load(f)
    out: dict[str, str] = {}
    for url, fname in raw.items():
        out[str(fname)] = str(url)
    return out


def iter_chunks_for_file(
    relpath: str,
    text: str,
    max_chunk: int = 1100,
    overlap: int = 150,
) -> Iterator[tuple[str, str, int]]:
    """
    Yields (heading, chunk_text, start_line).
    Markdown-aware: split on ## / ###; sub-split long sections by windows.
    """
    lines = text.splitlines()
    if not lines:
        return

    def line_no(idx: int) -> int:
        return idx + 1

    sections: list[tuple[str, str, int]] = []
    current_heading = ""
    buf: list[str] = []
    buf_start = 0

    def flush_buf(start_ln: int) -> None:
        nonlocal buf, current_heading, buf_start
        if buf:
            sections.append((current_heading, "\n".join(buf), start_ln))
            buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        m = HEADING_RE.match(line)
        if m:
            flush_buf(buf_start or line_no(i))
            level = len(m.group(1))
            title = m.group(2).strip()
            current_heading = title if level == 2 else f"{current_heading} > {title}"
            buf_start = line_no(i)
            buf = []
            i += 1
            while i < len(lines):
                line2 = lines[i]
                if HEADING_RE.match(line2):
                    break
                buf.append(line2)
                i += 1
            flush_buf(buf_start)
            continue
        if not buf:
            buf_start = line_no(i)
        buf.append(line)
        i += 1
    flush_buf(buf_start or 1)

    if not sections:
        sections = [("", text, 1)]

    for heading, body, start_line in sections:
        body = body.strip()
        if not body:
            continue
        if len(body) <= max_chunk:
            yield heading, body, start_line
            continue
        step = max_chunk - overlap
        for win_start in range(0, len(body), step):
            piece = body[win_start : win_start + max_chunk]
            if not piece.strip():
                break
            yield heading, piece.strip(), start_line


def stable_chunk_id(relpath: str, heading: str, start_line: int, body: str) -> str:
    h = hashlib.sha256(f"{relpath}|{heading}|{start_line}|{body[:200]}".encode()).hexdigest()
    return h[:20]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build FAISS index for CPP markdown corpus.")
    ap.add_argument("--corpus-dir", default=config.CORPUS_DIR)
    ap.add_argument("--index-dir", default=config.INDEX_DIR)
    ap.add_argument("--limit-files", type=int, default=0, help="Only index first N files (dev).")
    ap.add_argument("--embedding-model", default=config.EMBEDDING_MODEL)
    args = ap.parse_args()

    corpus_dir = os.path.abspath(args.corpus_dir)
    index_dir = os.path.abspath(args.index_dir)
    print(f"Corpus dir: {corpus_dir}")
    print(f"Index dir:  {index_dir}")
    if not os.path.isdir(corpus_dir):
        print(f"Corpus directory does not exist: {corpus_dir}", file=sys.stderr)
        sys.exit(1)
    idx_json = os.path.join(corpus_dir, "index.json")
    if not os.path.isfile(idx_json):
        print(f"Warning: no index.json at {idx_json} (URL attribution will be empty).", file=sys.stderr)

    os.makedirs(index_dir, exist_ok=True)

    url_by_file = load_url_map(corpus_dir)
    relpath_to_url = {}
    for fname, url in url_by_file.items():
        relpath_to_url[fname] = url

    md_files: list[str] = []
    for root, _, files in os.walk(corpus_dir):
        for name in files:
            if not name.endswith(".md"):
                continue
            if name == "index.md" and root == corpus_dir:
                pass
            full = os.path.join(root, name)
            md_files.append(full)
    md_files.sort()
    if args.limit_files:
        md_files = md_files[: args.limit_files]

    rows: list[dict] = []
    texts_for_encode: list[str] = []

    for full in tqdm(md_files, desc="Chunking"):
        relpath = os.path.relpath(full, corpus_dir).replace(os.sep, "/")
        try:
            with open(full, encoding="utf-8", errors="replace") as f:
                raw = f.read()
        except OSError:
            continue
        if not raw.strip():
            continue
        for heading, chunk_text, start_line in iter_chunks_for_file(relpath, raw):
            cid = stable_chunk_id(relpath, heading, start_line, chunk_text)
            rows.append(
                {
                    "chunk_id": cid,
                    "source_relpath": relpath,
                    "heading": heading,
                    "start_line": start_line,
                    "text": chunk_text,
                }
            )
            # Encode heading + body for better retrieval
            texts_for_encode.append(f"{heading}\n{chunk_text}" if heading else chunk_text)

    if not rows:
        print("No chunks produced; check corpus path.", file=sys.stderr)
        sys.exit(1)

    print(f"Encoding {len(rows)} chunks with {args.embedding_model} …")
    model = SentenceTransformer(args.embedding_model)
    batch = 64
    embs: list[np.ndarray] = []
    for i in tqdm(range(0, len(texts_for_encode), batch), desc="Embedding"):
        batch_texts = texts_for_encode[i : i + batch]
        v = model.encode(
            batch_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        embs.append(v.astype("float32"))
    mat = np.vstack(embs)
    dim = mat.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(mat)

    faiss_path = os.path.join(index_dir, f"{config.INDEX_NAME}.faiss")
    meta_path = os.path.join(index_dir, f"{config.INDEX_NAME}.meta.jsonl")
    faiss.write_index(index, faiss_path)

    with open(meta_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    url_map_out = os.path.join(index_dir, "url_map.json")
    with open(url_map_out, "w", encoding="utf-8") as f:
        json.dump(relpath_to_url, f, ensure_ascii=False, indent=0)

    print(f"Wrote {faiss_path} ({index.ntotal} vectors, dim={dim})")
    print(f"Wrote {meta_path}")
    print(f"Wrote {url_map_out}")


if __name__ == "__main__":
    main()
