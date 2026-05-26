---
title: "CPU vs GPU Matrix Multiplication Lab"
type: "Build"
phase: "01-gpu-fundamentals"
lesson: "02-cpu-vs-gpu-matrix-multiplication-lab"
duration_minutes: 60
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "Phase 00 completed"
objectives:
  - "Benchmark matrix multiplication on CPU and GPU"
  - "Interpret throughput gains and bottlenecks"
colab_url: "https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/01-gpu-fundamentals/02-cpu-vs-gpu-matrix-multiplication-lab/notebook/main.ipynb"
---

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raghunandanask/gpu-training/blob/main/phases/01-gpu-fundamentals/02-cpu-vs-gpu-matrix-multiplication-lab/notebook/main.ipynb)

## Motto
Matrix multiplication reveals GPU value faster than theory slides.

## Problem
Learners need tangible evidence for why tensor-heavy operations accelerate on GPUs.

## Concept
Matrix multiplication is massively parallel and maps efficiently onto GPU cores and memory bandwidth.

## Build It
Benchmark `torch.matmul` on CPU and GPU across increasing matrix sizes.

## Use It
Use results to discuss when transfer overhead cancels GPU benefits.

## Ship It
Create benchmark summary table in `outputs/matmul-benchmark-summary.md`.
