---
title: "Colab Benchmarking Starter Lab"
type: "Build"
phase: "00-colab-and-gpu-setup"
lesson: "03-colab-benchmarking-starter-lab"
duration_minutes: 45
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "Lesson 00.01 completed"
objectives:
  - "Measure operation timing correctly in CPU and GPU contexts"
  - "Understand warmup and synchronization effects"
colab_url: "https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/00-colab-and-gpu-setup/03-colab-benchmarking-starter-lab/notebook/main.ipynb"
---

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/00-colab-and-gpu-setup/03-colab-benchmarking-starter-lab/notebook/main.ipynb)

## Motto
Measure twice, optimize once.

## Problem
Without synchronization and multiple trials, GPU timings are often wrong.

## Concept
GPU kernels launch asynchronously. You must synchronize before recording elapsed time.

## Build It
Implement a helper function for repeated timing and compare CPU/GPU vector operations.

## Use It
Reuse this timing helper in all future labs.

## Ship It
Store your timing helper snippet in `outputs/timing-helper.py`.
