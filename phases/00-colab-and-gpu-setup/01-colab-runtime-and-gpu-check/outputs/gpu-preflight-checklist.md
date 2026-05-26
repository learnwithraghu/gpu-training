# GPU Preflight Checklist

- Enable GPU runtime in Colab.
- Run `!nvidia-smi` and confirm GPU is listed.
- Check `torch.cuda.is_available()` returns `True`.
- Print active device name.
- Execute one tensor operation on GPU successfully.
- Capture runtime metadata in notebook output.
