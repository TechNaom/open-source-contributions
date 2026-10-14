**Title:** bug(devcontainer): Codespaces setup hangs on a Corepack prompt, and Rust is missing

### What happened

I created a GitHub Codespace from `main` (8d7a8f77c, 2026-10-14) on a 4-core / 16 GB machine using the repo's `.devcontainer`. Two things blocked `pnpm run dx` from working out of the box:

**1. `postCreateCommand` hangs forever.** `cp .env.dev.example .env && pnpm i` stops at:

```
! Corepack is about to download https://registry.npmjs.org/pnpm/-/pnpm-12.8.2.tgz
? Do you want to continue? [Y/n]
```

Nobody can answer the prompt during creation, so `pnpm i` never runs. The likely cause: the Dockerfile runs `corepack prepare pnpm@12.8.2 --activate` at build time as `root`, but the Codespace runs as the `codespace` user, whose Corepack cache is empty, so Corepack downloads pnpm again and asks first.

**2. No Rust toolchain.** `cargo` and `rustup` aren't in the image (`mcr.microsoft.com/devcontainers/universal:6-noble`), but CONTRIBUTING.md lists Rust as a requirement: `pnpm dev` builds the AI gateway, and the worker build compiles `packages/native`. I had to install rustup by hand before the worker would start.

### Workaround I used

```bash
export COREPACK_ENABLE_DOWNLOAD_PROMPT=0 && pnpm install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
pnpm run dx-f   # then `pnpm run dev` again after the documented first-run failure
```

After that, the full stack came up (web, worker, Postgres, ClickHouse, Redis, MinIO) with the seeded demo project.

### Suggested fix

- `.devcontainer/devcontainer.json`: add `"containerEnv": { "COREPACK_ENABLE_DOWNLOAD_PROMPT": "0" }`, so the postCreate install can't block on a prompt.
- Add Rust to the image, e.g. the `ghcr.io/devcontainers/features/rust:1` feature in `devcontainer.json`. The crates' own `rust-toolchain.toml` files would still pick the exact toolchain.

I'm happy to open a small PR with both changes if that sounds right to you.
