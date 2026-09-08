# Extended literature map

Snapshot: 2026-09-08. This map complements the narrower novelty audit in `research-landscape.md`. It is organized by **which part of the BeforeThinking program a paper constrains**, rather than by publication venue.

The list is intentionally selective. It prioritizes work that changes the design of our experiments or limits a plausible novelty claim.

## 1. Chain-of-thought faithfulness and post-hoc reasoning

### Turpin et al. (2023), Language Models Don't Always Say What They Think

https://arxiv.org/abs/2305.04388

Biasing features can alter answers without being faithfully reported in CoT. This is foundational evidence that visible reasoning cannot automatically be treated as a transparent internal trace.

### Lanham et al. (2023), Measuring Faithfulness in Chain-of-Thought Reasoning

https://arxiv.org/abs/2307.13702

Uses truncation, corruption, paraphrase, and related interventions to operationalize causal dependence on CoT. Important precedent for our text-intervention ladder.

### Anthropic (2025), Reasoning models don't always say what they think

https://www.anthropic.com/research/reasoning-models-dont-say-think

Modern reasoning-model CoTs can omit influential hints and other factors. Reinforces the need for behavioral and mechanistic checks rather than self-report.

### Anthropic (2025), On the Biology of a Large Language Model

https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html

Circuit-tracing case studies distinguish examples of faithful and unfaithful CoT, and show internal multi-step and planning computations. This is important prior art for any broad claim that reasoning is merely visible token generation.

## 2. Early answer/readout and commitment-adjacent work

### Knowing Before Saying / CoTpred (ACL 2025)

Repository: https://github.com/anum94/CoTpred

Shows that initial representations can predict later CoT success. This blocks a novelty claim based solely on "correctness is predictable before reasoning."

### Cox, Kianersi & Garriga-Alonso (2026), Decoding Answers Before Chain-of-Thought

https://arxiv.org/abs/2603.01437

Pre-CoT residual-stream probes strongly predict final answers in several settings, and steering along probe-related directions changes answers. Directly motivates our distinction between readout and commitment.

### Boppana et al. (2026), Reasoning Theater

https://arxiv.org/abs/2603.05488

Compares activation probes, forced answers, and text monitors on large reasoning models. Another reason a simple early-probe study would be incremental.

### Datta et al. (2026), Large Language Models Decide Early and Explain Later

https://arxiv.org/abs/2604.22266

Tracks forced-answer completion at partial reasoning prefixes and observes answer switches. Relevant to behavioral commitment timing.

### Iwase et al. (2026), Reliable Chain-of-Thought via Prefix Consistency

https://arxiv.org/abs/2605.07654

Regenerating suffixes from prefixes predicts correctness and reduces self-consistency cost. Strong prior art for prefix branching as a diagnostic.

### Yuan et al. (2026), Hidden Error Awareness in Chain-of-Thought Reasoning

https://arxiv.org/abs/2605.09502

Hidden states predict trace correctness early, yet several attempted interventions fail. This is a central warning that diagnostic representations may not be causal levers.

### Ri, Panigrahi & Arora (2026), Do Thinking Tokens Help with Safety?

https://arxiv.org/abs/2606.25013

First-thinking-token refusal probes and nested prefix branching show early safety-decision effects. The repository's original project was partly motivated by extending this style of analysis beyond refusal/compliance.

### Jo (2026), Committed Before Reasoning

https://arxiv.org/abs/2607.16451

A controlled small-model case study of pre-commitment. Further narrows the novelty of a generic "answers are decided before reasoning" claim.

## 3. Critical tokens, thought anchors, and control points

### Lin et al. (ICML 2025), Critical Tokens Matter

https://arxiv.org/abs/2411.19943

Rollout contrast identifies tokens with disproportionate effect on reasoning success. Replacing them can improve performance. Important prior art for token-level causal importance.

### Bogdan et al. (2025), Thought Anchors: Which LLM Reasoning Steps Matter?

https://arxiv.org/abs/2506.19143

Code: https://github.com/interp-reasoning/thought-anchors

Uses black-box, attention-based, and causal methods to find sentence-level planning/backtracking steps that disproportionately affect downstream reasoning. Closest precedent for our visible-text cascade experiments.

### Guo et al. (2026), Dynamic Thinking-Token Selection

https://arxiv.org/abs/2601.18383

Uses attention influence to identify decision-critical reasoning tokens and retain only associated KV states. Shows that many thinking tokens may be redundant for final decisions.

### Zhuang et al. (2026), Reliable Control-Point Selection for Steering Reasoning

https://arxiv.org/abs/2604.02113

Reports that many keyword-detected reasoning boundaries are unstable under regeneration, then filters for behaviorally stable control points before extracting steering vectors. This directly motivates our distinction between a surface marker and a reproducible critical point.

