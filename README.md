# BeforeThinking

**BeforeThinking: Dynamics, Geometry, and Causality of Reasoning in Language Models**

This repository is a research harness and pre-registration workspace for studying how language-model reasoning trajectories form, propagate, and become constrained. The motivating question is whether a model's eventual answer is already strongly determined before visible chain-of-thought begins, but the program is deliberately broader: it connects behavioral branching, chain-of-thought perturbations, hidden activations, causal interventions, and workspace-style representations such as the 2026 Jacobian-lens / J-space framework.

The project keeps three notions of answer commitment separate:

1. **readout time** — when a held-out probe can predict the outcome;
2. **branch commitment time** — when independently sampled continuations from the same prefix converge on one answer;
3. **causal irreversibility time** — when matched interventions can no longer change the answer without destroying the continuation.

A decodable answer is not, by itself, a committed answer. The expanded program also studies how small prefix/token interventions propagate through later reasoning, whether those effects have measurable counterparts in residual/J-space trajectories, and when textual interventions can be reproduced or attenuated by activation-level interventions.

Start with [`docs/README.md`](docs/README.md) for the documentation map. The main umbrella design is in [`docs/unified-research-program.md`](docs/unified-research-program.md), the extended literature audit is in [`docs/literature-map-extended.md`](docs/literature-map-extended.md), and the original bounded three-clock pilot remains in [`docs/experiment-plan.md`](docs/experiment-plan.md).

## Local setup

```bash
uv sync --extra gpu --extra dev
uv run before-thinking doctor
uv run pytest
uv run ruff check .
```

The default local model is `Qwen/Qwen3-1.7B`. Model weights and generated artifacts are deliberately excluded from version control. No weights are downloaded by setup or tests.

Model downloads use `aria2c` with resumable segmented transfers. Install `aria2`, then prefetch the pinned snapshot with:

```bash
HF_HOME=$PWD/models/huggingface uv run before-thinking download-model
```

The snapshot is stored below `HF_HOME/aria2/` and the smoke command reads it locally, so Transformers does not start a second Hub download. Tune the connection count if needed, for example `--connections 32 --splits 32`.

## Pilot configuration

[`configs/pilot.yaml`](configs/pilot.yaml) fixes the initial model, datasets, sampling parameters, checkpoints, and statistical thresholds. The first real run is intentionally bounded. It should establish that generation, parsing, branching, hidden-state capture, and grouped evaluation work before any larger download or sweep.

The repository-level strategy is **black-box breadth, white-box depth**: inexpensive API sweeps identify robust cross-model phenomena, while local open-weight experiments test their internal and causal structure.
