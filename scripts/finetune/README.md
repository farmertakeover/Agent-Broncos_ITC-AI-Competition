# Optional: Unsloth fine-tune → Ollama

This app answers from the **FAISS corpus** at runtime. Fine-tuning only helps **tone, formatting, and tool-calling behavior**—not replacing retrieval.

## When it is useful

- You have **curated examples** (user question → `search_corpus` / `get_source_excerpt` → final answer with `[1]` citations).
- Base **Gemma 4** (or similar) via Ollama is sloppy on JSON tools or CPP-specific phrasing.

## Outline

1. **Install** Unsloth in a separate Python environment (GPU recommended). For **Gemma 4** specifically, start from [Unsloth’s Gemma 4 docs](https://unsloth.ai/docs/models/gemma-4) (GGUFs, Studio, llama.cpp, MLX). The main repo is [unslothai/unsloth](https://github.com/unslothai/unsloth).
2. **Train** with LoRA / QLoRA on a **Gemma 4** base that matches what you plan to serve (see Unsloth’s fine-tune links from that page).
3. **Merge** adapters into full weights (or export per Unsloth / transformers docs).
4. **Convert** to a format Ollama accepts (e.g. GGUF via `llama.cpp` tooling—check current Ollama import docs).
5. **Create a local Ollama model**:

   ```bash
   ollama create cpp-bronco -f Modelfile
   ```

   Point the `FROM` line in the Modelfile at your GGUF (or use Ollama’s documented import path).

6. **Point the app** at the new tag:

   ```bash
   export OLLAMA_MODEL=cpp-bronco
   ```

## Not covered here

Exact notebook code changes with every Unsloth and Ollama release. Treat this folder as a **checklist**; implement training in a dedicated repo or Colab to keep `requirements.txt` for the Flask app small.
