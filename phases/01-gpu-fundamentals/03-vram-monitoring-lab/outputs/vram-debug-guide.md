# VRAM Debug Guide

## Quick Commands

```python
torch.cuda.memory_summary()
```

```python
torch.cuda.memory_allocated()
torch.cuda.memory_reserved()
```

## Debug Workflow

1. Capture baseline memory.
2. Run one operation block.
3. Capture memory again.
4. Identify where spikes occur.
5. Reduce batch size or tensor dimensions if needed.

## Common Causes of OOM

- Large batch size
- Unreleased tensors kept in Python lists
- High precision where lower precision is enough
