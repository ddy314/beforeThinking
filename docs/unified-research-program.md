# Unified research program: dynamics, geometry, and causality of machine reasoning

## 1. Central question

The umbrella question is:

> **How does a language model move from an underdetermined prompt state to a constrained reasoning trajectory and final answer, and how are those constraints represented, propagated, and made causal inside the network?**

This formulation intentionally subsumes several narrower questions:

- Is the final answer linearly readable before visible chain-of-thought begins?
- When do independently sampled continuations stop exploring materially different answers?
- Which visible reasoning tokens or sentences exert disproportionate influence over later reasoning?
- Why can tiny prefix changes, apparently stylistic tokens, or model-specific phrases sometimes cause large performance changes?
- Does a textual perturbation create a localized transient, or a persistent cascade through later hidden states and generated reasoning?
- Are the same behavioral shifts recoverable by intervening directly in activations?
- Does an interpretable internal workspace such as Anthropic's 2026 J-space carry the state that mediates these transitions?
- When hidden states contain diagnostic information, is that information actually causal and editable?

The project therefore studies **reasoning state formation**, not merely early-answer prediction.

## 2. Conceptual model

A decoder-only model generates a trajectory through two coupled axes:

1. **depth-time**, the sequence of transformations across layers for a fixed token position;
2. **decode-time**, the sequence of autoregressive token positions.

For prompt `x`, visible reasoning prefix `r_{<=t}`, layer `l`, and final answer `Y`, denote the hidden state by `h_{t,l}`. A useful abstraction is a stochastic state transition process

\[
S_{t+1} \sim \mathcal{F}(S_t, r_t, x; \theta, \xi_t),
\]

where `S_t` is not asserted to be a single privileged vector. It may include the residual stream, KV-cache state, distributed head/MLP activity, and any lower-dimensional readout such as J-space coordinates. `\xi_t` represents sampling randomness.

The measurable final-answer distribution conditioned on a prefix is

\[
B_t(y) = P(Y=y\mid x,r_{\le t}).
\]

The project asks how `B_t`, internal representations, and causal sensitivity evolve together.

## 3. The five layers of evidence

### 3.1 Behavior

Measure final-answer distributions under repeated continuation from exact prefixes. This is the cheapest level and works for remote closed or open models. Primary observables include modal mass, entropy, switch probability, disagreement rate, calibration, answer class, correctness, and continuation similarity.

### 3.2 Visible reasoning text

Treat chain-of-thought as a dynamical sequence whose elements can be perturbed. A token or sentence can be influential even if it is not an error and even if its surface semantics look mundane. Planning, backtracking, uncertainty markers, equations, entities, and apparently stylistic prefixes are all candidate control points.

### 3.3 Internal representations

Read residual streams and component activations. Use progressively stronger methods:

- raw hidden-state statistics and similarity;
- linear probes with strict grouped controls;
- logit/tuned-lens style readouts;
- Jacobian-lens readouts;
- sparse features or attribution graphs when practical;
- activation patching and steering for causal tests.

### 3.4 Workspace / geometry

Anthropic's 2026 **J-space** work suggests a small set of verbalizable internal patterns can act as a global workspace: they can carry silent intermediate reasoning, be deliberately modulated, and broadcast to many downstream computations. The BeforeThinking question becomes sharper in this framework: does commitment coincide with the entry, stabilization, or broadcast of answer-relevant content in such a workspace?

### 3.5 Causality

A decodable state is not necessarily a control variable. The final evidential step is to intervene. Text replacement, prefix insertion, same-item activation patching, J-space coordinate swaps, head/feature ablation, and norm-matched steering should be evaluated with random and orthogonal controls and with coherence checks.

## 4. Core work packages

### WP1 — Commitment clocks

Preserve the existing preregistered pilot. Estimate separately:

- `T_read`: persistent answer readout time;
- `T_branch`: persistent branch concentration time;
- `T_irrev`: persistent causal irreversibility time.

The key result may be disagreement among these clocks rather than a universal early-commitment law.

### WP2 — Prefix susceptibility and cascade dynamics

Study minimal textual interventions introduced before or during reasoning. This includes ordinary perturbations and model-specific "magic prefix" phenomena such as a forced first sentence or repeated `we need to ...`-style pattern. Measure how intervention effects evolve downstream instead of scoring only final accuracy.

Main questions:

- Which positions have high leverage?
- Does a perturbation decay, persist, or amplify?
- Does it change only wording, or branch entropy and answer identity?
- Is the effect semantic, computational-delay-related, or an elicitation artifact learned during post-training?

### WP3 — Text-to-activation correspondence

For perturbations with robust behavioral effects, measure hidden-state divergence over both token and layer axes. Determine whether similar behavioral interventions produce convergent activation directions and whether activation interventions can reproduce the textual effect.

