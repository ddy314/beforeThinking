# BeforeThinking research documentation

`BeforeThinking` is a research program about **when, where, and how a language model's future reasoning trajectory becomes constrained**. The original question — whether an answer is already determined before visible reasoning begins — remains one work package, but the repository now treats it as part of a broader study of reasoning dynamics.

The program deliberately connects five observational levels:

1. **Behavioral dynamics** — continuation distributions, answer switches, branch entropy, self-correction, and final outcomes.
2. **Textual reasoning dynamics** — critical tokens, planning/backtracking sentences, forced prefixes, special tokens, and downstream cascade effects inside chain-of-thought.
3. **Representation dynamics** — residual-stream states, attention/MLP contributions, probes, activation patches, steering directions, and feature-level representations.
4. **Workspace geometry** — Jacobian-lens / J-space readouts and related low-dimensional or verbalizable internal representations.
5. **Causal dynamics** — matched interventions that ask whether a readable or correlated state is actually used by the model.

The intended scientific contribution is not a claim that models "already know" an answer, or that chain-of-thought is generally post-hoc. The project instead asks whether different operational signatures of commitment and reasoning influence agree, and maps the regimes in which they do not.

## Document map

- [`research-landscape.md`](research-landscape.md) — focused novelty audit for early answer commitment and the three-clock design.
- [`unified-research-program.md`](unified-research-program.md) — the umbrella research question, conceptual model, and work packages.
- [`perturbation-dynamics.md`](perturbation-dynamics.md) — formalization of prefix/token "diffusion" or cascade effects and the proposed perturbation-response kernel.
- [`internal-representations.md`](internal-representations.md) — residual-stream, activation, feature, Jacobian-lens, and J-space program.
- [`blackbox-sweep.md`](blackbox-sweep.md) — inexpensive API/OpenRouter experiments that establish cross-model behavioral regularities before white-box analysis.
- [`experimental-matrix.md`](experimental-matrix.md) — staged experiment matrix, controls, estimands, decision gates, and compute-aware sequencing.
- [`literature-map-extended.md`](literature-map-extended.md) — broader literature map across CoT faithfulness, critical tokens, latent reasoning, activation steering, circuit tracing, and workspaces.
- [`paper-roadmap.md`](paper-roadmap.md) — how the program can yield several focused papers without turning the first paper into an untestable mega-project.
- [`experiment-plan.md`](experiment-plan.md) — preregistered bounded pilot for the original three-clock question.
- [`local-toolchain.md`](local-toolchain.md) — local hardware constraints and reproducibility requirements.

## Unifying notation

For prompt `x`, sampled visible reasoning tokens `r_1, ..., r_T`, token position `t`, layer `l`, and final answer `Y`, write

- `h_{t,l}` for the residual-stream state;
- `B_t = P(Y | x, r_{<=t})` for the continuation-induced final-answer distribution;
- `R_{t,l}` for a chosen readout of `h_{t,l}` (linear probe, tuned/logit lens, Jacobian lens, SAE/feature readout, etc.);
- `I_{s -> t,l}` for the effect at `(t,l)` of an intervention introduced at source position/state `s`;
- `J_{t,l}` for a J-space/Jacobian-lens coordinate or readout when that method is available.

This lets the repository ask the same question at different scales: **what information exists, where does it propagate, when does it become behaviorally constraining, and which representations are causally involved?**

## Research discipline

Every mechanistic statement should identify the level of evidence supporting it. Correlation/readout, behavioral resampling, and causal intervention are separate evidence classes. A probe can demonstrate decodability; branching can demonstrate conditional outcome concentration; a matched intervention can demonstrate causal sensitivity. None alone establishes a unique internal algorithm.

All experiments should preserve exact model revision, tokenizer hash, prompt template, provider when remote, dtype/quantization, decoding parameters, seed, code commit, and artifact hashes. Black-box results are used for breadth; white-box local results are used for mechanism. Cross-level claims require both whenever feasible.

Snapshot: 2026-09-08.
