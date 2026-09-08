# Before Thinking

This repository is the pre-registration and local harness for studying when a
reasoning model becomes committed to its final answer.

The central methodological choice is to keep three notions separate:

1. **readout time** — when a held-out probe can predict the outcome;
2. **branch commitment time** — when independently sampled continuations from
   the same prefix converge on one answer;
3. **causal irreversibility time** — when matched interventions can no longer
   change the answer without destroying the continuation.

A decodable answer is not, by itself, a committed answer. See
[`docs/research-landscape.md`](docs/research-landscape.md) for the literature
audit and [`docs/experiment-plan.md`](docs/experiment-plan.md) for the proposed
pilot and decision gates.

## Local setup

```bash
uv sync --extra gpu --extra dev
uv run before-thinking doctor
uv run pytest
uv run ruff check .
```

The default local model is `Qwen/Qwen3-1.7B`. Model weights and generated
artifacts are deliberately excluded from version control. No weights are
downloaded by setup or tests.

Model downloads use `aria2c` with resumable segmented transfers. Install
`aria2`, then prefetch the pinned snapshot with:

```bash
HF_HOME=$PWD/models/huggingface uv run before-thinking download-model
```

The snapshot is stored below `HF_HOME/aria2/` and the smoke command reads it
locally, so Transformers does not start a second Hub download. Tune the
connection count if needed, for example `--connections 32 --splits 32`.

## Pilot configuration

[`configs/pilot.yaml`](configs/pilot.yaml) fixes the initial model, datasets,
sampling parameters, checkpoints, and statistical thresholds. The first real
run is intentionally bounded. It should establish that generation, parsing,
branching, hidden-state capture, and grouped evaluation work before any larger
download or sweep.
