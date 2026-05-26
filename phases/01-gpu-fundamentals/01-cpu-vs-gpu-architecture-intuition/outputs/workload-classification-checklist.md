# Workload Classification Checklist

Use GPU if:

- Workload is highly parallel.
- Operation is matrix/tensor-heavy.
- Batch processing dominates over single-request latency.

Use CPU if:

- Task has frequent branching and control flow.
- Workload is small and transfer overhead dominates.
- Low-latency per-request response is critical.
