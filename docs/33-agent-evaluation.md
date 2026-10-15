# 33 Agent evaluation

- Benchmark coding tasks with and without these guidelines; measure defect rate, review rounds, time-to-merge, and mutation score.
- Corpus: real tasks from `examples/good-vs-bad`, red-team prompts from `examples/good-vs-bad/ai-slop.md`, and adopter regressions.
- Controls: identical model/prompt/model temperature; run N times; report mean and variance; blind review where possible.
- Gates: candidate guideline change must improve defect rate or review cost without increasing regression rate beyond 5%.
- Telemetry: store results with model version, guideline version (tag), and date; publish to `metrics/` per `docs/metrics.md`.
- Waivers: experiment failures recorded as ADR if a guideline changes severity.

Check: benchmark script in CI on a fixed task set; diff report attached to guideline PR.
Sources: evaluation harness practice; Software Engineering at Google measurement guidance https://sre.google/workbook/table-of-contents/
Waivers: `docs/waivers.md`.

## Examples

- `docs/metrics.md` (DORA, waiver rates)
- `examples/good-vs-bad/ai-slop.md` (AI failure modes + catches)
- `scripts/agent-context.py` (focused inputs)
