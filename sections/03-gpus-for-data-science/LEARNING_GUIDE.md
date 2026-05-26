# Section 03 - GPUs for Data Science

## Teaching Outcome

Learners can compare CPU/GPU training behavior and tune batch size with mixed precision safely.

## Session Plan (75 minutes)

1. Training lifecycle review
2. CPU vs GPU training benchmark
3. Batch size and AMP tuning exercise
4. Memory-aware debugging patterns

## Teaching Notes

- Keep model small so learners focus on method, not waiting.
- Encourage evidence-based tuning using measured metrics.
- Require a short interpretation statement after each run.

## Notebook Cadence (ultra-short typing)

1. Prediction prompt before each experiment
2. Micro code cell (2-6 lines)
3. Read metric and explain implication
4. Decide one next tuning step

Maintain instructor persona directly in notebook text, not only in live narration.

## Notebook

- `notebooks/01-training-benchmark-and-tuning.ipynb`

## Solo Learner Experience (new)

This is one of the highest-ROI notebooks for real practitioners. Solo learners now receive:

- After the tuning experiments: deep **Interpretation** of what the throughput vs memory numbers actually mean for production decisions
- Named **Misconception repair** for the "always max out the batch size" and "AMP is only for experts" myths
- Complete **Model answers** to the checkpoint questions with the practical nuance
- Empathetic coaching that acknowledges "if you are feeling lost about what number to actually ship with, that feeling is correct and healthy"

Ends with **Lesson Recap**, **Role Lens** for all three job families, and a strong bridge into the data engineering sections.

Live teaching still works exactly as before using the prediction and decision prompts. The new cells become the permanent reference the learner keeps open in the second monitor while they tune their actual models.

See `../LEARNER_TUTOR_DESIGN.md` for the full standard.
