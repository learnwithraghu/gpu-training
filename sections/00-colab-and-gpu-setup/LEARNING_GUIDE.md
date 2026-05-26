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
