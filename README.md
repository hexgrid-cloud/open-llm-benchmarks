# Open LLM Inference Benchmarks — Real-World Throughput, Latency & TTFT on Dedicated GPUs

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

1. [Qwen3.5-9B · RTX5090 · BF16 · SGLang 0.x.y](#bench-rtx5090-qwen3-5-9b-bf16-sglang) — peak **1360.0** output tok/s @ concurrency 64
2. [Qwen3.5-9B · RTX5090 · BF16 · vLLM 0.19](#bench-rtx5090-qwen3-5-9b-bf16-vllm) — peak **1279.2** output tok/s @ concurrency 64

---

<a id="bench-rtx5090-qwen3-5-9b-bf16-sglang"></a>
### Qwen3.5-9B · RTX5090 · BF16 · SGLang 0.x.y

Dataset: **ShareGPT** · max_tokens 256 · temp 0.2 · CUDA 13.0.1 · 32GB VRAM

| concurrency | requests | output tok/s | E2E p95 (s) | TTFT p95 (s) |
|---|---|---|---|---|
| 16 | 1080 | 470.0 | 7.10 | 0.62 |
| 32 | 1080 | 1040.0 | 8.20 | 0.90 |
| **64** | **1080** | **1360.0** | **13.80** | **5.10** |
| 128 | 1080 | 1330.0 | 25.50 | 16.50 |

**Lesson / Outcome:** ILLUSTRATIVE PLACEHOLDER — replace with the real takeaway from your SGLang run (e.g. where throughput peaks and where latency/TTFT degrade).

[**Full benchmark, config & charts →**](results/rtx5090-qwen3.5-9b-bf16-sglang.md)

[↑ Back to index](#benchmark-index)

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

[**Full benchmark, config & charts →**](results/rtx5090-qwen3.5-9b-bf16-vllm.md)

[↑ Back to index](#benchmark-index)

---

_Auto-generated from `data/benchmarks.csv` (2 benchmarks, 8 sweep points). Metric columns = whatever the CSV contains; do not edit this section by hand._

<!-- BENCHMARKS:END -->

## How these are measured

Each benchmark sweeps concurrency against a real ShareGPT workload and records output
tok/s, E2E p95, and TTFT p95 at each level; the peak-throughput row is bolded. Full
protocol — warm-up, sampling, what's held constant, engine flags — is in
[`METHODOLOGY.md`](METHODOLOGY.md). Field-by-field data definitions are in
[`data/README.md`](data/README.md). Pin `engine_version` on every run: inference-engine
releases shift these numbers materially.

## Adding or removing a metric

The tables are schema-driven — the generator renders whatever metric columns the CSV
contains. Add a column to `data/benchmarks.csv` and it appears; remove it and it's gone.
No code change. Then run:

```bash
python scripts/generate_readme_table.py
```

(You'd only edit the script to exclude a new *non-metric* column via `NON_METRIC`, or to
change which column defines the peak via `PEAK_COL`.)

## Reproduce / contribute

```bash
git clone https://github.com/hexgrid-cloud/open-llm-benchmarks
cd open-llm-benchmarks
# add a benchmark: append rows to data/benchmarks.csv (one per concurrency level),
# write results/<gpu>-<model>-<precision>-<engine>.md, drop charts in assets/<slug>/,
# then regenerate the index:
python scripts/generate_readme_table.py
```

Corrections and reproductions welcome — open an issue or PR.

## License

Data and documentation: **CC BY 4.0** (reuse with attribution) — see [`LICENSE`](LICENSE).
Scripts: MIT.

## Citation

```
HexGrid.Cloud. "Open LLM Inference Benchmarks." https://github.com/hexgrid-cloud/open-llm-benchmarks
```
