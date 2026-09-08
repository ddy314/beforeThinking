# Perturbation dynamics: from "magic prefixes" to causal propagation kernels

## Motivation

Reasoning-model behavior can change sharply after interventions that appear small at the surface: changing the first few reasoning tokens, forcing a particular opening phrase, replacing one sentence, inserting a pause-like token, or patching a hidden state. Existing work has shown that some tokens and reasoning sentences are disproportionately important, but a final-answer flip alone does not tell us **how the effect propagated**.

This document turns the informal idea of a chain-of-thought "diffusion effect" into measurable objects. The word *diffusion* is used only as intuition; the primary technical term in this repository is **perturbation propagation**, because effects may decay, persist, branch, or amplify rather than obey a literal diffusion equation.

## 1. Intervention families

For a base prompt `x` and sampled reasoning trajectory `r`, introduce an intervention `delta` at source position `s`. We distinguish:

### Text interventions

- replace one token with a matched token;
- replace one complete reasoning sentence with a same-item alternative;
- force the first `k` reasoning tokens;
- force an opening template such as `we need to ...`;
- insert semantically weak filler or punctuation;
- insert a trained or naturally occurring pause/special token;
- reorder or paraphrase a local reasoning span;
- transplant a prefix from a sibling rollout of the same item.

### State interventions

- residual-stream patch from a same-item sibling trajectory;
- direction addition/subtraction with norm-matched controls;
- attention-head output patch/ablation;
- MLP/feature patching;
- J-space/Jacobian-lens coordinate swap or clamping;
- KV-cache edit when the implementation exposes it cleanly.

Text and state interventions are not assumed equivalent. One project goal is to identify when they converge behaviorally.

## 2. The perturbation-response kernel

Let `P_t^delta(z)` be the next-token distribution at downstream position `t` under intervention `delta`, and `P_t^0(z)` the matched unperturbed distribution. Define token-distribution divergence

\[
K_{\mathrm{tok}}(s,t;\delta)=D_{\mathrm{JS}}(P_t^\delta\,\|\,P_t^0),
\]

using Jensen-Shannon divergence for bounded, symmetric reporting. KL may be retained as a secondary directional statistic.

For hidden state at layer `l`, define

\[
K_h(s,t,l;\delta)=1-\cos(h_{t,l}^\delta,h_{t,l}^0),
\]

plus a norm-sensitive Euclidean statistic after a registered normalization. For groups of states, use CKA or subspace-angle comparisons rather than reducing everything to cosine distance.

For the final-answer distribution estimated by suffix resampling,

\[
K_Y(s,t;\delta)=D_{\mathrm{TV}}\left(B_t^\delta,B_t^0\right),
\]

where `B_t(y)=P(Y=y | x,r_{<=t})` and `D_TV` is total variation distance.

When J-space/Jacobian-lens readouts are available, define a workspace divergence, for example

\[
K_J(s,t,l;\delta)=D\left(J_{t,l}^\delta,J_{t,l}^0\right),
\]

with the exact distance registered according to whether `J` is represented as token logits, normalized concept scores, or coordinates.

Together these form a multi-view kernel

\[
\mathcal K(s,t,l;\delta)=\left(K_{\mathrm{tok}},K_h,K_J,K_Y\right).
\]

The object of interest is its shape over downstream token position and layer depth.

## 3. Summary statistics

A large kernel needs interpretable summaries. Proposed preregistered quantities:

### Integrated cascade magnitude

\[
A(\delta,s)=\sum_{t>s} w_t K_{\mathrm{tok}}(s,t;\delta),
\]

or the analogous hidden/workspace/answer version. Use a registered weighting scheme, preferably uniform over normalized remaining reasoning length in the primary analysis.

### Persistence length

The number of downstream tokens until divergence falls below a baseline-calibrated threshold and remains below it for `q` checkpoints.

### Amplification ratio

\[
G(\delta,s)=\frac{\max_{t>s} K(s,t;\delta)}{K(s,s^+;\delta)+\epsilon}.
\]

`G>1` suggests downstream amplification. This symbol is a scalar statistic and must not be confused with any representation-space name.

### Branch-switch probability

The probability that an intervention changes the modal final-answer class under matched continuation sampling.

### Propagation half-life

The first downstream distance where an appropriately smoothed kernel falls to half its post-intervention maximum. Report only for trajectories whose response is approximately decaying; it is meaningless for oscillatory or amplifying responses.

### Cross-level lag

Measure whether a shift appears first in internal state, workspace readout, next-token distribution, visible text, or final-answer distribution. Estimate lag only at coarse registered checkpoints to avoid pseudo-precision.

## 4. "Magic prefix" research program

A motivating case is the observed community phenomenon where a model performs better when its visible/internal reasoning is forced into a particular opening style, such as a `we need to ...` pattern. The repository `scp3500/oh-we-need` documents such a prompt-layer intervention for DeepSeek V4 and explicitly reports it as a model-specific empirical behavior, not a demonstrated mechanism.

The scientific question is therefore:

> **Why can a very small prefix intervention create a large change in reasoning quality, and which part of the model state carries that change forward?**

Do not begin by assuming overfitting to one canonical CoT phrase. Competing hypotheses must be separated experimentally.

### H-P1: semantic planning prior

The phrase activates a planning/strategy representation. Prediction: paraphrases with matched planning semantics should retain much of the effect; meaningless token-count controls should not.

### H-P2: post-training style basin

The phrase places the model into a reasoning style heavily represented during SFT/RL/post-training. Prediction: exact or near-exact lexical forms outperform semantic paraphrases, and family/version specificity is strong.

### H-P3: extra-compute / delay effect

