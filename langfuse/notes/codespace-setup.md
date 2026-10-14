# Running Langfuse in GitHub Codespaces

Fork: [TechNaom/langfuse](https://github.com/TechNaom/langfuse). Codespace `langfuse-dev`
(4-core, 16 GB, 32 GB disk, 30 min idle timeout). First set up 2026-10-15.

## First-time setup (what actually worked)

| Step | Command | Gotcha |
|---|---|---|
| Create | `gh codespace create -R TechNaom/langfuse -b main -m standardLinux32gb --idle-timeout 30m` | `gh` needs the `codespace` scope: `gh auth refresh -h github.com -s codespace` |
| Install packages | `export COREPACK_ENABLE_DOWNLOAD_PROMPT=0; pnpm install` | The devcontainer's `postCreateCommand` hangs forever on Corepack's "Do you want to continue? [Y/n]" prompt |
| Rust | `curl -sSf https://sh.rustup.rs \| sh -s -- -y --profile minimal` | Not in the devcontainer image, but the worker's native addon and the AI gateway need it |
| Start everything | `pnpm run dx-f` | Non-interactive version of `dx`; resets the local DBs and seeds demo data |
| Retry dev | `pnpm run dev` | First run fails with `Can't resolve '@langfuse/shared/src/server'` (documented "fails on the very first run"); the second run works |

Rust builds share one slot, so the AI gateway compiles first, then the native addon, then
the worker starts: about 10 minutes the first time. Disk goes from 7.6 GB free to about
4 GB free after the builds.

## Daily use

```bash
cd /workspaces/langfuse && source ~/.cargo/env && pnpm run dev   # databases restart with the codespace
```

Open it locally (login only works on the exact `NEXTAUTH_URL`, http://localhost:3000):

```powershell
gh codespace ports forward 3000:3000 -c langfuse-dev-69vrrrpqvw9pfrv9j
```

Then http://localhost:3000, user `demo@langfuse.com` / `password`.

| Check | Command |
|---|---|
| Web | `curl localhost:3000/api/public/health` |
| Worker | `curl localhost:3030/api/health` |
| Containers | `docker ps` |
| ClickHouse | `docker exec -it langfuse-clickhouse clickhouse-client --user clickhouse --password clickhouse` |

Seeded demo data: 7,246 traces, 101,547 observations, 67,229 scores.
