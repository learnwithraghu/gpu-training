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

- `notebooks/01-device-placement-and-vectorization.ipynb` (Visual Intuition Edition, May 2026)

## What changed — Visual Intuition style (new standard)

This notebook has been completely rewritten in the **Visual Intuition** style described in `../LEARNER_TUTOR_DESIGN.md`.

Instead of long prose "model answers" and interpretation blocks, the teaching now happens through three custom matplotlib visualizers the learner builds and then *controls*:

- `draw_memory_hierarchy(pcie_cost=...)` — draws CPU, PCIe pipe (thickness = cost), GPU. The pipe width and color become the visual embodiment of the tax.
- `draw_transfer_storm(n_copies=...)` — draws the "red storm" of individual crossings that the bad pattern creates. Changing `n` and re-drawing makes the pain scale visible.
- `draw_clean_placement()` — the single thick blue arrow + all compute happening inside the green GPU box.

The actual micro-benchmarks (Python loop vs vectorized) are still present, but their timings are now used to label and calibrate the pictures the learner just generated.

After the numbers, the notebook explicitly invites the learner to mutate the visuals ("change n to 35000 and re-draw", "increase pcie_cost to 25 and watch every crossing hurt more").

The checkpoint is now a question about what changed in the picture when they mutated it.

This is the Karpathy-inspired approach (diagnostic visualizations as the primary teaching medium, see makemore_part3_bn and micrograd lectures) adapted to GPU hardware intuition. It replaces the earlier text-heavy version.

## Live teaching

Run the visual cells on the projector. The best discussion moments are:
- "Before we run the loop, what will the next frame of the storm diagram look like?"
- "Now change the n parameter in the visual and re-execute. What just happened to the density of red?"
- "Point to the picture and explain to the person next to you why the vectorized line produced the clean blue arrow instead of the storm."

The pictures become the shared artifact.

## Solo learner experience

A person working alone will:
1. Define the visualizers with the notebook.
2. Generate the red storm for 20k elements.
3. Run the real timings.
4. Generate the clean placement picture.
5. Mutate the visuals themselves and feel the scaling.
6. Leave with two mental images they can sketch from memory a week later.

This is the highest-leverage notebook for the "no soul / half information" complaint because "move once" is the single most common silent performance killer in real GPU code.

See the full contract and inspiration in `../LEARNER_TUTOR_DESIGN.md`.
