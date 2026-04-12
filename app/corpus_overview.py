"""Aggregate corpus filenames into a topic map (not graph RAG — visualization only)."""
from __future__ import annotations

import os
from collections import Counter

from retrieval import config


def corpus_prefix_counts(max_prefixes: int = 80) -> tuple[list[dict], list[dict]]:
    """
    Group markdown files by leading topic token (before __ in filename).
    Returns (nodes, edges) for a star graph: center -> each topic.
    """
    corpus = os.path.abspath(config.CORPUS_DIR)
    if not os.path.isdir(corpus):
        return [], []

    counts: Counter[str] = Counter()
    for root, _, files in os.walk(corpus):
        for name in files:
            if not name.endswith(".md"):
                continue
            base = os.path.splitext(name)[0]
            topic = base.split("__")[0] if "__" in base else base
            topic = topic.lstrip("_").strip() or "root"
            if len(topic) > 48:
                topic = topic[:45] + "…"
            counts[topic] += 1

    top = counts.most_common(max_prefixes)
    center_id = "__corpus__"
    nodes = [{"id": center_id, "label": "CPP crawl", "count": sum(counts.values()), "type": "center"}]
    edges = []
    for tid, c in top:
        nodes.append({"id": tid, "label": tid, "count": c, "type": "topic"})
        edges.append({"source": center_id, "target": tid, "weight": float(c)})

    return nodes, edges
