# Section 04 - GPUs for Data Engineering

## Teaching Outcome

Learners can identify ETL bottlenecks and design vectorized GPU-friendly pipeline stages.

## Session Plan (75 minutes)

1. Data pipeline bottleneck map
2. CPU baseline for transform tasks
3. GPU/vectorized alternative implementation
4. Throughput and memory interpretation

## Teaching Notes

- Focus on data movement and serialization overhead.
- Treat every stage as measurable (extract, transform, aggregate).
- Ask learners to justify where GPU helps or does not help.

## Notebook Cadence (ultra-short typing)

1. Stage prompt (extract/transform/aggregate)
2. Micro code cell (2-6 lines)
3. Time output readout
4. Bottleneck checkpoint

Use short loops of measurement and interpretation.

## Notebook

- `notebooks/01-etl-bottleneck-and-acceleration.ipynb`
