# Section 03 - GPUs for Data Science

## Teaching Outcome

Learners understand how to use GPUs for data science workloads. This includes converting NumPy arrays to PyTorch tensors, accelerating Pandas-like operations, and training a simple machine learning model on a GPU.

## Goals of this session

Our audience is data scientists who know Python and SQL. They are hitting Out-Of-Memory (OOM) errors and want to optimize their ML models. They are new to GPU programming.

*   Explain how tensors are used in PyTorch, and the difference between PyTorch tensors and NumPy arrays.
*   Show how they can leverage GPUs for Pandas-like operations and how to convert current Pandas code to run on a GPU.
*   Show how simple model training (linear regression, 10 epochs) is done on a GPU.

## Submodules

1.  `notebooks/01-tensors-and-numpy/01-tensors-and-numpy.ipynb`
2.  `notebooks/02-pandas-on-gpu/02-pandas-on-gpu.ipynb`
3.  `notebooks/03-simple-model-training/03-simple-model-training.ipynb`

## What we won't learn?

*   CUDA programming
*   Hardware details
*   Memory hierarchy details
