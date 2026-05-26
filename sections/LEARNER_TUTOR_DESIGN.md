# Learner Tutor Experience Design

**Status:** Source of truth for how notebooks in `sections/` should feel for solo learners (and instructors).

This document lives in `sections/` because that is the canonical curriculum source.

## The Problem We Are Solving

Previous notebooks created a warm "trainer voice" but left solo learners with half the story:
- Prediction prompts with no follow-through explanation.
- Checkpoints that were discussion starters with no model answers or misconception repair.
- No consistent recap, role relevance, or "what to do if confused" support.

The result: learners felt they were getting fragments rather than a complete, coached learning loop.

## Core Principle

Every notebook must deliver a **full learning conversation** even when no human is present.

The learner should always be able to answer:
- What just happened?
- Why did it happen that way?
- What would I have gotten wrong if I were guessing?
- How does this matter to someone in my job?
- Did I actually get it?

## The Improved Notebook Contract (for every section)

### Per Major Step (after the experiment / observation)

1. **Prediction prompt** (keep) — "Pause and ask..." forces active thinking.
2. **Micro code cell** (2-6 lines, keep).
3. **Observation / Expected output** (keep, make runnable where possible).
4. **Interpretation** (required new depth) — 3-6 sentences that explain the underlying mental model, not just restate the numbers. Use analogies when helpful.
5. **Misconception repair** (required) — Name the 1-2 most common wrong mental models for this concept and why they feel intuitive but are wrong. Give the corrective insight.
6. **Checkpoint question** (keep, 1-2 focused questions).
7. **Revealed model answer + coaching note** (required) — Provide a strong sample answer + "If your answer was different, the key distinction is...". Warm, specific, never condescending.

### At the End of Every Notebook

- **Lesson Recap** — 4-6 crisp bullets: concepts understood + skills practiced.
- **Role Lens** — One short paragraph each for DevOps, Data Science, Data Engineering showing exactly where this concept appears in their real work this month.
- **Human moment** — One paragraph acknowledging the emotional reality ("This part trips up almost everyone the first time...") and giving permission + next action.
- **Momentum + Preview** — "You now have X. Next section we will use exactly this to do Y. You are ready."

### Tone Rules (Human Touch)

- Use "you" and "we" consistently.
- Acknowledge difficulty and normalize struggle: "If you're feeling...", "That's expected...", "Many experienced engineers still...".
- Celebrate micro-wins: "This small habit will save you days over a career."
- Be direct about what matters for the job, not just the lab.
- Never leave a conceptual loose end.

### What to Remove or Deprecate in Style

- Pure rhetorical questions with zero follow-up.
- "Ask the instructor" as the only path to understanding.
- Wrap-ups that only list what was done, never what it means or why it was hard.

## How Instructors Use This

The `LEARNING_GUIDE.md` in each section remains the live-teaching script. The notebook itself is now also a first-class self-study artifact.

When teaching live:
- Use the prediction prompts and checkpoints for discussion exactly as before.
- The new interpretation and model-answer cells become "what I would have said if we had more time" or "handout for anyone who wants the deeper version".

## Migration Notes

- All 8 current notebooks will be updated to this contract in waves (starting with 00-03).
- The old `phases/` + `catalog.json` structure is legacy. Learner experience improvements happen only in `sections/`.
- When adding new labs or sections, follow this document.

## Success Signals (how we know it is working)

- A solo learner can finish a notebook and, when asked "explain this to a teammate", gives a confident, accurate answer with the right mental model.
- Learners report "I finally understood why X happens" instead of "I followed the steps".
- Instructors report less time spent re-explaining the same concepts in office hours / Slack.

---

This is the standard. Update this file when we learn what works even better.
