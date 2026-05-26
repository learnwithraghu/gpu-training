# Lesson Template

Use this template for every lesson under:

`phases/<NN-phase>/<NN-lesson>/docs/en.md`

---
title: "<Lesson Title>"
type: "Learn | Build | Project"
phase: "<NN-phase-slug>"
lesson: "<NN-lesson-slug>"
duration_minutes: 45
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "<Prerequisite 1>"
  - "<Prerequisite 2>"
objectives:
  - "<Objective 1>"
  - "<Objective 2>"
colab_url: "https://colab.research.google.com/github/<owner>/<repo>/blob/main/phases/<NN-phase>/<NN-lesson>/notebook/main.ipynb"
---

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](<colab_url>)

## Motto

One sentence that captures the lesson idea.

## Problem

What practical bottleneck does this lesson solve?

## Concept

Explain the intuition with minimal math.

## Build It

Implement the concept in notebook code cells.

## Use It

Apply the concept to realistic data or model behavior.

## Ship It

What reusable artifact is produced in `outputs/`?

## Notebook Cell Contract (Build/Project Lessons)

Every `notebook/main.ipynb` should include ordered sections:

1. Setup
2. Theory-to-code bridge
3. Benchmark or experiment
4. Interpretation
5. Extensions

## Output Artifacts

At least one of the following in `outputs/`:

- checklist / runbook
- benchmark summary
- troubleshooting guide
- role mapping note
