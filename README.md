# GPU Engineering From Scratch (Colab First)

A practical curriculum to build GPU literacy for DevOps, Data Science, and Data Engineering roles.

Inspired by the structure of [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) and tailored for GPU workflows that run only in Google Colab.

## What This Curriculum Teaches

- Understand GPU fundamentals without heavy math.
- Benchmark and optimize real workloads in Colab.
- Apply GPU thinking to ML training, data pipelines, and DevOps operations.
- Build role-based capstone projects with measurable performance and cost impact.

## Runtime Policy

All executable labs and projects are designed for Google Colab only.

Every Build/Project lesson includes:

- an `Open in Colab` link
- a notebook at `notebook/main.ipynb`
- copy-ready code blocks on the published site

## Curriculum Shape

- `00-colab-and-gpu-setup`
- `01-gpu-fundamentals`
- `02-gpu-programming-without-fear`
- `03-gpus-for-data-science`
- `04-gpus-for-data-engineering`
- `05-gpus-for-devops-mlops`
- `06-optimization-and-cost-engineering`
- `07-capstone-projects-by-role`

See `docs/syllabus.md` for the detailed map.

## Repository Layout

```text
docs/                  syllabus and learner-facing guides
phases/                phase and lesson content
scripts/               build and validation scripts
site/                  static site source and generated output
.github/workflows/     CI and GitHub Pages deployment
catalog.json           generated lesson catalog
```

## Local Build

```bash
python3 scripts/build_catalog.py
python3 scripts/validate_lessons.py
python3 scripts/build_site.py
```

The generated website will be available under `site/dist/`.

## Deploy (Free) on GitHub Pages

This repo includes `.github/workflows/pages.yml`.

On every push to `main`, GitHub Actions:

1. builds `catalog.json`
2. validates lesson structure and Colab links
3. generates static site files
4. deploys `site/dist` to GitHub Pages

## Current Milestone

Phase 00 and Phase 01 are fully authored with Colab notebooks and outputs:

- GPU runtime verification
- CPU vs GPU benchmarking
- VRAM monitoring
- throughput/latency mental models with role mapping