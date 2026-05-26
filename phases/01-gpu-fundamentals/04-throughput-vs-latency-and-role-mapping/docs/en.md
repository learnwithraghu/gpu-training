---
title: "Throughput vs Latency and Role Mapping"
type: "Learn"
phase: "01-gpu-fundamentals"
lesson: "04-throughput-vs-latency-and-role-mapping"
duration_minutes: 30
languages: ["Python"]
runtime: "Google Colab"
prerequisites:
  - "Lesson 01.02 completed"
objectives:
  - "Differentiate throughput and latency outcomes"
  - "Map GPU fundamentals to DevOps, DS, and DE roles"
---

## Motto
The right metric depends on the job, not the hardware trend.

## Problem
Teams optimize for speed without deciding whether they need higher throughput or lower latency.

## Concept
Throughput measures total work done over time; latency measures completion time of one request. GPU optimization strategies can improve one while hurting the other.

## Build It
Interpret benchmark results from previous lessons through throughput and latency lenses.

## Use It
Choose metrics that match each role:

- DevOps: utilization, queue depth, scheduling efficiency
- Data Science: epoch time, model convergence speed
- Data Engineering: rows processed per second, pipeline cost per run

## Ship It
Write role mapping outputs in `outputs/role-mapping.md`.
