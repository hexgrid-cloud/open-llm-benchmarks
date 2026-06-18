# Methodology

How every number in this repository is produced. Each benchmark is a **concurrency
sweep**: the same model/GPU/engine driven at several concurrency levels so you can see
where throughput peaks and where latency degrades. If a run deviates from this protocol,
its article says so.

## What we measure (per concurrency level)

- **Output tok/s** — aggregate output tokens per second across all concurrent requests.
- **E2E p95** — end-to-end request latency, 95th percentile (seconds).
- **TTFT p95** — time-to-first-token, 95th percentile (seconds). This is where queueing
  pressure shows up first.

The **peak** of the throughput curve (and the concurrency it occurs at) is the headline;
the point just before latency/TTFT spike is the useful operating point.

## Environment held constant

Within one benchmark the *only* swept variable is concurrency; everything else is fixed
and recorded per row: model, dtype, GPU, engine + **version**, CUDA, dataset,
`max_model_len`, `max_tokens`, temperature, streaming. For an **engine comparison**
(e.g. vLLM vs SGLang) those must match across the two runs — otherwise it isn't fair.

## Workload

- **Dataset:** ShareGPT sample (real, multi-turn, multilingual) rather than synthetic
  fixed-length prompts. Record the number of unique prompts and how they're replayed
  across concurrency levels.
- Document `max_tokens` per completion and temperature; both affect throughput.

## Procedure

1. **Warm-up** — load model, run warm-up requests, discard.
2. **Per level** — drive the target concurrency (e.g. 16, then 32, 64, 128) for the full
   prompt set; record output tok/s and latency/TTFT percentiles.
3. **Streaming** — note ON/OFF (TTFT is only meaningful with streaming).
4. **Repeat / stability** — if a level is noisy, re-run and note variance.

## Load tool

Custom harness (being open-sourced). Until it's public, the article documents the engine
launch flags and request parameters needed to reproduce the run.

## Honesty rules (non-negotiable)

- Report the full curve, including the level where adding concurrency stops helping.
- Never present a single-environment number as a universal model property.
- **Pin `engine_version`** — a number from vLLM 0.19 isn't comparable to a later release.
- Mark illustrative/placeholder rows clearly; don't let them be cited as real.
- Optional but encouraged: occasionally cross-check one run against an external GPU or a
  published independent number so readers can sanity-check the range.

## Versioning

Each benchmark batch is a commit; notable batches are tagged as releases. `run_id` + the
commit make any figure traceable.
