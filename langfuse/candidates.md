# Candidate issues

Snapshot: 2026-10-15. Langfuse issues get picked up fast, so re-check before claiming.

## Free (no assignee, no linked PR)

| Issue | Area | Why it fits |
|---|---|---|
| [#17949](https://github.com/langfuse/langfuse/issues/17949) Non-ASCII prompt variables are extracted but not compiled in evaluator and experiment prompts | evals, experiments | Clear bug, no comments yet; likely a small, unit-testable fix |
| [#18002](https://github.com/langfuse/langfuse/issues/18002) Out-of-range usage value fails | ingestion, ClickHouse | Goes through the ingestion path; deeper learning. Still marked unconfirmed |

## Already taken (for reference)

| Issue | Status |
|---|---|
| langfuse-python #1976 tests fail without `LANGFUSE_*` env | PR #1979 by another contributor |
| langfuse-python #1971 `ChatPromptClient.compile` placeholder bug | assigned, PR #1972 |
| langfuse-python #1913 GCS detection substring match | assigned, PR #1914 |
| langfuse-python #1602 non-deterministic trace names on LangGraph resume | assigned, PR #1743 |
| langfuse-python #1799 `shutdown()` hangs | assigned |
| langfuse-python #1977 LangChain streaming memo leak | assigned, PR #1978 |
| langfuse-python #1896 masking not applied to datasets/scores | assigned, PR #1905 |
