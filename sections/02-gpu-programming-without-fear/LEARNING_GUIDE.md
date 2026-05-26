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

## Notebook

- `notebooks/01-device-placement-and-vectorization.ipynb`
