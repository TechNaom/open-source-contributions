# US-001: Codespaces setup works out of the box

| | |
|---|---|
| Upstream issue | [langfuse/langfuse#18832](https://github.com/langfuse/langfuse/issues/18832) (opened 2026-10-15) |
| Repo | langfuse/langfuse |
| Branch | `fix/18832-devcontainer` in [TechNaom/langfuse](https://github.com/TechNaom/langfuse) |
| PR | not yet; waiting for a maintainer reply |
| Status | claimed |

## User story

As a new Langfuse contributor, I want the repo's Codespace to finish setup on its own,
so that I can run `pnpm run dx` without debugging the environment first.

## Problem

Found by us while setting up (see [../notes/codespace-setup.md](../notes/codespace-setup.md)):

1. `postCreateCommand` hangs on Corepack's "Do you want to continue? [Y/n]" prompt. Likely
   cause: the Dockerfile runs `corepack prepare` as `root`, but the Codespace user is
   `codespace`, whose Corepack cache is empty.
2. The image has no Rust, but `pnpm dev` builds the AI gateway and the worker compiles
   `packages/native`.

## Acceptance criteria

- [ ] A fresh Codespace finishes `postCreateCommand` with no prompt
- [ ] `cargo` is available in a fresh Codespace
- [ ] `pnpm run dx-f` brings up web + worker without manual installs

## Plan

- `.devcontainer/devcontainer.json`: `"containerEnv": { "COREPACK_ENABLE_DOWNLOAD_PROMPT": "0" }`
- Add `ghcr.io/devcontainers/features/rust:1`; the crates' `rust-toolchain.toml` still pins versions

## Test plan

- [ ] Create a new Codespace from the PR branch; confirm postCreate completes unattended
- [ ] `cargo --version` works; `pnpm run dx-f` reaches healthy web (3000) and worker (3030)

## What I learned

- Dev containers run build steps as root but sessions as a non-root user, so per-user caches
  (Corepack, npm, cargo) built in the image may not be visible at runtime.
- Langfuse's dev loop is Node + Rust: turbo runs Rust builds in a one-slot concurrency group,
  so the gateway, native addon and worker start one after another.
