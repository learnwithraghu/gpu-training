---
title: "CPU vs GPU Architecture Intuition"
type: "Learn"
phase: "01-gpu-fundamentals"
lesson: "01-cpu-vs-gpu-architecture-intuition"
duration_minutes: 35
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "Phase 00 completed"
objectives:
  - "Understand how CPU and GPU hardware differs"
  - "Reason about when GPUs are beneficial"
---

## Motto
CPUs excel at low-latency decision making; GPUs excel at high-throughput parallel work.

## Problem
Many engineers use GPUs as a black box and cannot explain why some workloads speed up while others do not.

## Concept
CPU has fewer powerful cores, strong branch handling, and large caches. GPU has many simpler cores and high memory bandwidth for parallel numerical workloads.

## Build It
No coding in this lesson. Build a mental model that predicts workload behavior.

## Use It
Apply this model before choosing infrastructure for training or analytics tasks.

## Ship It
Write your workload classification checklist in `outputs/workload-classification-checklist.md`.
