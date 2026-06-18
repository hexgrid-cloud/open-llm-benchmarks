# Data dictionary — `benchmarks.csv`

**One row = one concurrency level of one benchmark.** A *benchmark* is all rows sharing
a `run_id` (e.g. the 16/32/64/128 sweep of one model+GPU+engine). This file is the
canonical machine-readable source; the README tables and charts are derived from it.

## Identity & environment (these define the benchmark)

| column | type | description |
|---|---|---|
| `run_id` | string | groups the concurrency sweep into one benchmark; ties to one article |
| `date` | YYYY-MM-DD | date executed |
| `model` | string | short display name |
| `model_hf_id` | string | exact Hugging Face model id |
| `quant` | enum | dtype / quantization (`BF16`, `FP8`, `AWQ-4bit`, ...) |
| `gpu` | string | GPU model (e.g. `RTX5090`) |
| `vram_gb` | int | VRAM per GPU |
| `cpu` | string | host CPU/RAM summary |
| `engine` | string | inference engine (`vLLM`, `SGLang`, ...) |
| `engine_version` | string | **pin this** — perf changes between releases |
| `cuda` | string | CUDA version |
| `dataset` | string | workload (e.g. `ShareGPT`) |
| `max_model_len` | int | configured context length |
| `max_tokens` | int | max tokens per completion |
| `temperature` | number | sampling temperature |

## Metrics (one set per concurrency level)

> The generator shows **every** column below automatically. Add or remove a metric here
> and it flows through to the README with no code change.

| column | type | description |
|---|---|---|
| `concurrency` | int | concurrent request level (the swept variable) |
| `requests` | int | requests issued at this level |
| `output_tok_s` | number | aggregate output tokens/sec (peak of this is the headline) |
| `e2e_p95_s` | number | end-to-end request latency, p95 (seconds) |
| `ttft_p95_s` | number | time-to-first-token, p95 (seconds) |

## Bookkeeping

| column | type | description |
|---|---|---|
| `report` | string | path to the article for this benchmark (same for all rows of a `run_id`) |
| `notes` | string | per-row caveats; mark `peak`, deviations, or `ILLUSTRATIVE PLACEHOLDER` |

## Conventions

- Append-only: corrections add a new `run_id` + note rather than editing history.
- Every row of a sweep repeats the identity columns (keeps the file self-contained and
  trivially filterable). The `run_id` ties them together.
- The README summary collapses each `run_id` to its peak-`output_tok_s` row.
