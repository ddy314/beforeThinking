# Pre-registered pilot plan

## Research question

When do three operational signatures of answer commitment emerge, and when do
they disagree?

For a prompt `x`, a sampled reasoning trajectory `r`, checkpoint `t`, and final
answer `Y`, define:

- `T_read`: earliest checkpoint where a held-out, calibrated probe predicts the
  trajectory's final outcome above a registered threshold and remains above it;
- `T_branch`: earliest checkpoint where resampled continuations conditioned on
  `x + r[:t]` put a Wilson lower confidence bound above `tau` on the same modal
  answer at all later checkpoints;
- `T_irrev`: earliest checkpoint where registered, matched interventions fail
  to move final-answer probability by `delta` while maintaining coherence, at
  all later checkpoints.

These are reported separately. A composite `T_commit` will not be introduced
unless the three measures empirically agree under pre-specified tolerances.

## Pilot scope

- Model: `Qwen/Qwen3-1.7B`, BF16, PyTorch eager/Transformers.
- Tasks: 64 ARC-Challenge multiple-choice items and 64 GSM8K numeric items,
  sampled once with fixed IDs. MATH-500 enters only after parser validation.
- Base trajectories: 8 per item with the model-card sampling defaults.
- Prefix checkpoints: 0%, first thinking token, then 10/25/50/75/90% of the
  natural thinking trace. Absolute token position is retained alongside the
  normalized position.
- Branches: 8 suffixes per selected prefix in the pilot; increase only after a
  binomial precision and runtime audit.
- Hidden states: last token at `{25%, 50%, 75%, 100%}` layer depth, stored in
  float16 with model revision and tokenizer hash.
- Primary outcomes: exact answer class, correctness, modal mass, normalized
  entropy, switch probability, probe AUROC/Brier/ECE, intervention flip rate,
  and incoherence rate.

The bounded pilot is about plumbing and variance, not publication-level power.
At 128 items × 8 trajectories × 7 checkpoints × 8 branches, it already implies
57,344 branch continuations before interventions. The first smoke uses 8 items,
2 trajectories, 4 checkpoints, and 2 branches (128 continuations).

## Controls that are mandatory

1. Split train/test by `item_id`, never by rollout. Report GroupKFold and a
   leave-items-out test.
2. Compare hidden-state probes with prompt-only, token-position, trace-length,
   answer-prior, and surface-text baselines.
3. Run within-item label permutation and between-item permutation tests.
4. Exclude positions after an explicit answer string first appears, then report
   a separate leakage-inclusive analysis.
5. Preserve sampling seeds and use common random numbers for paired branch
   comparisons where the generation implementation permits it.
6. Record parse failures as failures, not silently drop them. Report results
   both with parse-failure as a class and on the parseable subset.
7. Score intervention coherence independently (perplexity/KL and rule-based
   truncation checks); an answer flip in broken text is not causal evidence.
8. Do not mix BF16 and quantized activation geometry in a primary comparison.

## Causal ladder

The project advances only when each cheaper rung works:

1. **Behavioral branching:** resample suffixes from exact prefixes.
2. **Semantic counterfactual:** replace one complete reasoning sentence with a
   same-item, alternative-answer sibling sentence matched for length.
3. **Residual patch:** patch a same-item sibling trajectory at one registered
   layer and checkpoint; sweep only 4 layer depths initially.
4. **Directional steering:** exploratory only, with orthogonal/random and norm-
   matched controls. It is not treated as a natural intervention.

## Decision gates

- Stop or redesign if answer parsing is below 98% on ARC or 95% on GSM8K.
- Stop the probe claim if it does not beat prompt-only and surface baselines on
  held-out items with bootstrap confidence intervals.
- Stop the “commitment” framing if branch estimates are too noisy or do not
  persist at later checkpoints; report trajectory stability instead.
- Do not start causal sweeps until at least 30 same-item pairs end in different
  answers, because matched alternative-answer patches otherwise lack support.
- Scale beyond the pilot only if two independent reruns reproduce the ordering
  of the three clocks and artifact hashes match.

## Expected outcomes

The most interesting plausible result is not universally early commitment, but
a phase diagram: easy/correct trajectories may show `T_read < T_branch <
T_irrev`, while hard or self-correcting trajectories show late, non-monotone, or
undefined times. A null result—probe confidence that fails same-item controls or
does not track branching—is also valuable because it exposes a common category
error in the current literature.

