# Internal representations: residual streams, features, and J-space

## 1. Goal

The white-box part of BeforeThinking asks which internal representations accompany and causally mediate changes in reasoning trajectory. The project should resist a common failure mode in interpretability: finding a highly predictive direction and immediately treating it as the model's decision variable.

The correct ladder is:

1. **describe** the state;
2. **decode** information from it;
3. **localize** where the information is concentrated;
4. **intervene** on candidate representations;
5. **test mediation and robustness** under matched controls.

The repository's existing three-clock design provides the behavioral target. This document specifies how internal measurements should connect to it.

## 2. Measurement hierarchy

### 2.1 Residual-stream traces

For selected token positions `t` and layers `l`, record `h_{t,l}`. Primary low-cost analyses:

- norm and cosine trajectory;
- within-item pairwise distances among sibling rollouts;
- PCA only as visualization, never as primary evidence;
- linear CKA between conditions;
- trajectory clustering with item-balanced sampling;
- layerwise distance induced by a registered intervention.

Always compare within the same prompt/item before pooling across items. Problem identity is an enormous confounder.

### 2.2 Linear probes

Probe targets may include:

- exact final answer class;
- final correctness;
- future answer switch;
- branch entropy band;
- presence of later self-correction/backtracking;
- intervention susceptibility class.

Use grouped train/test splits by item. Include prompt-only and surface-text baselines. Report AUROC only when the label structure supports it; also report Brier score, ECE, balanced accuracy, and confidence intervals. A successful probe establishes **decodability**.

### 2.3 Logit lens and tuned lens

The logit lens projects intermediate residuals through the final normalization/unembedding. It is cheap and useful for exploratory maps, but early layers may use a basis poorly aligned with the final decoder. The Tuned Lens learns an affine translator per layer and is a stronger baseline for latent token predictions.

Use these methods to ask whether candidate answer tokens, planning words, error concepts, or branch-specific tokens become decodable before they are emitted. Do not interpret a smooth token-rank trajectory as a literal chain of internal symbolic reasoning.

Reference: Belrose et al., **Eliciting Latent Predictions from Transformers with the Tuned Lens** (2023), https://arxiv.org/abs/2303.08112

## 3. Jacobian lens and J-space

### 3.1 What Anthropic reported

Anthropic's 2026 work **Verbalizable Representations Form a Global Workspace in Language Models** introduces the Jacobian lens (J-lens) and calls the family of verbalizable internal patterns it identifies **J-space**. The method transports a residual-stream vector at layer `l` toward the final-layer basis using an average input-output Jacobian and decodes the result with the model's unembedding.

A simplified expression is

\[
\mathrm{JL}_l(h)=W_U J_l h,
\qquad
J_l = \mathbb{E}\left[\frac{\partial h_{\mathrm{final}}}{\partial h_l}\right].
\]

Anthropic reports that J-space contents can be verbalized, deliberately modulated, used for silent intermediate reasoning, and broadcast to many downstream computations. The workspace is concentrated in an intermediate layer band and occupies only a small fraction of overall activity.

Primary sources:

- paper: https://arxiv.org/abs/2607.15495
- research summary: https://www.anthropic.com/research/global-workspace
- reference implementation: https://github.com/anthropics/jacobian-lens

The open implementation supports Hugging Face decoder transformers and uses Qwen examples, making it unusually relevant to this repository.

### 3.2 Why it matters for BeforeThinking

The original commitment question can be reframed into testable workspace questions:

- Does the future answer become visible in J-space before it is linearly readable by a generic probe?
- Does branch entropy collapse after an answer/plan concept stabilizes in J-space?
- Do high-leverage critical tokens correspond to sharp J-space transitions?
- Does a magic-prefix intervention move the model into a distinct J-space trajectory?
- Are self-correction events preceded by error/uncertainty concepts entering J-space?
- Does causal irreversibility occur after answer-related workspace content becomes broadly broadcast?

These are stronger questions than simply asking whether a final-answer token appears in a lens.

### 3.3 Minimal replication plan

Do not begin by reproducing the full Anthropic paper. The local plan is:

1. fit or load a J-lens for one small Qwen-family model compatible with the local hardware;
2. validate lens quality on simple factual and arithmetic prompts;
3. select a small set of reasoning trajectories already used in WP1/WP2;
4. render layer × token J-lens readouts for candidate concepts;
5. pre-register concept tokens/sets where possible rather than choosing only after looking;
6. compare J-space transition points with `T_read`, `T_branch`, perturbation peaks, and visible critical tokens;
7. only then implement swap/clamp interventions for a small set of coordinates.

The companion repository notes that fitting quality becomes usable with substantially fewer prompts than the paper-scale setup, although this must be verified empirically on our selected model.

### 3.4 J-space controls

- random vocabulary directions;
- matched-frequency token directions;
- same semantic concept expressed by multiple tokens;
- unrelated concept swaps;
- layer-band shifts;
- norm-matched residual perturbations;
- prompt-only controls;
- tokenization controls for multi-token concepts.

A J-lens readout is still a projection method. It should be treated as evidence about a particular verbalizable subspace, not a complete transcript of model cognition.

## 4. Sparse features and circuit tracing

Anthropic's monosemanticity work, cross-layer transcoders, and circuit tracing provide a second route from raw activations to interpretable computation. Their 2025 circuit-tracing work builds attribution graphs whose nodes are interpretable features and whose edges capture influence; the companion **On the Biology of a Large Language Model** reports examples of multi-step internal reasoning, advance planning, backward reasoning, and both faithful and unfaithful chain-of-thought.

Relevant sources:

