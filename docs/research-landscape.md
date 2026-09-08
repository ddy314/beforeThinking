# Research landscape and novelty audit

Snapshot date: 2026-09-08. This is a scoped search of arXiv, author/project
pages, and released repositories, not a claim of exhaustive priority.

## Bottom line

The broad project proposed in `start.md` is already crowded. Early answer
decodability, forced answers at partial reasoning prefixes, correctness probes,
prefix regeneration, token/sentence interventions, and early stopping have all
been attempted. A paper that only plots `AUROC(t)` on GSM8K/MATH and calls the
first high-AUROC point “commitment” would be incremental and would overclaim
what a probe establishes.

The defensible opening is a within-question, multi-rollout study that measures
readout, behavioral branching, and causal reversibility together. The main
scientific object is the gap between those clocks, not another isolated probe.

## Who has tried what

| Work | What it establishes | What it does not establish for this project |
|---|---|---|
| Turpin et al., [Language Models Don't Always Say What They Think](https://arxiv.org/abs/2305.04388) (2023) | Biasing features can affect answers without faithful disclosure in CoT. | No tokenwise hidden-state/branch commitment clock for modern reasoning models. |
| Lanham et al., [Measuring Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2307.13702) (2023) | Truncation, corruption, and paraphrase tests operationalize causal dependence on CoT. | Not a joint activation-readout and same-prefix continuation study. |
| Lin et al., [Critical Tokens Matter](https://arxiv.org/abs/2411.19943) (2024) | Rollout contrast identifies tokens that disproportionately affect math success; token replacement and DPO can help. | “Critical” is not the same as a calibrated, persistent commitment time. |
| Bogdan et al., [Thought Anchors](https://arxiv.org/abs/2506.19143) (2025) | Sentence-level counterfactual rollouts, attention, and causal suppression find influential planning/backtracking steps. | Does not align answer-readout time, branch concentration, and irreversibility per trajectory. |
| Yamaguchi, Etheridge & Arditi, [Where Do Reasoning Models Refuse?](https://arxiv.org/abs/2507.03167) (2025) | Fixed and resampled CoT prefixes causally affect refusal; opening sentences can determine outcomes in distilled models. | Safety refusal is binary and structurally different from open-domain correctness. |
| Cox, Kianersi & Garriga-Alonso, [Decoding Answers Before Chain-of-Thought](https://arxiv.org/abs/2603.01437) (2026) | Pre-CoT residual-stream probes reach about 0.9 AUC on many tasks; steering flips over half of answers in their settings. | Primarily pre-CoT, not a tokenwise within-rollout commitment curve; decodability still need not imply irreversibility. |
| Boppana et al., [Reasoning Theater](https://arxiv.org/abs/2603.05488) (2026) | Compares activation probes, forced answers, and text monitors on DeepSeek-R1 671B and GPT-OSS 120B; easy and hard tasks differ; probe-guided exit saves tokens. | Frontier-scale evidence is not locally reproducible here and does not isolate same-item stochastic variation. |
| Zhao, [Entropy trajectory shape predicts LLM reasoning reliability](https://arxiv.org/abs/2603.18940) (2026) | Samples answers at intermediate steps; entropy-trajectory shape predicts correctness on GSM8K. | Diagnostic entropy is not combined with hidden readout or matched causal intervention. |
| Datta et al., [Large Language Models Decide Early and Explain Later](https://arxiv.org/abs/2604.22266) (2026) | Forced answer completion tracks answer switches; on Qwen3-4B answers change in 32% of queries and early stopping saves tokens. | A forced-answer prompt is a measurement intervention; it does not by itself identify latent state or irreversible commitment. |
| Mehrafarin, Parekh & Konstas, [When Chain-of-Thought Fails, the Solution Hides in the Hidden States](https://arxiv.org/abs/2604.23351) (2026) | Token-level activation patching on GSM8K finds recoverable solution information even in wrong traces. | Recovery from information-bearing states is not a full answer-distribution commitment analysis. |
| Iwase et al., [Reliable Chain-of-Thought via Prefix Consistency](https://arxiv.org/abs/2605.07654) (2026) | Regenerating suffixes from truncated prefixes predicts correctness and reduces self-consistency cost across models and tasks. | Uses prefix consistency as selection weight, rather than triangulating it with probes and answer-changing interventions. |
| Yuan et al., [Hidden Error Awareness](https://arxiv.org/abs/2605.09502) (2026) | Hidden states predict trace correctness early; within-problem controls reduce difficulty confounding; four attempted corrections fail. | Mostly error-vs-correct readout, not exact answer identity or a calibrated point of irreversibility. |
| Ri, Panigrahi & Arora, [Do Thinking Tokens Help with Safety?](https://arxiv.org/abs/2606.25013) and [code](https://github.com/princeton-pli/lrm_safety_deliberation) (2026) | First-thinking-token refusal probes reach 0.84–0.95 AUROC; nested prefix branching and sentence cuts show safety decisions often lock early. | Explicitly focuses refusal/compliance. Its authors identify general reasoning tasks and larger models as extensions. Full reproduction used H100-class compute and GPU-weeks. |
| Jo, [Committed Before Reasoning](https://arxiv.org/abs/2607.16451) (2026) | A carefully controlled Qwen3-8B case study exposes pre-commitment and important wording/oracle controls. | One minimal task and small activation samples cannot support a cross-task timing law. |

## What appears not to have been done together

No paper found in this search performs all of the following in one registered
design:

- multiple stochastic trajectories for every *same question*, with all splits
  grouped by question;
- exact-answer or answer-class readout at matched token positions;
- nested suffix branching from those same prefixes to estimate the conditional
  final-answer distribution;
- matched alternative-answer activation/text interventions at the same points;
- separate estimates of readout time, branch commitment time, and causal
  irreversibility time, including disagreement cases;
- cross-task comparison with difficulty calibrated *within model and task*;
- explicit controls for prompt-only difficulty, answer-token leakage, trace
  length normalization, intervention incoherence, and quantization.

This is a negative result of the scoped search, not proof that no unpublished or
unindexed work exists. A fresh search is required immediately before claiming
novelty in a paper.

## What we can and cannot claim

We can test whether a final outcome is linearly readable, whether continuation
distributions concentrate, and whether specified interventions change those
distributions. We can compare these operational times across sampled models,
tasks, and difficulty bands.

We cannot infer that the model “already knew” an answer from probe AUROC alone;
prove that natural-language CoT is wholly post-hoc; identify a unique internal
decision variable; generalize from 1.5–1.7B local models to frontier systems; or
prove metaphysical claims about whether a model is “really thinking.” Activation
patches and forced-answer prompts are interventions with their own distribution
shift, not transparent windows into an untouched process.

## Opportunity assessment

| Direction | Assessment | Reason |
|---|---|---|
| Reproduce first-token correctness AUROC only | Low value | Directly overlaps several 2026 papers. |
| Define one `T_commit` from probe confidence | Invalid as stated | Conflates decodability with causal commitment and depends on probe calibration. |
| Triangulate three clocks on same trajectories | Promising | Directly tests where established methods agree and, more importantly, disagree. |
| Build an early-exit system | Moderate, secondary | Already demonstrated; useful only if disagreement-aware timing improves the accuracy/compute frontier. |
| Large cross-family sweep | Not locally realistic | 8 GB VRAM forces small models, quantization, or remote compute. |
| Full token-by-token activation patching | Not a first pilot | Compute scales with layers × positions × sources × continuations. |
| Small registered pilot on Qwen3-1.7B | High feasibility | BF16 weights fit; sequential branch sampling and selected layers/positions are tractable. |

