# Experimental matrix and staged execution plan

## Principle

The repository now contains a broad research program, but experiments must remain staged. Each expensive white-box step is unlocked only by a cheaper result that justifies it. This prevents the project from turning into an unfocused sweep of interpretability techniques.

The existing `experiment-plan.md` remains the preregistered pilot for the first commitment study. This document places that pilot in the larger program.

## Phase 0 — plumbing and invariants

**Goal:** verify the measurement stack before interpreting anything.

Model: `Qwen/Qwen3-1.7B` BF16 locally.

Tasks: tiny fixed ARC-Challenge and GSM8K slices.

Verify:

- deterministic dataset IDs;
- chat template and `<think>`/answer parsing;
- seeded generation;
- exact prefix replay;
- hidden-state capture;
- branch resampling;
- artifact manifests;
- grouped evaluation;
- intervention hooks that restore the original result when patch strength is zero.

Gate: no scientific run until raw outputs can be reconstructed from manifests and repeated smoke runs agree within expected sampling variation.

## Phase 1 — commitment pilot (WP1)

Use the existing plan in `experiment-plan.md`.

Primary outputs:

- `T_read`;
- `T_branch`;
- `T_irrev` or an explicit statement that it is not estimable in the pilot;
- distributions of clock gaps;
- same-item correct/incorrect sibling trajectories for later phases.

Key gate: the readout must beat prompt-only/surface baselines and branching uncertainty must be small enough to identify meaningful trajectory differences.

## Phase 2 — black-box prefix discovery (WP2/WP6)

Run a low-cost API sweep across a panel of small models.

Treatments:

- natural reasoning;
- one or more candidate "magic" prefixes;
- semantic paraphrases;
- token-count-matched filler;
- prefix truncation;
- position-shift control.

Tasks: ARC-Challenge, GSM8K, one logic task, one non-reasoning control.

Primary outcomes:

- paired accuracy treatment effect;
- branch entropy change;
- answer-switch probability;
- suffix length;
- cross-family transfer matrix.

Gate for mechanistic follow-up: at least one effect survives item-paired uncertainty intervals, parser-independent scoring, and basic lexical/token-count controls.

## Phase 3 — local perturbation propagation (WP2)

Take only robust Phase 2 interventions that can be reproduced on the local open model, plus sibling-prefix interventions discovered in Phase 1.

For each selected source position `s`, record downstream checkpoints and estimate:

- token-distribution JS divergence;
- final-answer TV distance from branch resampling;
- hidden-state divergence at selected layer depths;
- integrated cascade magnitude;
- persistence/amplification class;
- branch-switch probability.

Controls:

- random token replacement;
- same-length paraphrase;
- random same-item sibling span;
- position-matched intervention;
- no-op intervention.

Gate: continue only if the effect is larger than matched controls and is not explained by obvious incoherence.

## Phase 4 — J-space / Jacobian-lens alignment (WP4)

Fit or apply the Anthropic open Jacobian-lens implementation on a compatible Qwen-family model.

### Calibration tasks

- factual recall;
- simple arithmetic;
- explicit concept-holding prompts;
- answer-token decoding sanity checks.

### Reasoning tasks

For Phase 1/3 trajectories, track registered concept sets:

- final answer class/token;
- intermediate numeric values;
- plan/method words;
- uncertainty/error/backtracking concepts;
- task-specific entities.

Primary analyses:

- J-space transition magnitude versus critical-token score;
- J-space answer rank versus branch entropy;
- timing difference between J-space stabilization and `T_read/T_branch`;
- intervention-induced J-space divergence versus final-answer treatment effect.

Gate: a workspace claim requires replication across items and a control concept panel; cherry-picked screenshots are exploratory only.

## Phase 5 — targeted causal state interventions (WP3/WP4)

Use only positions/layers nominated in previous phases.

Interventions:

1. same-item residual patch;
2. source-minus-target difference vector addition;
3. J-space coordinate swap/clamp where implementation is validated;
4. selected head output patch if a distributed path is suspected.

Primary outcomes:

- source-answer adoption probability;
- answer distribution TV change;
- perturbation propagation kernel after state intervention;
- coherence and KL/perplexity cost;
- attenuation of the original textual treatment when counter-steered.

Controls:

- random direction;
- orthogonal direction;
- sign reversal;
- norm match;
- layer shift;
- unrelated same-item state;
- off-target task performance.

Gate: no mediation claim unless a candidate state both tracks the text intervention and has a controlled causal effect.