### Dura, Öztürk & Tekir (2026), Mechanistic Interpretability of CoT via Sequential Activation Patching

https://arxiv.org/abs/2608.22332

Introduces sequential activation patching across reasoning-token positions and identifies distributed attention-head contributions. Published shortly before this snapshot and important for novelty: token-distributed patching itself is no longer an open gap.

## 4. Pause tokens, filler computation, and latent reasoning

### Goyal et al. (ICLR 2024), Think before you speak: Training Language Models With Pause Tokens

https://arxiv.org/abs/2310.02226

Learned pause tokens give the model extra autoregressive computational positions before answer extraction and improve several tasks when included in training. Essential control for "magic prefix" hypotheses: some benefit may arise from additional computation rather than semantics.

### Quiet-STaR (2024)

https://arxiv.org/abs/2403.09629

Trains models to generate internal rationales around arbitrary text and improves difficult-token prediction and downstream reasoning. Supports the broader idea that useful reasoning need not coincide with the visible answer protocol.

### Hao et al. (2024), Coconut: Training Large Language Models to Reason in a Continuous Latent Space

https://arxiv.org/abs/2412.06769

Feeds continuous hidden states back as latent thoughts. Reports that latent states can encode multiple alternative next steps and support search-like behavior. Relevant to our distinction between visible CoT and underlying reasoning state.

### Xu et al. (ACL 2025), SoftCoT

https://aclanthology.org/2025.acl-long.1137/

Projects continuous soft thoughts into an LLM's embedding space without full-model modification. Adds another example where reasoning can be carried by continuous representations.

### London & Kanade (NeurIPS 2025), Pause Tokens Strictly Increase the Expressivity of Constant-Depth Transformers

https://arxiv.org/abs/2505.21024

Provides a formal expressivity result for pause tokens. Strengthens the need to separate computation-depth effects from semantic-prefix effects.

### Kim, Kim & Thorne (2025), Learning to Insert [PAUSE] Tokens for Better Reasoning

https://arxiv.org/abs/2506.03616

Dynamically inserts pause tokens at low-confidence positions and reports reasoning/code gains. Useful precedent for position-sensitive filler computation.

### Fast Quiet-STaR (EMNLP Findings 2025)

https://aclanthology.org/2025.findings-emnlp.1020/

Studies internalizing reasoning while reducing explicit thought-token overhead. Adds evidence that visible token count and useful internal computation need not align simply.

## 5. Hidden information and activation-level reasoning

### Mehrafarin, Parekh & Konstas (2026), When Chain-of-Thought Fails, the Solution Hides in the Hidden States

https://arxiv.org/abs/2604.23351

Activation patching can recover useful solution information from hidden states, including from failed traces. Motivates separating information-bearing from naturally decision-driving states.

### Chen, Plaat & van Stein (AAAI 2026), How Does Chain of Thought Think?

https://ojs.aaai.org/index.php/AAAI/article/view/40281

Combines sparse autoencoders with activation patching to study CoT-related features. Prior art for feature-level causal CoT analysis.

### Wang, Ma & Xu (AAAI 2026), Eliciting Chain-of-Thought in Base LLMs via Gradient-Based Representation Optimization

https://ojs.aaai.org/index.php/AAAI/article/view/40669

Manipulates hidden states to guide reasoning trajectories while regularizing distribution shift. Relevant to state-space control of reasoning.

### RISER (ACL Findings 2026)

https://aclanthology.org/2026.findings-acl.226/

Builds and adaptively composes reasoning activation vectors. Important for any claim that reasoning-related directions are a new idea.

### Activation Steering for Chain-of-Thought Compression (ACL Findings 2026)

https://aclanthology.org/2026.findings-acl.1828/

Finds concise and verbose CoTs occupy separable activation regions and steers between them. Shows that reasoning style can be encoded as steerable activation structure.

## 6. General representation engineering and causal interventions

### Li et al. (2023), Inference-Time Intervention (ITI)

https://arxiv.org/abs/2306.03341

Shifts selected attention-head activations along truth-related directions. Foundational example of inference-time representation intervention.

### Turner et al. (2023), Activation Addition / activation engineering

https://arxiv.org/abs/2308.10248

Uses contrastive activation differences as steering vectors. A baseline family for our text-to-state correspondence work.

### Belrose et al. (2023), Tuned Lens

https://arxiv.org/abs/2303.08112

Provides calibrated per-layer latent prediction readout and improves on the raw logit lens. Baseline for layerwise answer/readout analysis.

### ROME / causal tracing

https://github.com/kmeng01/rome

Causal tracing and model editing establish standard intervention patterns for locating information and testing causal effects in transformers.

## 7. Anthropic mechanistic interpretability line

### Towards Monosemanticity / dictionary learning

