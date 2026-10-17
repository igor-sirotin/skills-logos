---
name: bumping-a-logos-module-backend
description: 'Use when bumping the library "backend" a Logos Core module wraps — logos-delivery in logos-delivery-module, logos-chat (libchat) in logos-chat-module — to latest master/main or to a given commit/tag, reviewing every upstream commit in the range and applying the matching module-side changes, then opening a draft PR. Keywords: bump logos-delivery, bump libchat, bump logos-chat, update backend, flake.lock bump, Cargo rev bump, upstream diff review.'
---

# Bumping a module's backend library

Default target is the tip of the library's default branch. Use a commit or tag only if the user gives one.

## Backends

| Module | Library | Where the pin lives | How to bump |
|---|---|---|---|
| `logos-co/logos-delivery-module` | `logos-messaging/logos-delivery` (branch `master`) | `flake.nix` input `logos-delivery` (`git+https://…?submodules=1`), locked in `flake.lock` | `nix flake update logos-delivery`. For a specific rev: `nix flake lock --override-input logos-delivery 'git+https://github.com/logos-messaging/logos-delivery?submodules=1&rev=<sha>'` |
| `logos-co/logos-chat-module` | `logos-messaging/logos-chat` (formerly `libchat`; the Cargo URL still says `libchat.git`) | `rust-lib/Cargo.toml`: the same `rev = "<sha>"` on every libchat-repo crate (`logos-generic-chat`, `libchat`, `logos-account`, …) | Replace the rev on **all** of them, then run `cargo update` for those packages to refresh `rust-lib/Cargo.lock` |

Bump only the backend. Leave other pins (`nim-ffi`, `logos-rln-modules`, `logos-module-builder`, …) alone.

If a module has no row here, read its `flake.nix` and manifest to find the pin, and add a row.

## Workflow

1. **Isolate.** Call `EnterWorktree` first. Put scratch work in `$CLAUDE_JOB_DIR/tmp`.
2. **Get the range.** Clone the library into scratch. Read the current rev from the lock/manifest and resolve the target rev. Then run `git -C <clone> log --oneline <old>..<target>`.
3. **Triage every commit.** Run `git show --stat` on each one, then read the diff of anything outside tests/CI. Commit bodies are often empty, so judge from the diff, not the title. Put each commit in one bucket:
   - **API/ABI:** the public header (`library/liblogosdelivery.h`, libchat's public crate API), FFI exports, CBOR/JSON schemas, event names and payloads.
   - **Config:** new, renamed or removed keys, and changed defaults (e.g. a transport turned on by default, or a port that now follows another port).
   - **Plugin contracts** the module implements (e.g. the RLN plugin in `rln_lez/`): the ops, the wire format, the library's timeouts, and how often an op is called.
   - **Behaviour the module documents:** event ordering and terminal states, or when an event fires.
   - **Nothing:** tests, CI, upstream docs, internal refactors, dependency bumps with no API change.
4. **Map each non-"Nothing" commit onto the module.** Grep the module for the symbol, key or event. Check each of these places:
   - The plugin source (`src/*.cpp|h`, `rust-lib/src`) and its API doc comments.
   - Test stubs and mocks that mirror the library header (`tests/stubs/`, `tests/mocks/`).
   - `conf/*.json`, `docker-compose.yml` (a new listening port or protocol needs a port mapping), and `docs/pages/*`.
   - `metadata.json` (libraries, packages).
5. **Apply the changes.** Code changes come first. Doc changes are **one or two lines** each and cover only what a module user sees. Don't restate upstream internals or preset contents; those belong upstream.
6. **Bump the pin** (see the table), then run `git diff --stat` on the lock.
7. **Build and test in the background.** A new liblogosdelivery rev usually builds from source on aarch64, which takes a long time.
   - delivery: `nix build .#default .#checks.<system>.unit-tests .#lgx-portable -L --no-link`
   - chat: `nix build .#chat_module -L` plus its checks.
   - Report the test count from the log.
8. **Commit, push and open a draft PR.**
   - Branch: `chore/bump-<library>-<short-sha>`.
   - Title: follow the repo's style, e.g. `chore(nix): bump logos-delivery to master <short-sha>`.
   - Body: follow the `writing-pr-descriptions` skill. Keep it to about 4 numbered items. Reference upstream PRs cross-repo (`logos-messaging/logos-delivery#4337`); a bare `#N` links into the module repo.
   - Put in the collapsed "AI-made decisions" block: the commits that needed nothing, and any pre-existing problem you saw but left alone.

## Gotchas

- The worktree isolation guard rejects `cd <dir> && git …`, loops over git, and `eval`. Use `git -C <path>` with literal arguments, or write the loop to a script file in `$CLAUDE_JOB_DIR/tmp` and `bash` it.
- `gh pr edit` fails because the token lacks `read:org`. Update the body with `gh api -X PATCH repos/<owner>/<repo>/pulls/<n> -F body=@<file>`.
- No Claude attribution in commits or PR bodies.
- Keep the report short. List the commits that needed module changes and name the ones that didn't.
