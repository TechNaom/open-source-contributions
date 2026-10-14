# Langfuse

Open-source LLM engineering platform: tracing, evals, prompt management and datasets.
I use it in production for my LinkedIn branding pipeline, so this is learning the internals
of a tool I depend on.

## Repos

| Repo | Stack | Fork | Local checks |
|---|---|---|---|
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | Next.js 16, tRPC, Prisma, Postgres, ClickHouse, Redis, S3, Rust | not yet (GitHub Codespaces for the full stack) | `pnpm run lint`, `pnpm tc`, `pnpm exec knip`, `pnpm run test` |
| [langfuse/langfuse-python](https://github.com/langfuse/langfuse-python) | Python, OpenTelemetry, Pydantic, Fern-generated client | [TechNaom/langfuse-python](https://github.com/TechNaom/langfuse-python) | `uv run --frozen ruff check .`, `mypy langfuse`, `pytest tests/unit` |

Issues for **all** Langfuse repos, the Python SDK included, are tracked in `langfuse/langfuse`.

## Contribution rules (from their CONTRIBUTING.md)

- Open or comment on an issue **before** a significant change; undiscussed changes may be rejected.
- Sign the CLA once. Commit author email must match the GitHub account.
- Conventional commits (`fix(sdk): ...`); PRs are squash-merged; split large changes into stacked small PRs.
- Bug fixes: write the failing test first, confirm it fails, then fix.
- Don't hand-edit generated code (`langfuse/api/` in the SDK, Fern output in the main repo).
- AI-assisted work is fine; the human author owns the PR, understands the change, and posts the proof.

## Pages

- [notes/architecture.md](notes/architecture.md): how the system works
- [candidates.md](candidates.md): issues being considered
- [user-stories/](user-stories/): one file per contribution