https://www.anthropic.com/research/decomposing-language-models-into-understandable-components

Sparse features can be more interpretable than individual neurons and can be causally steered. Supports feature rather than raw-neuron analysis.

### Circuit Tracing (2025)

https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html

Builds interpretable attribution graphs using cross-layer transcoders and validates hypotheses with interventions.

### On the Biology of a Large Language Model (2025)

https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html

Shows multi-step internal reasoning, planning ahead, multilingual abstraction, hallucination mechanisms, and CoT faithfulness/unfaithfulness case studies in Claude 3.5 Haiku.

### Open-sourcing circuit-tracing tools (2025)

https://www.anthropic.com/research/open-source-circuit-tracing

Makes parts of the circuit-tracing stack usable on open models, including small Gemma/Llama examples. Relevant for targeted future case studies.

### Tracing attention computation through feature interactions (2025)

https://www.transformer-circuits.pub/2025/attention-qk/index.html

Extends feature attribution graphs to better explain why attention patterns arise. Useful if our propagation paths require attention-level explanation.

## 8. J-space / global workspace

### Gurnee et al. (Anthropic, 2026), Verbalizable Representations Form a Global Workspace in Language Models

Paper: https://arxiv.org/abs/2607.15495

Summary: https://www.anthropic.com/research/global-workspace

Code: https://github.com/anthropics/jacobian-lens

Introduces the Jacobian lens and J-space. Reports a small verbalizable workspace that can carry silent intermediate reasoning, be deliberately modulated, and broadcast to downstream computations. This is one of the most important pieces of prior work for the expanded BeforeThinking program.

Our opportunity is not to rediscover J-space. It is to study **workspace dynamics during reasoning commitment and perturbation propagation**, especially on open reasoning models and with branch-level behavioral measures.

## 9. Natural-language decoding of activations

### Fraser-Taliente et al. (Anthropic, 2026), Natural Language Autoencoders

https://transformer-circuits.pub/2026/nla/

Maps activations to natural-language explanations and reconstructs activations from those explanations. This is a future comparison point for whether answer/planning information identified by other methods is independently verbalizable.

## 10. Prefill as computation and memory

### Li (2026), Models Take Notes at Prefill: KV Cache Can Be Editable and Composable

https://arxiv.org/abs/2606.17107

Reports that prefill can write field-conditioned conclusions into downstream KV-cache states. This is directly relevant to the question of what has already been computed before visible reasoning starts.

### Anthropic introspection work (2025)

https://www.anthropic.com/research/introspection

Includes experiments with artificially prefilled outputs and injected internal concepts, suggesting a possible mismatch-detection mechanism between intended and observed output. Relevant to forced-prefix interventions and whether models detect externally altered CoTs.

### Napa et al. (2026), Can Reasoning Models Detect Changes to their Chains of Thought?

https://arxiv.org/abs/2606.22085

Finds only modest detection of edited CoTs in tested reasoning models. This helps justify prefix transplantation as an intervention while also motivating explicit tamper-detection controls.

## 11. Empirical "magic prefix" observation

### scp3500/oh-we-need (2026)

https://github.com/scp3500/oh-we-need

A community repository documenting a `we need to ...` reasoning-style prompt for DeepSeek V4 variants. It explicitly presents the effect as prompt-layer empirical behavior and does not supply mechanistic evidence for why it works.

This is useful as a motivating phenomenon, not as scientific ground truth. BeforeThinking can transform this kind of observation into a controlled question: semantic planning prior, post-training style basin, added-compute effect, early trajectory selection, parser artifact, or provider/system-prompt interaction?

## 12. What remains comparatively open

The literature is crowded around individual pieces. The strongest remaining gap appears to be **joint measurement across levels**. In particular, this search did not find a single design that simultaneously:

- estimates same-prefix final-answer branch distributions;
- measures readout and causal irreversibility on the same trajectories;
- treats prefix/token interventions as a downstream propagation process rather than a one-shot score;
- aligns perturbation effects across token time and layer depth;
- tests whether J-space/workspace transitions mediate high-leverage reasoning events;
- compares textual and matched activation interventions;
- first maps the phenomenon broadly across cheap black-box models and then explains selected cases mechanistically.

This is the unifying niche of the expanded repository.

## 13. Claims already too crowded to lead with

Avoid leading a paper with any of these by themselves:

- "we can predict correctness from hidden states";
- "the answer is decodable before CoT";
- "some reasoning tokens matter more than others";
- "activation steering changes reasoning";
- "continuous latent reasoning is possible";
- "a special prefix improves benchmark accuracy";
- "we patch activations at multiple CoT positions";
- "J-space contains silent reasoning."

The project becomes distinctive by **linking these observations into a causal temporal account** and by being disciplined about what each measurement establishes.
