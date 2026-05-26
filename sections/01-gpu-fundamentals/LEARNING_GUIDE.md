# Section 01 - GPU Fundamentals

## Teaching Outcome

Learners can explain CPU vs GPU architecture tradeoffs and choose GPU acceleration candidates.

## Session Plan (60 minutes)

1. Mental models: throughput vs latency
2. Architecture walkthrough: cores, memory, parallelism
3. Demonstration: matrix multiply behavior
4. Reflection: role-based mapping (DevOps, DS, DE)

## Teaching Notes

- Use intuitive analogies first, formulas second.
- Ask learners to predict performance before running code.
- Tie each concept to practical engineering decisions.

## Notebook Cadence (ultra-short typing)

1. Prompt learners before code
2. Run one micro code cell (2-6 lines)
3. Interpret output together
4. Confirm one takeaway before moving on

Use a coaching tone: "pause and ask", "common mistake", and "debug hint" cues should appear throughout.

## Notebooks

- `notebooks/01-throughput-vs-latency/01-throughput-vs-latency.ipynb`
- `notebooks/02-memory-vs-compute/02-memory-vs-compute.ipynb`
- `notebooks/03-matrix-multiplication/03-matrix-multiplication.ipynb`

## Solo Learner Experience (new)

The notebook now contains the complete coached loop for someone studying alone:

- After each experiment: Interpretation that explains the *why*, not just the numbers
- Explicit **Misconception repair** for the intuitions that feel right but are wrong
- Full **Model answer** to the checkpoint questions with the key distinction called out
- Warm support language for the moment when a solo learner would normally get stuck

The notebook ends with a **Lesson Recap**, three **Role Lens** paragraphs (DevOps, Data Science, Data Engineering), and a **Momentum + Preview** that tells the learner exactly what they are now ready for.

Live instructors can still drive discussion from the prediction and checkpoint prompts. The new cells serve as the "deeper explanation I would give if time allowed" or as post-class reading.

This pattern is now the standard across `sections/`. Reference `../LEARNER_TUTOR_DESIGN.md`.
