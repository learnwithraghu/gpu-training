# GPU Engineering From Scratch

**`sections/` is the single source of truth** for all learner-facing and instructor-facing curriculum content.

This repo delivers a complete tutor experience for both live classrooms and solo self-paced learners. Notebooks are deliberately designed with full learning loops — prediction, experiment, deep interpretation, misconception repair, model answers, role relevance, and clear recaps — so you never feel like you only got half the story.

## Core Structure

- `sections/` — canonical teaching guides (`LEARNING_GUIDE.md`) + runnable Colab notebooks for each of the 8 sections. See `sections/LEARNER_TUTOR_DESIGN.md` for the exact contract that makes the solo experience feel coached and complete.
- `idea.md` — long-form curriculum direction and rationale
- `ROADMAP.md` — rollout checkpoints (learner experience improvements now happen only in `sections/`)

## Who This Is For

- **Solo learners** — open any notebook in Colab and get the full explanation, not just prompts and code.
- **Instructors** — use `LEARNING_GUIDE.md` for session plans; the notebooks themselves now contain the "what I would have said" depth as first-class cells.
- **Teams** — role-specific framing appears early and often so DevOps, Data Science, and Data Engineering practitioners see themselves immediately.

## Teaching / Learning Path

Follow sections in order:

1. Colab and GPU setup
2. GPU fundamentals
3. GPU programming without fear
4. GPUs for data science
5. GPUs for data engineering
6. GPUs for DevOps and MLOps
7. Optimization and cost engineering
8. Capstone projects by role

Each section includes:

- a `LEARNING_GUIDE.md` you can teach from directly (or use as a self-study companion)
- one focused notebook built to the solo-learner contract (prediction → micro-exercise → interpretation → misconception repair → model answer → recap → role lens)