- **Towards Monosemanticity / Decomposing Language Models Into Understandable Components**: https://www.anthropic.com/research/decomposing-language-models-into-understandable-components
- **Circuit Tracing: Revealing Computational Graphs in Language Models**: https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html
- **On the Biology of a Large Language Model**: https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html
- open-source circuit-tracing tools: https://www.anthropic.com/research/open-source-circuit-tracing

These methods are computationally heavier than simple hidden-state capture. In BeforeThinking they are **hypothesis-testing tools for a few trajectories**, not the default measurement layer.

## 5. Natural Language Autoencoders

Anthropic's 2026 **Natural Language Autoencoders (NLAs)** map activations to natural-language explanations and train a reverse model to reconstruct the original activation from that explanation. This offers another possible bridge between hidden states and visible reasoning.

Sources:

- https://www.anthropic.com/research/natural-language-autoencoders
- https://transformer-circuits.pub/2026/nla/

For this repository, a full NLA training run is likely outside the first local compute budget. The concept is still important because it supplies a comparison target: if J-space or probes say an answer is present, can an independent activation-to-language method verbalize the same content? This is a future extension rather than a pilot dependency.

## 6. Activation patching

### 6.1 Same-item sibling patching

The primary causal intervention should transfer states between two rollouts of the **same question** that end in different answers or qualitatively different reasoning branches. This sharply reduces semantic and difficulty confounding.

For source trajectory `a`, target trajectory `b`, source token `s`, target token `t`, and layer `l`, replace a registered component of `h^b_{t,l}` with the corresponding state or difference from `a`, then continue generation.

Primary outcomes:

- change in final-answer distribution;
- branch entropy;
- probability of adopting the source answer;
- coherence / perplexity degradation;
- downstream hidden/J-space propagation.

### 6.2 Sequential activation patching

Dura et al. (2026) explicitly study token-distributed CoT causal effects with sequential activation patching and multi-head interventions: https://arxiv.org/abs/2608.22332

Therefore, "patching along a reasoning trajectory" is not a novelty claim. Our extension must connect sequential patching to the propagation kernel, branch commitment, and workspace dynamics.

### 6.3 Hidden solution information

Mehrafarin et al. (2026) show that token-level hidden states can contain recoverable task-solving information even in failed CoTs: https://arxiv.org/abs/2604.23351

This motivates a distinction between:

- **information-bearing states** — contain useful information;
- **decision-driving states** — actually influence the natural continuation;
- **editable states** — can be intervened on without destroying coherence.

BeforeThinking should report these categories separately.

## 7. Activation steering

Baseline methods include:

- ITI / truthfulness directions: https://arxiv.org/abs/2306.03341
- Activation Addition / ActAdd: https://arxiv.org/abs/2308.10248
- representation-engineering methods broadly;
- reasoning-specific steering such as RISER: https://aclanthology.org/2026.findings-acl.226/

Use steering after a correlational direction has been identified, but never treat a successful steer as proof that natural inference uses a one-dimensional variable. Strong steering can push the model off distribution.

Required controls:

- random direction;
- orthogonal direction;
- norm-matched direction;
- sign reversal;
- layer-shift control;
- off-target benchmark degradation;
- KL or perplexity/coherence budget.

## 8. Diagnostic versus causal representations

Yuan et al., **Hidden Error Awareness in Chain-of-Thought Reasoning: The Signal Is Diagnostic, Not Causal** (2026), report strong hidden-state error prediction alongside failed correction/steering interventions: https://arxiv.org/abs/2605.09502

This is especially important for our framing. A signal can be:

1. predictive of future failure;
2. correlated with the computational process causing failure;
3. a downstream byproduct of that process;
4. causally upstream but difficult to edit cleanly;
5. an actual low-dimensional control variable.

The project should be designed to distinguish these possibilities instead of assuming (5).

## 9. Prefill and KV-cache state

Bojie Li's 2026 **Models Take Notes at Prefill: KV Cache Can Be Editable and Composable** reports causal evidence that prefill can write field-conditioned conclusions into downstream KV-cache states: https://arxiv.org/abs/2606.17107

This is directly relevant to the repository name. It suggests another measurement surface besides the final prompt-token residual state. A future white-box extension can compare:

- residual readout at the last prompt token;
- distributed KV-cache state over prompt positions;
- J-space contents during late prefill;
- the first visible reasoning token;
- subsequent branch commitment.

Do not infer from this paper that all tasks are precomputed during prefill. Treat it as a concrete competing mechanism to test.

## 10. Practical local hierarchy

Given the local 8 GB-class GPU budget, prioritize:

**Tier 1:** residual capture, grouped probes, logit lens, branch resampling.

**Tier 2:** J-lens fitting/application on a small model; selected residual patches.

**Tier 3:** head-level sequential patches and a few steering vectors.

**Tier 4:** sparse-feature/circuit-tracing or NLA-style methods only for tightly selected cases or external compute.

Breadth comes from the black-box sweep; mechanistic depth comes from carefully selected local trajectories.

## 11. Main cross-level analyses

The most valuable figures are likely not standalone activation heatmaps. Prefer joint plots such as:

- branch entropy + probe confidence + J-space answer rank versus normalized reasoning time;
- perturbation-response heatmap over token × layer with final-answer treatment effect overlay;
- within-item trajectory map showing correct/incorrect sibling rollouts and their workspace divergence;
- susceptibility curve with `T_read`, `T_branch`, and `T_irrev` markers;
- text intervention versus matched activation intervention effect sizes;
- critical-token score versus J-space transition magnitude and downstream cascade area.

These directly support the program's central thesis: reasoning should be studied as a coupled behavioral and representational dynamical process.

Snapshot: 2026-09-08.
