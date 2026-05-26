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

## Submodules topics
1. High cardinality aggregations usecase - Create required datasets using faker and use that to explain things in notebook. Keep it concise.
2. When should data engineers use GPU and when not
3. Spark on GPU vs CuDF thoughts and opinions


Reference teaching style here /Users/raghunandanask/Desktop/github-repo/gpu-training/teaching_style.md 