Any sufficiently neutral extra tokens permit useful additional autoregressive computation. Prediction: matched pause/filler sequences recover the gain once token count and position are controlled.

### H-P4: early trajectory selection

The prefix changes the distribution over latent reasoning modes before substantive computation. Prediction: branch entropy, hidden-state clustering, or J-space contents diverge immediately and remain separated even when later visible text converges superficially.

### H-P5: decoder-format artifact

The apparent gain arises from answer parsing, output formatting, or benchmark interaction. Prediction: gains disappear under semantic answer scoring, randomized output labels, or alternative parsers.

### H-P6: provider/system-prompt interaction

For API models, the effect depends on hidden provider prompt templates, reasoning-budget policies, or serving implementation. Prediction: effect size changes by provider or API surface despite an identical public model name.

## 5. Required controls for prefix experiments

Every claimed prefix effect should include as many of these as feasible:

- exact-token-count random controls;
- punctuation/filler controls;
- semantic paraphrases;
- style-preserving but task-irrelevant controls;
- task-semantic but style-different controls;
- position-shifted copies of the same phrase;
- prefix truncations (`k=1,2,4,8,...` tokens);
- tokenizer-aware controls that preserve token count;
- multiple temperatures including greedy when supported;
- multiple seeds and same-item paired comparisons;
- answer parser-independent scoring;
- provider/model-revision recording;
- unrelated tasks to test whether the intervention is a global style change or reasoning-specific.

The core estimand should be an **average treatment effect within item**, not a raw aggregate accuracy difference.

## 6. Critical points versus critical content

Two concepts must remain distinct.

A **critical position** is a point in the trajectory where many possible interventions have unusually large downstream effects. A **critical content token/sentence** is a particular realized element whose replacement changes the trajectory strongly.

This distinction matters because a model may pass through a generally sensitive decision boundary where almost any perturbation changes the branch, even if the observed token has no special semantic meaning. Conversely, a semantically important token might occur at a mechanically robust point where equivalent paraphrases preserve the state.

Estimate position criticality with a panel of perturbations rather than one replacement.

## 7. Relation to commitment clocks

The propagation program connects directly to `T_read`, `T_branch`, and `T_irrev`.

Before `T_branch`, interventions may redirect which answer basin dominates. After `T_branch` but before `T_irrev`, the branch distribution may be concentrated while targeted state edits still redirect it. After `T_irrev`, registered coherent interventions should have sharply reduced answer-level effect.

This motivates a **susceptibility curve**

\[
\chi(t)=\mathbb E_{\delta\sim\mathcal D}[D_{\mathrm{TV}}(B_t^\delta,B_t^0)],
\]

where `D` is a registered intervention family. A possible empirical signature of commitment is a transition from high to low susceptibility, but this must be reported separately from probe readout.

## 8. Text-to-state mediation analysis

For a robust textual intervention, collect:

1. immediate textual/logit effect;
2. residual-stream displacement at selected layers;
3. J-space/readout displacement if available;
4. downstream branch-distribution effect;
5. a matched activation intervention designed to reproduce the candidate internal displacement.

A mediation-style claim is strongest when:

- text intervention changes internal variable `M`;
- `M` predicts downstream behavioral effect within item;
- direct intervention on `M` reproduces part of the behavior;
- ablating or counter-steering `M` attenuates the text intervention effect;
- random/norm-matched directions do not.

Even then, call `M` a **candidate mediator**, because distributed state changes can violate simple mediation assumptions.

## 9. Experimental scales

### Black-box broad scan

Use many small/cheap API models to identify which prefixes, positions, and tasks show reproducible effects. No mechanistic claim is made here.

### Local white-box replication

Use Qwen3-1.7B BF16 as the primary mechanistic model. Reproduce a small number of high-effect interventions with hidden-state capture and matched suffix branching.

### Targeted extension

Only after a robust local effect, test one larger or differently trained open model. Quantized models are secondary because activation geometry changes with quantization.

## 10. Relevant prior work

- Goyal et al., **Think before you speak: Training Language Models With Pause Tokens**, ICLR 2024: https://arxiv.org/abs/2310.02226
- Lin et al., **Critical Tokens Matter**, ICML 2025: https://arxiv.org/abs/2411.19943
- Bogdan et al., **Thought Anchors: Which LLM Reasoning Steps Matter?**, 2025: https://arxiv.org/abs/2506.19143
- London & Kanade, **Pause Tokens Strictly Increase the Expressivity of Constant-Depth Transformers**, NeurIPS 2025: https://arxiv.org/abs/2505.21024
- Kim et al., **Learning to Insert [PAUSE] Tokens for Better Reasoning**, 2025: https://arxiv.org/abs/2506.03616
- Zhuang et al., **Reliable Control-Point Selection for Steering Reasoning in Large Language Models**, 2026: https://arxiv.org/abs/2604.02113
- Napa et al., **Can Reasoning Models Detect Changes to their Chains of Thought?**, 2026: https://arxiv.org/abs/2606.22085
- Dura et al., **Mechanistic Interpretability of Chain-of-Thought Reasoning via Sequential Activation Patching**, 2026: https://arxiv.org/abs/2608.22332
- `scp3500/oh-we-need`, empirical DeepSeek V4 prefix-style project: https://github.com/scp3500/oh-we-need

## 11. Novelty boundary

"A prefix changes accuracy" is not a research contribution by itself. "A token is important" is already crowded. The defensible contribution is to characterize **where the effect enters, how it propagates, what representational transition accompanies it, whether it changes branch commitment, and whether a matched internal intervention recapitulates it**.

Snapshot: 2026-09-08.
