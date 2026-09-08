# Black-box cross-model sweep

## Purpose

Mechanistic experiments are expensive and model-specific. BeforeThinking therefore uses a two-stage strategy:

1. **black-box breadth** — test whether a phenomenon exists across many models using only generated outputs and repeated continuation;
2. **white-box depth** — select a few representative open-weight models for hidden-state and causal analysis.

A unified API service such as OpenRouter is useful for stage 1 because it exposes many models behind a common request format and makes small-model sweeps inexpensive. The black-box sweep is not a substitute for mechanistic evidence; it is a discovery and external-validity layer.

## 1. Questions suitable for API-only experiments

API access is enough to study:

- forced-prefix and first-token effects;
- sensitivity to specific reasoning openings or style templates;
- prefix truncation curves;
- branch entropy from repeated continuations;
- answer-switch frequency;
- continuation consistency from exact textual prefixes when the API allows assistant-prefix continuation or equivalent prompt reconstruction;
- CoT sentence replacement and paraphrase effects;
- position effects of the same intervention;
- temperature and sampling sensitivity;
- scaling across model size/family/post-training style;
- cross-model transfer of a prefix discovered on one model;
- whether effects persist across providers serving nominally the same model.

API-only experiments cannot directly establish neuron-, feature-, residual-, J-space-, or head-level mechanisms.

## 2. Model panel design

Do not choose models only because they are popular. The panel should cover contrasts that test hypotheses.

### Size axis

Include several very small models where possible (sub-1B, ~1–2B, ~3–4B), plus a few larger models as reference points. The exact panel should be recorded from the provider catalog at run time because availability and pricing change.

### Training axis

Where possible compare:

- base vs instruction-tuned;
- ordinary instruct vs explicit reasoning/RL variants;
- distilled reasoning models vs their base family;
- dense vs MoE models;
- same-family neighboring sizes.

### Family axis

Include multiple independent families so a model-specific prompt artifact is not mistaken for a general reasoning law.

### Provider axis

For models served by multiple providers, either pin a provider or record the provider returned for every request. Hidden system prompts, quantization, kernels, and serving defaults can create apparent model effects.

## 3. Core experiment A: prefix susceptibility scan

For each `(model, item)` obtain a baseline sample set and treatment sample sets.

Treatments should include:

- exact candidate prefix;
- semantic paraphrase;
- style-matched but task-neutral prefix;
- token-count-matched filler;
- punctuation/filler control;
- truncated prefix lengths;
- position-shifted prefix;
- random token sequence with tokenizer-aware length matching.

Primary estimands:

\[
ATE_m = \mathbb E_i[\operatorname{score}(Y_{i,m}^{\delta})-\operatorname{score}(Y_{i,m}^{0})],
\]

with paired bootstrap over items, and

\[
\Delta H_m = \mathbb E_i[H(B_{i,m}^{\delta})-H(B_{i,m}^{0})],
\]

where `B` is the empirical final-answer distribution from repeated samples.

A prefix is interesting mechanistically only if its effect survives basic parsing and lexical controls and reproduces on enough items to support white-box follow-up.

## 4. Core experiment B: perturbation propagation from text alone

Even without hidden states, downstream propagation can be estimated from generated text.

Given a base trajectory and an intervention at source `s`, repeatedly regenerate suffixes at checkpoints `t>s`. Compare:

- answer distribution;
- semantic continuation embedding distribution (using a fixed external encoder, if desired);
- sentence/function-tag distribution;
- rate of planning/backtracking/self-correction markers;
- normalized suffix length;
- next-step answer confidence when a task permits it.

This gives a behavioral approximation to the perturbation-response kernel before local mechanistic analysis.

## 5. Core experiment C: transfer matrix

If prefix `p_a` is discovered on source model family `a`, evaluate it on model family `b` and construct

\[
M_{ab}=\text{effect of prefix discovered on family }a\text{ when applied to }b.
\]

Interpretation:

- strong diagonal, weak off-diagonal: likely model/family-specific training artifact;
- broad transfer: likely semantic/control strategy with cross-family validity;
- size-dependent transfer: possible emergence or post-training interaction;
- provider-dependent transfer: serving/API confound requiring caution.

## 6. Core experiment D: first-token / first-sentence intervention

For reasoning models whose visible reasoning can be controlled, compare:

1. natural generation;
2. forced first token only;
3. forced first 2/4/8 tokens;
4. forced first full sentence;
5. sibling-rollout prefix transplant;
6. matched random/filler controls.

