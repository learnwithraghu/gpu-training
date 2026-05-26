# Learner Tutor Experience Design

**Status:** Source of truth for how notebooks in `sections/` should feel for solo learners (and instructors).

This document lives in `sections/` because that is the canonical curriculum source.

**May 2026 update:** We discovered that adding more text (even "rich interpretation" and "model answers") does not create soul. The notebooks still felt like dense prose with occasional code. The real 10/10 examples (especially Andrej Karpathy's nn-zero-to-hero lecture notebooks — micrograd, makemore part 3, etc.) teach almost entirely through **live-generated custom visualizations** that make the invisible concept visible and interactive. The learner watches the phenomenon happen in pictures they control, not paragraphs they read.

## The Problem We Are Solving

Previous notebooks created a warm "trainer voice" but left solo learners with half the story:
- Prediction prompts with no follow-through explanation.
- Checkpoints that were discussion starters with no model answers or misconception repair.
- Long walls of explanatory text that still left the core mental model abstract.
- No visual externalization of the hardware/software reality (threads, memory movement, utilization, contention).

The result: even after "improvements," the experience felt like reading a very long textbook that occasionally asked you to run a tiny script. No soul.

## Core Principle (updated)

Every notebook must make the **central invisible concept visible and manipulable** by the learner through code they control and pictures they generate.

The learner should finish able to *draw or describe* the phenomenon from memory and explain what changes when you flip the key decision (placement, precision, batch size, etc.).

Inspiration sources (the bar we are matching):
- karpathy/nn-zero-to-hero (especially makemore_part3_bn.ipynb): diagnostic histograms, activation/gradient statistics plots, saturation percentages, update:data ratio trajectories — the plots *are* the teaching.
- VizuaraAI/dna-of-a-transformer: live diagrams synchronized with the exact lines of code, scroll-triggered revelations, "see the data structure as you touch the numbers."
- General high-quality staff engineer notebooks: custom matplotlib figures (not just loss curves), progressive refinement of the same visual, "build the tiny simulator together," intentional "show the disaster visually first."

## The Visual Intuition Notebook Contract (new standard for sections/)

### Overall Rhythm (instead of "Step 1 / Expected output / Long text")

1. **Hero visual or tiny visual builder** — The section often opens by defining or calling a small drawing function that renders the key mental model (memory hierarchy with bandwidth pipes, thread/block grid, transfer arrows, utilization bars, etc.).
2. **"Let's make the bad thing visible"** — Run the naive or slow pattern (the elementwise Python loop, the per-iteration .to(device), the tiny batch, etc.). Immediately call the visualizer with real parameters from that run. The picture shows the pain (storm of red arrows, saturated bars, thick expensive pipes lighting up on every iteration).
3. **Measure + label the visual** — The timing or memory numbers from the run become annotations, widths, colors, or callouts on the diagram the learner just generated.
4. **Fix the decision, re-draw** — Change one line (placement, vectorization, batch size, AMP). Re-invoke the same visual function or its evolved version. Watch the storm disappear, the pipes thin out, the utilization bars light up evenly. The before/after pictures are the "model answer."
5. **Manipulate the visual** — Give the learner explicit cells: "Change the `num_elements` slider parameter in the visualizer and re-draw. What happens to the relative cost of the red arrows?" or "Add a third memory level to the hierarchy drawing."
6. **Short diagnostic captions + one killer question** — After the visual reveal, 2-4 sentences max + one question that forces the learner to articulate what the picture just taught them.
7. **Progressive refinement** — The same visual (or a clearly evolved version) appears 2-4 times across the notebook, getting more annotated, more realistic, or showing the optimized state.

### Visual Style Rules (what makes it feel alive)

- Custom matplotlib figures using patches, FancyArrowPatch, text annotations, colormaps — not generic `plt.plot(loss)`.
- The figures have **story titles** ("Every red arrow below is a full PCIe round-trip that happened inside your loop — 20,000 of them").
- Color is purposeful: red = expensive repeated cost, blue = one-time good transfer, green = local compute, gray = idle.
- Figures are wide where needed (figsize=(14, 5) or (20, 4) like Karpathy's diagnostic rows).
- The code that produces the visual is short, readable, and built in front of the learner (Karpathy "we will implement this tiny thing together").
- No 30-line explanation paragraphs. The picture + 1-3 sentences + the ability to mutate the picture does the work.

### What we deprecate

- Long "Model answer (strong understanding)" blocks of prose.
- "Interpretation" as pure text.
- "Pause and ask" that is never visually closed.
- Checkpoints whose only answer is more text.

The visuals *are* the interpretation, the model answer, the misconception repair (you literally see the wrong mental model produce the bad picture), and the celebration of the fix.

### At the End of Every Notebook (kept, but lighter)

- **Lesson Recap** — still crisp bullets, but one of them usually references "the visual that made X click for me."
- **Role Lens** — short, specific.
- **Human moment** — one warm paragraph.
- **Momentum + Preview** — strong forward link.
- Optional: "Extend the visualizer" exercises (the Karpathy exercise pattern).

### Tone

Still warm, "we", acknowledges confusion. But the empathy now often points at the picture: "If your first reaction to the red storm was 'that can't be how bad it is' — good. That reaction is exactly why we draw it."

## How Instructors Use This

Live teaching: run the visual cells on the projector. The "pause and ask" moments are now "what do you predict the next frame of this diagram will look like after we move the tensor creation?" The pictures become shared objects of discussion.

Self-study: the learner generates the exact same pictures and can mutate them. They leave with mental images, not just bullet points.

## Migration (current state)

- The text-heavy "improved" versions of notebooks 00-03 (May 2026 first pass) are now considered an intermediate step.
- We are redoing them (starting with section 02, the highest-leverage "move once" lesson) in the Visual Intuition style.
- New notebooks (04+) are written directly in this style.
- The old long prose contract is superseded by the visual contract above.

## Success Signals (updated)

- A solo learner, a week later, can sketch from memory the key diagram from the notebook (the transfer arrows, the memory hierarchy pipes, the warp execution grid, whatever the section's hero visual was) and explain what changes when the key decision flips.
- Learners say "I can *see* why the loop was slow now" rather than "I understand the rule."
- When they hit a similar problem in their real code, they think of the picture first, not the bullet point.

---

This is the standard. We update it when we discover even better ways to make the invisible visible.

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
