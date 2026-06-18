#!/usr/bin/env python3
"""
Generate the benchmark index + per-benchmark sections of README.md from
data/benchmarks.csv.

LAYOUT (between the markers)
----------------------------
## Benchmark index        -> one linked line per benchmark (+ peak hint)
### <model · gpu · precision · engine>   (one section per benchmark)
    config line
    full concurrency-sweep table (peak row bolded)
    **Lesson / Outcome:** ...
    link to the detailed article + back-to-index

DATA MODEL
----------
Each benchmark is a CONCURRENCY SWEEP: one CSV row per concurrency level. All rows
sharing a `run_id` are one benchmark and map to one article (`report`). The
`lesson` value (first non-empty row of the run) is the Lesson/Outcome.

SCHEMA-DRIVEN METRICS
---------------------
Metric columns are not hardcoded. Any CSV column not in `NON_METRIC` is a metric and
is rendered automatically:
  * Add a metric column to the CSV -> appears. No code change.
  * Remove one -> disappears. No code change.
Edit this file only to: add a NON-metric column you don't want shown (-> NON_METRIC),
or rename the throughput column used for the peak (-> PEAK_COL). LABELS is optional
cosmetic prettification.

Usage:  python scripts/generate_readme_table.py
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "benchmarks.csv"
README_PATH = ROOT / "README.md"
START, END = "<!-- BENCHMARKS:START -->", "<!-- BENCHMARKS:END -->"

# ---- configuration (the only things you'd ever edit) -----------------------
PEAK_COL = "output_tok_s"          # column used to find each sweep's peak
NON_METRIC = {                     # everything NOT here is treated as a metric
    "run_id", "date", "model", "model_hf_id", "quant", "gpu", "vram_gb", "cpu",
    "engine", "engine_version", "cuda", "dataset", "max_model_len", "max_tokens",
    "temperature", "report", "notes", "lesson",
}
LABELS = {                         # optional pretty headers (cosmetic)
    "quant": "precision", "concurrency": "concurrency", "requests": "requests",
    "output_tok_s": "output tok/s", "e2e_p95_s": "E2E p95 (s)",
    "ttft_p95_s": "TTFT p95 (s)",
}
# ---------------------------------------------------------------------------


def label(col):
    return LABELS.get(col, col)


def load():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), r.fieldnames


def metric_cols(fieldnames):
    return [c for c in fieldnames if c not in NON_METRIC]


def as_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("-inf")


def peak_row(rows):
    return max(rows, key=lambda r: as_float(r.get(PEAK_COL)))


def group_by(rows, key):
    g = {}
    for r in rows:
        g.setdefault(key(r), []).append(r)
    return g


def title_of(r):
    engine = f"{r.get('engine', '')} {r.get('engine_version', '')}".strip()
    parts = [r.get("model", ""), r.get("gpu", ""), r.get("quant", ""), engine]
    return " · ".join(p for p in parts if p)


def anchor_of(rows):
    """Stable anchor from the article filename (deterministic, link-safe)."""
    report = rows[0].get("report", "").strip()
    base = pathlib.Path(report).stem if report else rows[0].get("run_id", "")
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return f"bench-{slug}"


def first_lesson(rows):
    for r in rows:
        if (r.get("lesson") or "").strip():
            return r["lesson"].strip()
    return ""


def config_line(r):
    bits = []
    if r.get("dataset"):
        bits.append(f"Dataset: **{r['dataset']}**")
    if r.get("max_tokens"):
        bits.append(f"max_tokens {r['max_tokens']}")
    if r.get("temperature"):
        bits.append(f"temp {r['temperature']}")
    if r.get("cuda"):
        bits.append(f"CUDA {r['cuda']}")
    if r.get("vram_gb"):
        bits.append(f"{r['vram_gb']}GB VRAM")
    return " · ".join(bits)


def sweep_table(rows, metrics):
    peak = peak_row(rows)
    head = [label(c) for c in metrics]
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join(["---"] * len(metrics)) + "|"]
    for r in sorted(rows, key=lambda x: as_float(x.get("concurrency"))):
        cells = [r.get(c, "") for c in metrics]
        if r is peak:
            cells = [f"**{c}**" for c in cells]
        out.append("| " + " | ".join(str(c) for c in cells) + " |")
    return "\n".join(out)


def build(rows, fieldnames):
    metrics = metric_cols(fieldnames)
    benches = list(group_by(rows, lambda r: r.get("run_id", "")).values())
    benches.sort(key=lambda rs: tuple(rs[0].get(k, "") for k in ["model", "gpu", "engine"]))

    # index
    idx = ["## Benchmark index", ""]
    for i, rs in enumerate(benches, 1):
        r0, pk = rs[0], peak_row(rs)
        idx.append(f"{i}. [{title_of(r0)}](#{anchor_of(rs)}) — peak "
                   f"**{pk.get(PEAK_COL, '')}** {label(PEAK_COL)} @ concurrency {pk.get('concurrency','')}")
    idx.append("")

    # sections
    sections = []
    for rs in benches:
        r0 = rs[0]
        report = r0.get("report", "").strip()
        link = f"[**Full benchmark, config & charts →**]({report})" if report else ""
        lesson = first_lesson(rs)
        sections.append(
            f'<a id="{anchor_of(rs)}"></a>\n'
            f"### {title_of(r0)}\n\n"
            f"{config_line(r0)}\n\n"
            f"{sweep_table(rs, metrics)}\n\n"
            f"**Lesson / Outcome:** {lesson}\n\n"
            f"{link}\n\n"
            f"[↑ Back to index](#benchmark-index)"
        )

    footer = (f"_Auto-generated from `data/benchmarks.csv` ({len(benches)} benchmarks, "
              f"{len(rows)} sweep points). Metric columns = whatever the CSV contains; "
              "do not edit this section by hand._")

    return "\n".join(idx) + "\n---\n\n" + "\n\n---\n\n".join(sections) + "\n\n---\n\n" + footer


def main():
    rows, fieldnames = load()
    section = build(rows, fieldnames)
    text = README_PATH.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"Markers {START}/{END} not found in README.md.")
    pre, post = text.split(START)[0], text.split(END)[1]
    README_PATH.write_text(f"{pre}{START}\n\n{section}\n\n{END}{post}", encoding="utf-8")
    print(f"OK: {len(rows)} rows, {len(set(r.get('run_id') for r in rows))} benchmarks, "
          f"metrics={metric_cols(fieldnames)}")


if __name__ == "__main__":
    main()