Measure the marginal treatment effect as prefix length grows. A sharp gain at one or two tokens is qualitatively different from a smooth effect proportional to the amount of supplied reasoning.

## 7. Remote reproducibility manifest

Every request record should include at minimum:

- timestamp;
- API service;
- public model slug;
- provider/routing result when exposed;
- model/version metadata when exposed;
- full system/user/assistant message payload after templating;
- temperature, top-p, top-k if applicable;
- seed if supported;
- maximum output tokens;
- reasoning/thinking budget parameters if exposed;
- tool availability disabled/enabled state;
- returned usage counts;
- finish reason;
- raw response;
- parser output;
- retry count and error metadata;
- local code commit.

Never silently merge responses produced by different provider routes into one mechanistic condition.

## 8. Cost accounting

Avoid hard-coding provider prices into scientific documents because they change. At experiment launch, snapshot the provider's published price table and save it as an artifact.

For model `m`, approximate request cost as

\[
C_m = N_{in}\,p_{in,m}/10^6 + N_{out}\,p_{out,m}/10^6,
\]

and total sweep cost as the sum over requests plus any platform fee. Report observed token usage rather than multiplying only configured `max_tokens`.

The scientific optimization target is **information per dollar**, not the cheapest model. A slightly more expensive endpoint with stable routing and fewer failed requests can be a better experimental instrument.

## 9. Request-volume planning

Large factorial designs explode quickly. For example,

`models × items × prefixes × temperatures × repetitions`

can exceed tens of thousands of calls even with small values. Use a funnel:

### Discovery pass

- 5–10 models;
- 30–100 items;
- 4–8 prefix/control conditions;
- 2–4 repetitions.

### Confirmation pass

Keep only effects that survive paired uncertainty intervals and parser checks. Increase repetitions and item count for those conditions.

### Mechanistic handoff

Choose 1–3 open-weight models with:

- a robust effect;
- local feasibility;
- sibling rollouts ending in different answers;
- reasonable tokenizer/model-family correspondence to the black-box condition.

## 10. Statistics

Because repeated generations from the same item are not independent, use hierarchical or clustered uncertainty estimates.

Recommended minimum:

- paired bootstrap by item;
- mixed-effects logistic regression for binary correctness when sample size permits;
- beta-binomial or hierarchical binomial models for per-item branch proportions;
- false-discovery correction for large model × prefix grids;
- effect sizes and confidence intervals, not only p-values.

Avoid treating each rollout as an independent datapoint in a naive t-test.

## 11. Benchmark panel

Use tasks that expose different branch structures:

- ARC-Challenge: discrete answer classes, cheap parsing;
- GSM8K: numeric reasoning and self-correction;
- MATH-500: harder multi-step reasoning after parser validation;
- logical deduction / BBH-style tasks: explicit branch/planning structure;
- code micro-tasks: useful later if execution-based scoring is added.

For prefix-specific phenomena, include a small non-reasoning control task so a global verbosity/style effect is not mislabeled as reasoning improvement.

## 12. Relationship to local experiments

The black-box sweep should generate hypotheses, not consume the entire research budget. Its most valuable output is a table like:

| phenomenon | families where observed | effect size | control survival | local model available? | mechanistic priority |
|---|---:|---:|---:|---:|---:|
| early forced-prefix gain | ... | ... | ... | ... | ... |
| branch entropy collapse | ... | ... | ... | ... | ... |
| first-sentence leverage | ... | ... | ... | ... | ... |
| self-correction sensitivity | ... | ... | ... | ... | ... |

White-box work then asks why the strongest and most representative rows occur.

## 13. Failure modes

- model slug silently changes backend behavior;
- API rejects or rewrites assistant prefills;
- hidden reasoning is unavailable, making conditions incomparable;
- safety/system layers interact with the prefix;
- provider rate limiting changes sampling schedule;
- retries selectively preserve easy prompts;
- answer parser creates artificial gains;
- model retirement breaks exact replication.

These are reasons to preserve raw responses and metadata from the first run.

## 14. Scientific role

The OpenRouter/API component gives BeforeThinking something a single-GPU mechanistic project normally lacks: **breadth across many independent model families at low cost**. The local model then supplies causal/mechanistic depth. The strongest final papers will use each where it is most defensible rather than pretending that one access mode can answer every question.

Snapshot: 2026-09-08.
