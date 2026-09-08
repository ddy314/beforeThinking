# Paper roadmap and project decomposition

## Why the repository should be broad while papers stay narrow

The research program is deliberately larger than one paper. That is a strength only if each empirical claim can be isolated, preregistered, and finished without waiting for every other work package.

`BeforeThinking` should function as a **research spine**: datasets, rollout storage, prefix replay, activation capture, branching, metrics, and intervention infrastructure are shared. Individual papers then take a small set of hypotheses from that spine.

A useful umbrella title is:

> **BeforeThinking: Dynamics, Geometry, and Causality of Reasoning in Language Models**

The repository can support at least four paper-shaped projects.

## Paper A — When does a reasoning trajectory become committed?

### Core question

When do answer readout, continuation concentration, and causal irreversibility emerge relative to each other?

### Primary novelty

Joint, same-item estimation of three distinct commitment clocks on the same reasoning trajectories.

### Required evidence

- grouped probe controls;
- exact-prefix suffix branching;
- matched causal intervention at selected checkpoints;
- clock-gap distributions;
- difficulty/correctness stratification;
- replication on at least one second model or training regime if feasible.

### Strong result forms

- systematic `T_read < T_branch < T_irrev` in one regime;
- non-monotone or undefined clocks in self-correcting/hard trajectories;
- early decodability that fails to predict causal lock-in;
- task/model-specific phase diagram rather than universal early commitment.

### What not to claim

Do not say the model "has already decided" merely because a linear probe is accurate.

## Paper B — Perturbation propagation in chain-of-thought

### Core question

How do small changes to reasoning prefixes or critical steps propagate through later reasoning and final-answer distributions?

### Primary novelty

A **perturbation-response kernel** over decode time (and, in the white-box subset, layer depth), with quantitative persistence/amplification regimes.

### Experimental anchor

Use a mixture of:

- naturally high-leverage sibling prefixes;
- sentence-level critical points;
- model-specific prefix phenomena such as `we need to ...`-style interventions;
- matched filler/paraphrase/token-count controls.

### Strong result forms

- early positions show larger integrated cascade magnitude after remaining-length controls;
- perturbations fall into reproducible decay/persistence/amplification regimes;
- branch-switches are preceded by internal divergence rather than merely by visible lexical differences;
- a "magic prefix" effect survives rigorous controls and has a characteristic propagation signature.

### What not to claim

Do not call a final accuracy difference a diffusion mechanism. The mechanism claim requires downstream propagation measurements and preferably a white-box replicate.

## Paper C — Workspace transitions and reasoning commitment

### Core question

Do J-space/Jacobian-lens workspace events align with behavioral commitment, critical tokens, and perturbation propagation?

### Primary novelty

Applying the 2026 global-workspace/J-space framework to the **temporal dynamics of reasoning commitment** rather than rediscovering workspace properties.

### Required evidence

- calibrated J-lens on an open reasoning model;
- preregistered concept sets;
- many-item timing analysis;
- controls for token frequency and layer band;
- comparison with generic probes and branch entropy;
- targeted workspace intervention if technically reliable.

### Strong result forms

- answer/plan workspace stabilization predicts branch collapse better than token position;
- high-leverage prefix interventions induce an early persistent workspace shift;
- J-space changes precede visible self-correction;
- workspace readout and generic linear probe diverge in informative regimes.

### What not to claim

Do not identify J-space with consciousness or with the complete internal state of reasoning.

## Paper D — From prompt engineering to representation engineering

### Core question

When a textual prefix changes reasoning, can the effect be matched, attenuated, or reproduced by intervening on the associated internal representation?

### Primary novelty

A controlled bridge between prompt-level treatment and activation-level treatment, tested on the same items and outcomes.

### Required evidence

- robust text treatment first;
- candidate internal displacement identified without using test outcomes improperly;
- matched activation intervention;
- random/orthogonal/norm controls;
- mediation-style attenuation or recapitulation;
- coherence and off-target measurements.

### Strong result forms

- text and activation interventions share a low-dimensional component;
- only part of a text effect is recoverable with a steering direction, implying distributed mediation;
- family-specific magic prefixes correspond to family-specific activation basins;
- highly diagnostic signals fail to mediate behavior, establishing a useful negative boundary.

