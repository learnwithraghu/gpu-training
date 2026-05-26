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

## Solo Learner Experience (new)

This notebook was one of the highest-leverage places to add depth because the "move once" rule is where most people silently fail for months.

Solo learners now get:

- After the critical experiments: full **Interpretation** of why the placement change dominates the vectorization change
- Named **Misconception repair** for the "I will just put everything on the GPU at the top of the script" trap
- A complete **Model answer** to the checkpoint plus the key distinction
- Empathetic language that says "this is the section where a lot of people quietly realize their code was accidentally CPU-bound"

Ends with **Lesson Recap**, **Role Lens** for all three personas, and a strong forward link to the data-science section.

When teaching live you can still harvest the prediction and checkpoint moments for discussion. The extra cells become the permanent reference the learner can return to the night before a code review or a production incident.

See the overall standard in `../LEARNER_TUTOR_DESIGN.md`.
