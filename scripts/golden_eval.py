#!/usr/bin/env python3
"""Evaluate retrieval against golden questions (path heuristics + optional caps)."""
from __future__ import annotations

import argparse
import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from retrieval import config
from retrieval.store import get_store


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--golden",
        default=os.path.join(REPO_ROOT, "_data", "golden_questions.json"),
    )
    ap.add_argument(
        "--output",
        default=os.path.join(REPO_ROOT, "_data", "eval_results.json"),
    )
    ap.add_argument("--top-k", type=int, default=config.DEFAULT_TOP_K)
    args = ap.parse_args()

    with open(args.golden, encoding="utf-8") as f:
        cases = json.load(f)

    store = get_store()
    try:
        store.ensure_loaded()
    except FileNotFoundError as e:
        print("Index missing:", e, file=sys.stderr)
        sys.exit(2)

    results = []
    hits_ok = 0
    for case in cases:
        q = case["question"]
        want = [s.lower() for s in case.get("path_substrings", [])]
        retrieved = store.search(q, top_k=args.top_k)
        paths = [h.source_path.lower() for h in retrieved]
        matched = any(any(w in p for w in want) for p in paths) if want else bool(paths)
        if matched:
            hits_ok += 1
        results.append(
            {
                "id": case.get("id"),
                "question": q,
                "matched": matched,
                "top_paths": [h.source_path for h in retrieved[:3]],
            }
        )

    summary = {
        "total": len(cases),
        "matched": hits_ok,
        "match_rate": round(hits_ok / max(len(cases), 1), 3),
        "token_saving_caps": {
            "DEFAULT_TOP_K": config.DEFAULT_TOP_K,
            "MAX_TOP_K": config.MAX_TOP_K,
            "MAX_CHUNK_CHARS": config.MAX_CHUNK_CHARS,
            "EXCERPT_WINDOW_CHARS": config.EXCERPT_WINDOW_CHARS,
            "MAX_TOOL_ROUNDS": config.MAX_TOOL_ROUNDS,
            "MAX_CONVERSATION_MESSAGES": config.MAX_CONVERSATION_MESSAGES,
            "FAISS_PREFETCH_K": config.FAISS_PREFETCH_K,
            "USE_RERANKER": config.USE_RERANKER,
        },
    }
    out = {"summary": summary, "results": results}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
