# Local toolchain and capacity

Verified on 2026-09-08:

- NVIDIA GeForce RTX 4060 Laptop GPU, 8,188 MiB VRAM, compute capability 8.9;
- NVIDIA driver 610.57.04; CUDA toolkit 13.3;
- Intel Core i7-14650HX, 24 logical CPUs;
- 31 GiB RAM and 31 GiB swap;
- approximately 200 GiB free on the workspace filesystem;
- uv 0.9.27; system Python 3.14.7 (not used by this project).

The project pins Python 3.12 because ML wheels are substantially more reliable
there than on the host's Python 3.14. PyTorch uses its own CUDA runtime wheel;
the host driver, rather than the local `nvcc` version, determines whether that
wheel can execute.

## Capacity rules

- Primary: Qwen3-1.7B BF16 at revision
  `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, batch size 1, sequential
  branches, capped context. The repository reports 2,031,739,904 BF16
  parameters, so weights alone require roughly 4.1 GB before runtime overhead.
- Possible extension: DeepSeek-R1-Distill-Qwen-1.5B BF16.
- Exploratory only: Qwen3-4B/Phi-4-mini-reasoning in 4-bit. Quantization changes
  activations and is not comparable to BF16 without a dedicated control.
- Not local: 7B+ BF16, broad layer × token patch sweeps, or the GPU-week nested
  branching scale used by the safety paper.
- Use Transformers/PyTorch for generation plus hidden states. vLLM is useful for
  throughput but is not the primary measurement engine because arbitrary
  hidden-state capture and patching are central here.

Weights live outside version control. Every artifact manifest must include the
Hugging Face repository, immutable revision, tokenizer file hashes, dtype,
attention implementation, package lock hash, prompt template, seed, and all
decoding parameters.

Set `HF_HOME=$PWD/models/huggingface` before downloads so the cache is local,
ignored, and easy to inventory. The repository uses `aria2c` for resumable,
segmented model downloads. Prefetch the pinned snapshot with:

```bash
HF_HOME=$PWD/models/huggingface uv run before-thinking download-model
```

The default is 16 connections and 16 segments per file, with two files in
flight. Tune these with `--connections`, `--splits`, and `--parallel-files` if
the server or local network behaves better at another level. A real
weight-and-generation smoke is available as:

```bash
HF_HOME=$PWD/models/huggingface uv run before-thinking model-smoke
```

`model-smoke` performs the same aria2 prefetch and then loads the resulting
local snapshot with `local_files_only=True`.
