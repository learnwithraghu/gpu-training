# Teaching Plan: Section 01 — GPU Fundamentals

To teach GPU Fundamentals from first principles, we break the content down into three distinct, logical topics. Each topic has its own dedicated subdirectory containing a focused, Karpathy-style notebook and a custom-designed, pencil-sketch SVG diagram.

---

## Topic 1: Throughput vs. Latency (The Architecture Tradeoff)
*   **Goal**: Deconstruct the difference between CPU latency-optimized design and GPU throughput-optimized design.
*   **Notebook**: `sections/01-gpu-fundamentals/notebooks/01-throughput-vs-latency/01-throughput-vs-latency.ipynb`
*   **Visual Sketch**: `sections/01-gpu-fundamentals/notebooks/01-throughput-vs-latency/images/cpu-vs-gpu-architecture.svg`
    *   *Concept*: Illustrates a CPU with a few large, complex cores (deep caches, control logic) versus a GPU with thousands of tiny, simple ALUs.
*   **Experiment**: Measure sequential element-wise operations on CPU vs. GPU.

---

## Topic 2: Arithmetic Intensity & The Memory Wall
*   **Goal**: Introduce the concept of the memory wall, PCIe transfer bottlenecks, and how computing efficiency is bound by bytes transferred vs. operations performed.
*   **Notebook**: `sections/01-gpu-fundamentals/notebooks/02-memory-vs-compute/02-memory-vs-compute.ipynb`
*   **Visual Sketch**: `sections/01-gpu-fundamentals/notebooks/02-memory-vs-compute/images/gpu-memory-hierarchy.svg`
    *   *Concept*: Shows the bandwidth differences across CPU RAM, the PCIe bus, GPU HBM, and GPU SRAM (registers).
*   **Experiment**: Benchmark the overhead of `.to("cuda")` transfer versus the time of doing actual computation, showing when copy overhead destroys GPU advantage.

---

## Topic 3: Matrix Multiplication (The Crossover Point)
*   **Goal**: Explain why dense linear algebra is the perfect GPU workload and discover the matrix size "crossover point" where GPU throughput overrides launch latency.
*   **Notebook**: `sections/01-gpu-fundamentals/notebooks/03-matrix-multiplication/03-matrix-multiplication.ipynb`
*   **Visual Sketch**: `sections/01-gpu-fundamentals/notebooks/03-matrix-multiplication/images/matmul-crossover.svg`
    *   *Concept*: A curve plotting Matrix Size vs. Execution Time, visualizing the transition region where the GPU begins to outpace the CPU.
*   **Experiment**: Run a sweep of matrix sizes from $32 \times 32$ to $4096 \times 4096$ on both CPU and GPU, plotting the crossover point.