## Phase 6 — component/circuit case studies (WP5)

This is intentionally narrow.

Candidates:

- one high-amplification early prefix effect;
- one self-correction/backtracking transition;
- one case where probe readout is early but branch commitment is late;
- one diagnostic-but-noncausal representation if found.

Methods:

- sequential activation patching;
- head-level attribution/ablation;
- feature-level analysis if a suitable SAE/transcoder exists;
- Anthropic/Neuronpedia circuit-tracing tooling where model support is practical.

Deliverable: mechanistic case studies that explain a previously established population-level effect. Do not attempt a complete circuit map of reasoning.

## Phase 7 — replication and generalization

Repeat the strongest finding on at least one additional model family or training regime.

Preferred contrasts:

- base vs reasoning-tuned;
- 1.5–1.7B vs 4B-ish;
- Qwen-family vs another family;
- BF16 primary vs a carefully labeled quantized exploratory replicate.

A final claim should state exactly which dimensions generalized and which did not.

# Shared factor matrix

| Axis | Discovery values | Confirmatory values |
|---|---|---|
| model | many API models | 1–3 open-weight models |
| task | ARC, GSM8K, logic, control | task(s) with robust effect |
| rollout | 2–4 | 8+ or precision-driven |
| temperature | 0 / model default / one higher | preregistered subset |
| prefix length | 0,1,2,4,8,sentence | effect-centered subset |
| token position | early/mid/late | normalized checkpoints |
| layer | 25/50/75/100% | nominated local neighborhood |
| intervention | text controls | text + state causal controls |
| representation | none/API | residual, probe, J-lens, selected components |

# Core response variables

## Behavioral

- correctness;
- exact answer class;
- branch modal mass;
- normalized branch entropy;
- answer-switch probability;
- continuation length;
- self-correction/backtracking frequency;
- parse-failure rate.

## Readout

- AUROC / balanced accuracy;
- Brier score;
- ECE;
- answer-token rank;
- J-space concept rank/score;
- prompt-only baseline gap.

## Propagation

- `K_tok` JS divergence;
- `K_h` residual divergence;
- `K_J` workspace divergence;
- `K_Y` answer-distribution TV distance;
- cascade area;
- persistence length;
- amplification ratio;
- cross-level lag.

## Causal

- intervention flip/adoption rate;
- change in source-answer probability;
- coherence failure;
- KL/perplexity shift;
- off-target degradation.

# Statistical plan

The independent experimental unit is primarily the **item**, not each rollout.

Use:

- grouped splits by item;
- paired bootstrap over items;
- cluster-robust or mixed-effects models for repeated samples;
- Wilson or beta-binomial intervals for branch proportions;
- permutation tests within item for probe/control comparisons;
- false-discovery correction when scanning many token/layer locations;
- preregistered primary positions before fine-grained exploratory heatmaps.

For timing quantities with censored/undefined values, do not coerce them to the trace end. Report undefined rates and consider survival-analysis style summaries if sample size supports them.

# Compute-budget gates

Local limits are described in `local-toolchain.md`. The following rules keep the project within them:

1. do not store every layer × every token activation for the full sweep;
2. store selected positions/layers first, rerun nominated cases for dense traces;
3. branch sampling is sequential/batched conservatively;
4. avoid full activation-patching grids until a sparse set of candidate locations exists;
5. J-lens fitting is a separate cached artifact;
6. 7B+ white-box runs are not assumed in the primary project;
7. remote/API inference provides breadth rather than renting large GPUs by default.

# Negative-result policy

Several null outcomes remain scientifically useful:

- early probe signal disappears under within-item controls;
- prefix gain vanishes with token-count or parser controls;
- J-space events do not align with commitment;
- high predictive directions cannot be steered coherently;
- perturbations mostly decay instead of amplifying;
- effects are strongly family-specific.

The design should preserve these outcomes rather than progressively redefining metrics until an effect appears.

# Recommended first sequence

The concrete execution order is:

1. finish Phase 0 smoke;
2. run the bounded Phase 1 pilot already specified;
3. in parallel, launch a small black-box prefix discovery panel;
4. intersect the two result sets to choose local high-value perturbations;
5. estimate propagation kernels;
6. add J-lens only after the behavioral effect is real;
7. patch only nominated states;
8. replicate the strongest result.

This sequence maximizes the probability that every expensive mechanistic run answers a question established by cheaper evidence.

Snapshot: 2026-09-08.
