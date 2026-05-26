# Colab Guide

## Runtime Setup

1. Open any lesson notebook using its `Open in Colab` link.
2. In Colab, choose `Runtime > Change runtime type`.
3. Set `Hardware accelerator` to `GPU`.
4. Run the first setup cells.

## Standard Runtime Checks

Run these checks at the top of every notebook:

```bash
!nvidia-smi
```

```python
import torch
print("CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
```

## Working Pattern

- Keep tensors on GPU for as long as possible.
- Minimize CPU<->GPU transfers.
- Benchmark with warmup runs before recording time.
- Capture VRAM usage before and after major operations.

## Troubleshooting

- If CUDA is unavailable, reconnect runtime and reselect GPU.
- If memory errors happen, reduce batch size first.
- If timing is noisy, rerun cells and average multiple trials.
