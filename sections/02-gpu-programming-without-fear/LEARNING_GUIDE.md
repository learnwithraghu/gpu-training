# Section 02 - GPU Programming Without Fear

## Teaching Outcome

Learners can write GPU-aware code that minimizes host-device transfers and uses vectorized operations.

## Session Plan (60 minutes)

1. Device placement strategy
2. Vectorization over Python loops
3. Transfer overhead demonstration
4. Cleanup patterns and reproducibility

## Teaching Notes

- Repeat: move data once, compute many times.
- Call out synchronization traps when timing GPU code.
- Have learners rewrite one loop-based snippet live.

## Notebook Cadence (ultra-short typing)

1. Prompt: what is the bottleneck?
2. Micro code cell (2-6 lines)
3. Quick readout and interpretation
4. Checkpoint question

Prioritize fast feedback loops over long cells.

## Notebook

- `notebooks/01-device-placement-and-vectorization.ipynb`
