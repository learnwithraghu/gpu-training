# GPU Fundamentals Role Mapping

## DevOps

- Track GPU utilization and idle windows.
- Prevent waste from repeated host-to-device transfers.
- Balance queueing and workload placement.

## Data Science

- Tune batch size and precision to improve training throughput.
- Monitor VRAM to avoid OOM during experimentation.
- Use GPU-friendly tensor operations over Python loops.

## Data Engineering

- Use vectorized GPU data transforms for large datasets.
- Watch memory and transfer overhead in ETL stages.
- Optimize for throughput per dollar, not only raw speed.