## Optional Paper E — A behavioral atlas across small reasoning models

This is viable only if the API sweep discovers a clear cross-family law. A catalog of model results alone is weak. It becomes paper-shaped if it identifies a robust scaling or training-regime pattern such as:

- reasoning post-training shifts criticality earlier/later;
- susceptibility curves predict self-correction ability;
- prefix transfer has a structured family × family matrix;
- branch entropy dynamics predict accuracy or test-time scaling efficiency across models.

The API study should otherwise remain a supporting section/data resource for Papers B–D.

## Shared infrastructure that compounds across papers

### Dataset registry

Stable item IDs, prompt templates, parsers, semantic scoring, task metadata, and difficulty bands.

### Rollout store

Raw prompt, visible reasoning, answer, seed, sampling settings, provider/model metadata, and immutable artifact IDs.

### Prefix graph

Each trajectory should be representable as a set of checkpoints with outgoing sampled continuations. This structure supports commitment, prefix consistency, critical-token analysis, and perturbation experiments.

### Activation store

Sparse-by-default selected `(item, rollout, token, layer, component)` records with a rerun path for dense analysis.

### Intervention registry

Every intervention needs a typed record:

- source trajectory;
- source position;
- target trajectory;
- target position/layer;
- intervention family;
- strength;
- control family;
- coherence metrics;
- output artifact IDs.

### Analysis package

Common implementations for grouped splits, hierarchical bootstrap, answer distribution entropy, TV/JS divergence, timing extraction, and propagation metrics.

## Figure roadmap

A coherent visual identity across papers can make the program feel unified.

### Figure family 1 — reasoning timelines

Horizontal token time with stacked tracks for:

- visible CoT segments;
- probe confidence;
- branch entropy;
- J-space concept score;
- intervention susceptibility;
- final `T_read/T_branch/T_irrev` markers.

### Figure family 2 — propagation maps

Token × token or token × layer heatmaps for perturbation response, with source intervention marked explicitly.

### Figure family 3 — phase diagrams

Axes such as difficulty, model size, or reasoning-training regime; color represents clock gap, susceptibility, or amplification class.

### Figure family 4 — text/state correspondence

Scatter or paired plots comparing textual intervention effect with matched activation intervention effect.

### Figure family 5 — branch trees

Same-prefix continuation trees showing where answer classes collapse, reopen, or self-correct.

## Milestone gates

### Milestone M1 — trustworthy pilot

The existing commitment pilot runs end-to-end and yields reproducible branch and probe estimates.

### M2 — one robust perturbation phenomenon

At least one prefix/token/sentence intervention survives matched controls on enough items to justify white-box study.

### M3 — propagation map

The robust intervention has a repeatable downstream behavioral and hidden-state response profile.

### M4 — workspace alignment

J-lens calibration succeeds and its reasoning readouts can be compared quantitatively with M1–M3.

### M5 — causal bridge

At least one candidate internal representation can be intervened on coherently and compared with the textual treatment.

### M6 — independent replication

The central effect replicates on another model or training regime.

A paper can be written at M2–M3 if the behavioral propagation result is strong; it does not have to wait for M4–M6. Conversely, M4–M5 can become a separate mechanistic paper.

## Priority ranking under current compute constraints

1. **Paper A / three clocks** — already scaffolded, local, scientifically clean.
2. **Paper B / perturbation propagation** — cheap behavioral discovery plus manageable local follow-up; best fit to the "diffusion" idea.
3. **Paper C / J-space dynamics** — high upside because the Anthropic code is open and Qwen-compatible, but requires careful replication work.
4. **Paper D / text-to-activation mediation** — potentially the strongest mechanism paper, but depends on B/C finding robust candidates.
5. **Large circuit maps / NLA training** — defer until a narrow question clearly justifies the compute.

## Repository-level thesis

The long-term thesis should remain modest enough to survive negative findings:

> **Reasoning in autoregressive language models is a temporally extended process whose future trajectories become constrained at different times under different operational definitions. Small textual or internal perturbations can reveal where those constraints form and how they propagate. Combining behavioral branching, representation readout, workspace analysis, and causal intervention provides a more faithful account than any one measurement alone.**

This statement remains meaningful whether models commit early, late, non-monotonically, or in family-specific ways.

Snapshot: 2026-09-08.
