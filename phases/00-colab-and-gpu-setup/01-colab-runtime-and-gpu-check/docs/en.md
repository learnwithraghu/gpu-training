---
title: "Colab Runtime and GPU Check"
type: "Build"
phase: "00-colab-and-gpu-setup"
lesson: "01-colab-runtime-and-gpu-check"
duration_minutes: 30
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "Basic Python"
objectives:
  - "Verify GPU runtime health in Colab"
  - "Read GPU hardware and CUDA availability details"
colab_url: "https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/00-colab-and-gpu-setup/01-colab-runtime-and-gpu-check/notebook/main.ipynb"
---

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/00-colab-and-gpu-setup/01-colab-runtime-and-gpu-check/notebook/main.ipynb)

## Motto
Never benchmark before confirming your runtime.

## Problem
Learners often run GPU lessons on CPU-only runtime by mistake and get misleading results.

## Concept
Colab sessions are ephemeral, so runtime checks must happen every session. `nvidia-smi` validates hardware, and `torch.cuda.is_available()` confirms framework access.

## Build It
Run setup cells that print GPU model, CUDA availability, memory limits, and a tiny tensor test on GPU.

## Use It
Use this lesson as a mandatory preflight before any GPU benchmark or training notebook.

## Ship It
Produce a reusable preflight checklist in `outputs/gpu-preflight-checklist.md`.
