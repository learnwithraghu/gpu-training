# Roadmap

## Tutor Experience (highest priority 2026)

The single biggest complaint from solo learners was "I feel like I'm getting half the information and there is no human in the loop." We are fixing this by turning every notebook into a complete coached conversation.

- All learner experience improvements now happen exclusively inside `sections/` (the declared source of truth).
- New standard is documented in `sections/LEARNER_TUTOR_DESIGN.md`.
- Section 02 notebook has been fully rewritten in the new Visual Intuition style (custom matplotlib GPU diagrams for memory hierarchy and "transfer storms", learner mutates the pictures, Karpathy-style diagnostic visuals as the primary teaching medium instead of walls of text). See `sections/02-gpu-programming-without-fear/LEARNING_GUIDE.md` + `sections/LEARNER_TUTOR_DESIGN.md`.
- Notebooks 00, 01, and 03 will be redone in the same visual style next (the earlier text-heavy pass is now considered an intermediate prototype).

## Section Rollout Strategy

### Wave 1 (MVP Foundations)

- Finalize `sections/00-colab-and-gpu-setup`.
- Finalize `sections/01-gpu-fundamentals`.
- Ensure notebooks keep ultra-short, explanation-first cell flow.

### Wave 2 (Acceleration Core)

- Ship `sections/02-gpu-programming-without-fear`.
- Ship `sections/03-gpus-for-data-science`.
- Add mixed precision and batch tuning benchmark labs.

### Wave 3 (Infrastructure and Data)

- Ship `sections/04-gpus-for-data-engineering`.
- Ship `sections/05-gpus-for-devops-mlops`.
- Add production simulation artifacts (runbooks, profiling templates).

### Wave 4 (Optimization and Capstone)

- Ship `sections/06-optimization-and-cost-engineering`.
- Ship `sections/07-capstone-projects-by-role`.
- Publish role-specific capstone rubrics and completion criteria.

## Quality Standards

- Each section notebook uses short code cells (2-6 lines) with markdown coaching between them.
- Every notebook follows the Visual Intuition contract in `sections/LEARNER_TUTOR_DESIGN.md`: build or invoke a custom visualizer that makes the core concept visible → run the real experiment → feed the numbers into the picture → let the learner mutate the visual → short diagnostic caption + one killer question about what changed in the picture. The visuals (not prose walls) carry the interpretation, model answer, and misconception repair.
- The notebook must be a first-class artifact for a solo learner; the `LEARNING_GUIDE.md` is the live-instructor companion, not a requirement for understanding.
- Every section remains directly teachable from `LEARNING_GUIDE.md`.

## Success Metrics

- Learners (especially solo) report that they can finish a notebook and confidently explain the concepts to a teammate without re-reading the material.
- A solo learner never feels they only got "half the story" — every conceptual loose end is closed inside the notebook itself.
- Learners can run all MVP labs in Colab without local setup.
- Learners can follow notebooks with minimal typing fatigue.
- Instructors can run a full session directly from section materials and also hand the same notebook to a self-paced student with confidence.
