import statistics
import time

import torch


def benchmark(fn, repeats=10, warmups=3):
    for _ in range(warmups):
        fn()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        timings.append(time.perf_counter() - start)
    return {
        "median_seconds": statistics.median(timings),
        "mean_seconds": statistics.mean(timings),
        "runs": timings,
    }
