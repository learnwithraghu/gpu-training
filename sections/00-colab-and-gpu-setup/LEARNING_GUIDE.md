# Section 00 - Colab and GPU Setup

## Teaching Outcome

Learners can reliably start a Colab GPU runtime, verify hardware, and avoid invalid benchmark runs.

## Session Plan (45 minutes)

1. Context: why runtime verification matters
2. Live setup: GPU runtime check in Colab
3. Guided practice: collect a baseline timing
4. Debrief: common pitfalls and preflight checklist

## Teaching Notes

- Emphasize that Colab sessions are ephemeral.
- Require learners to run `nvidia-smi` before every lab.
- Show one failed run scenario (CPU runtime) and compare.

## Notebook Cadence (ultra-short typing)

1. One teaching prompt (markdown)
2. One micro code cell (2-6 lines)
3. One expected-output note
4. One checkpoint question

Keep the pace conversational: pause every 2-3 cells and ask learners what they predict next.

## Notebook

- `notebooks/01-runtime-verification-and-baseline.ipynb`

## Solo Learner Experience (new)

The notebook is deliberately written so a person working completely alone still gets a complete coached experience. After every experiment you will find:

- A rich **Interpretation** block that explains the mental model (not just the numbers)
- **Misconception repair** that names the wrong intuition most people bring and why it feels right
- A **Model answer** to the checkpoint question plus the key distinction
- A warm **"If you're still unsure..."** paragraph that normalizes confusion and gives a concrete next action

At the end there is a full **Lesson Recap**, **Role Lens** paragraphs for DevOps / Data Science / Data Engineering, and a clear **Momentum + Preview** for the next section.

When you teach live, you can still use the prediction prompts and checkpoints for discussion. The extra cells become the "what I would have said if we had more time" or the handout for anyone who wants the deeper version later.

This is the new standard for all notebooks in `sections/`. See `../LEARNER_TUTOR_DESIGN.md`.
