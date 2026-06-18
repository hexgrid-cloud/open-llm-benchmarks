<div align="center">

# ⚡ Open LLM Inference Benchmarks

### Real-world throughput, latency & TTFT on dedicated GPUs 🚀

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Benchmarks](https://img.shields.io/badge/benchmarks-2-green.svg)](#benchmark-index)
[![vLLM](https://img.shields.io/badge/engine-vLLM-orange.svg)]()
[![SGLang](https://img.shields.io/badge/engine-SGLang-purple.svg)]()
[![NVIDIA GPU](https://img.shields.io/badge/NVIDIA-GPU-76B900?logo=nvidia&logoColor=white)]()

</div>

Reproducible inference benchmarks for open-source LLMs (Llama, Qwen, Gemma, Mistral,
DeepSeek) served on dedicated GPUs with engines like **vLLM** and **SGLang**. Each
benchmark is a **concurrency sweep** (16 → 128) run against the real-world **ShareGPT**
workload, reporting **output throughput, end-to-end p95 latency, and time-to-first-token
p95** at every level — so you can see exactly where a setup peaks and where it falls over.

Unlike quality leaderboards, this measures **serving behavior under load** on known
hardware with a known stack. Every number is single-environment and pinned to its exact
config (GPU, dtype, engine **version**, dataset); these are not universal model
properties. All data lives in [`data/benchmarks.csv`](data/benchmarks.csv) so you can
reproduce or challenge any figure. Maintained by [HexGrid](https://hexgrid.cloud).

<!-- BENCHMARKS:START -->

## Benchmark index

1. [Qwen3.5-9B · RTX5090 · BF16 · vLLM 0.19](#bench-rtx5090-qwen3-5-9b-bf16-vllm) — peak **1279.2** output tok/s @ concurrency 64

---

<a id="bench-rtx5090-qwen3-5-9b-bf16-vllm"></a>
### Qwen3.5-9B · RTX5090 · BF16 · vLLM 0.19

Dataset: **ShareGPT** · max_tokens 256 · temp 0.2 · CUDA 13.0.1 · 32GB VRAM

| concurrency | requests | output tok/s | E2E p95 (s) | TTFT p95 (s) |
|---|---|---|---|---|
| 16 | 1080 | 444.4 | 7.48 | 0.70 |
| 32 | 1080 | 999.9 | 8.55 | 0.99 |
| **64** | **1080** | **1279.2** | **14.59** | **5.68** |
| 128 | 1080 | 1253.3 | 27.01 | 17.92 |

**Lesson / Outcome:** Throughput peaks at concurrency 64 (~1,280 tok/s) then flattens. Pushing to 128 leaves throughput flat but triples TTFT (5.7s -> 17.9s p95) and nearly doubles E2E latency — the extra concurrency only buys queue time. Operate at 64.

![TTFT & TPOT Latency](assets/rtx5090-qwen3.5-9b-bf16-vllm/ttft-tpot-latency.png)

[**Full benchmark, config & charts →**](results/rtx5090-qwen3.5-9b-bf16-vllm.md)

[↑ Back to index](#benchmark-index)

---

<!-- BENCHMARKS:END -->

## How these are measured

Each benchmark sweeps concurrency against a real ShareGPT workload and records output
tok/s, E2E p95, and TTFT p95 at each level; the peak-throughput row is bolded. Full
protocol — warm-up, sampling, what's held constant, engine flags — is in
[`METHODOLOGY.md`](METHODOLOGY.md). Field-by-field data definitions are in
[`data/README.md`](data/README.md). Pin `engine_version` on every run: inference-engine
releases shift these numbers materially.

## Adding a new benchmark

Follow these steps for adding a new benchmark in the repository:
1. Add the rows to `data/benchmarks.csv` — one row per concurrency level (so a 16/32/64/128 sweep = 4 rows). All four rows share the same run_id, repeat the identity columns (model, gpu, engine, version, dataset, etc.), and differ only in concurrency + the metrics. Put your Lesson / Outcome text in the lesson cell of one row (the first is fine; the rest can be blank), and set the report column to the article path.
2. Write the detail article at `results/<gpu>-<model>-<precision>-<engine>.md`. The filename must match the report path in the CSV (that's also what the README anchor is built from).
3. Add charts (if any) to `assets/<gpu>-<model>-<precision>-<engine>/` and reference them in the article with a relative path like ../assets/<slug>/sweep.png.
4. Regenerate and commit:
```bash
python scripts/generate_readme_table.py
git add -A && git commit -m "Add benchmark: <model> <gpu> <engine>"
git push
```

## Adding or removing a metric

The tables are schema-driven — the generator renders whatever metric columns are present in the CSV. 
Add a column to `data/benchmarks.csv` and it appears; remove it and it's gone.
No code change. 
Then run:

```bash
python scripts/generate_readme_table.py
```

(You'd only edit the script to exclude a new *non-metric* column via `NON_METRIC`, or to
change which column defines the peak via `PEAK_COL`.)

## Reproduce / contribute

Corrections and reproductions welcome — open an issue or PR.

## License

Data and documentation: **CC BY 4.0** (reuse with attribution) — see [`LICENSE`](LICENSE).
Scripts: MIT.

## Citation

```
HexGrid.Cloud. "Open LLM Inference Benchmarks." https://github.com/hexgrid-cloud/open-llm-benchmarks
```