This work package is the bridge between prompt engineering and mechanistic interpretability.

### WP4 — Workspace dynamics and J-space

Fit/apply the open-source Jacobian lens on supported Qwen-family open models. Track answer concepts, plans, intermediate quantities, uncertainty/error concepts, and control words across layer × token position. Test whether workspace events predict branch collapse or precede visible critical tokens.

Where feasible, perform coordinate swaps or clamping with matched controls. Treat J-space as one candidate readout, not as a presupposed unique reasoning substrate.

### WP5 — Distributed reasoning circuits

On a small set of high-value trajectories, use sequential activation patching, head-level analysis, feature methods, or open circuit-tracing tools. The goal is not exhaustive circuit recovery; it is to test specific hypotheses generated by WP2–WP4, especially propagation paths from early control points to later answer representations.

### WP6 — Cross-model black-box scaling

Use a unified API layer such as OpenRouter to run inexpensive behavioral experiments over many small and medium models. The black-box sweep estimates how universal each phenomenon is before spending white-box compute on a few representative models.

Cross-model axes should include model family, size, base vs instruction/reasoning post-training, context length, and where possible provider/quantization. Provider and exact model identifier must be pinned or recorded.

## 5. Main hypotheses

These hypotheses are deliberately falsifiable.

**H1 — Three-clock separation.** `T_read`, `T_branch`, and `T_irrev` will often be ordered but non-identical; early decodability can precede behavioral concentration and causal irreversibility.

**H2 — Early perturbation amplification.** A minority of early reasoning tokens/sentences will produce larger integrated downstream effects than matched later perturbations, beyond simple remaining-context-length effects.

**H3 — Propagation regimes.** Perturbations will fall into at least three empirical regimes: rapidly decaying, persistent but bounded, and amplifying/branch-switching.

**H4 — Workspace mediation.** High-leverage textual interventions will be associated with larger or earlier changes in J-space/workspace readouts than low-leverage lexical controls.

**H5 — Text/activation equivalence is partial.** Some textual interventions will have activation directions that reproduce part of their behavioral effect, while others will depend on distributed context changes and resist low-rank steering.

**H6 — Criticality is distinct from error.** The most causally influential tokens need not contain explicit mistakes; planning, uncertainty resolution, backtracking, or style/control tokens may dominate.

**H7 — Diagnostic signals may be non-causal.** High probe performance for correctness/error or final answer need not imply that steering along the probe direction can repair behavior.

**H8 — Reasoning post-training changes susceptibility.** Reasoning-trained/instruction-tuned models will differ systematically from base models in where high-leverage control points occur and how long perturbations persist.

**H9 — Pause versus semantic-prefix dissociation.** If a prefix effect is primarily additional computation, matched meaningless/pause-like tokens should reproduce it after appropriate training; if it is an elicitation prior, semantically or stylistically matched prefixes should dominate.

**H10 — Commitment/workspace phase relation.** Branch entropy collapse will cluster around identifiable internal representational transitions more strongly than around normalized token position alone.

## 6. A shared mathematical object: the intervention field

For an intervention `\delta` applied at source `s`, define a family of downstream effects

\[
\Delta^{(m)}_{s\to(t,l)}(\delta),
\]

where `m` identifies a metric: hidden-state distance, J-space displacement, next-token distribution divergence, branch-distribution divergence, or final-answer change.

The project treats the collection of these values as an **intervention field**. This is more general than saying that a token is important. It captures where an effect travels, how long it persists, whether it changes representation before behavior, and whether two intervention types share a pathway.

The corresponding detailed estimators are specified in `perturbation-dynamics.md`.

## 7. What would constitute a strong result

A strong paper does not need every work package. Examples of publication-level findings include:

- a reproducible separation among readout, branch, and irreversibility clocks across tasks;
- a robust early-token propagation law with matched lexical and position controls;
- evidence that branch-collapse events align with a J-space transition more strongly than with surface-text markers;
- a demonstration that a model-specific "magic prefix" acts through a measurable, persistent internal trajectory shift rather than merely formatting the text;
- a negative mechanistic result showing that highly predictive hidden signals are not causal, with a clear taxonomy of when editability fails;
- a cross-family phase diagram of reasoning susceptibility followed by a white-box mechanism study on representative models.

## 8. Claims explicitly out of scope

The project should not claim consciousness, a unique "true thought" representation, or that visible CoT is globally faithful/unfaithful. It should not infer causality from attention alone, infer commitment from a single probe threshold, or generalize a 1.7B local result to frontier systems without independent behavioral evidence.

## 9. Naming

A useful full project subtitle is:

> **BeforeThinking: Dynamics, Geometry, and Causality of Reasoning in Language Models**

The name still refers to the motivating question, while the subtitle makes clear that the project covers the entire transition from prefill through visible reasoning to final answer.

Snapshot: 2026-09-08.
