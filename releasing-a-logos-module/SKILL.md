---
name: releasing-a-logos-module
description: "Use when cutting a release of a Logos Core module or UI — logos-delivery-module, logos-delivery-demo, logos-chat-module, logos-chat-ui — bumping metadata.json, pinning dependent modules, tagging vX.Y.Z, or writing/rewriting the GitHub release notes for one. Keywords: release, release notes, cut a release, publish a release, gh release create, tag, version bump, metadata.json version, logos-modules-release."
---

# Releasing a Logos module

Covers `logos-co/logos-delivery-module`, `logos-co/logos-delivery-demo`, `logos-co/logos-chat-module`, `logos-co/logos-chat-ui`. All four release the same way: a prepare-release PR, a lightweight tag on the merged commit, and a hand-written GitHub release.

**The release notes are the deliverable.** They are read by module consumers who never see the diff — app developers pinning the module, the Logos Core team, Status. Write for someone deciding whether to upgrade and what breaks when they do.

## Versioning

`0.<testnet>.<patch>` — see [`docs/versioning.md`](https://github.com/logos-co/logos-delivery-module/blob/master/docs/versioning.md) in logos-delivery-module (the policy is shared; only that repo carries the doc).

- MAJOR is fixed at `0` — the API is not stable, breaking changes land in any release.
- MINOR tracks the Logos testnet number this release targets. Bumping it resets PATCH.
- PATCH increments for every release against the same testnet.

A breaking change does **not** bump MINOR. `0.2.0` dropped `version()` from the delivery module's API and was still a MINOR bump only because it was the first release for Testnet 2.

## Procedure

1. **Collect the changes.** `git log --oneline <last-tag>..master` and `gh pr list --state merged --search "merged:>=<date of last tag>"`. Every release-note bullet cites the PR that made it, so work from merged PRs, not raw commits.
2. **Prepare-release PR.** Bump `"version"` in `metadata.json`, and move any module dependency pins onto the release tags this version ships against:
   - `flake.nix` inputs (`logos-delivery-module.url = "github:logos-co/logos-delivery-module/v0.2.0"`), plus `flake.lock`.
   - chat_module also: `rust-lib/Cargo.toml` / `Cargo.lock`, and the hand-maintained contract copies `rust-lib/*.lidl`, `rust-lib/deps/*.lidl`.
   - chat_ui follows chat_module's delivery pin rather than pinning delivery itself — keep it that way, so the whole stack resolves one delivery rev.
   - Title: `chore: release vX.Y.Z` when nothing but the version moves; `build: prepare X.Y.Z against <dep> vA.B.C` when dependency pins move with it.
3. **Draft the release** before merging: `gh release create` is fine as a draft with no tag; put the draft link in the PR body ("publish after merge").
4. **Merge, then publish.** The tag is a lightweight tag GitHub creates at publish time on the merge commit — publish the draft with the tag `vX.Y.Z` and target `master` rather than tagging by hand. Verify the tag landed on the release commit.
5. **Downstream, in lockstep.** delivery_module → chat_module and logos_delivery_demo; chat_module → chat_ui. A downstream release that only moves its pin is still a real release with its own notes (see chat-ui v0.2.2 below).
6. **`logos-co/logos-modules-release`.** Open a PR bumping the submodule pointers to the new release commits — this is what actually ships the modules to hosts. `logos-delivery-demo` is in it too (`submodules/logos-delivery-demo`). After merge, publish with `gh workflow run release-<repo>.yml -R logos-co/logos-modules-release`.

## Release-notes format

A short lead paragraph (one or two sentences, optional for delivery repos, used in the chat repos) saying what this release is *for*, then `###` sections. Include only the sections that have content, in this order:

| Section | Use |
|---|---|
| `### Features` | New capability a consumer can call or see. |
| `### Breaking changes` | Anything a consumer must change to upgrade. Name what was removed and what replaces it. |
| `### Behavior changes` | Same API, different behaviour — defaults, ports, paths, what a call now does. |
| `### Fixes` (or `### Fixes & robustness`) | Bugs fixed. |
| `### Contract` | Chat repos only: the API-contract delta in prose, when `init`/records/methods changed shape. |
| `### Changes & dependencies` | Dependency pins, toolchain moves, build-system changes. |
| `### Upgrading <dep>` | The bundled or pinned upstream moved: highlights plus a compare link. |
| `### Compatibility` | What to install this alongside — used by chat_ui, which is meaningless on its own. |
| `### Docs` | Guides added or reworked. |
| `### Tests & CI` (or `### Tests & docs`, `### Build & CI`) | Doc-tests, e2e suites, CI. |

Close with a horizontal rule and `**Full changelog:** https://github.com/<org>/<repo>/compare/<prev>...<new>` when the compare is worth linking; a release whose notes already name every PR may omit it.

### Bullet style

- **Every bullet ends with the PR reference in parentheses** — `(#79)`, or `(#61, #62)` when several PRs made it. Same-repo PRs as `#N`; cross-repo as a full URL (`logos-messaging/logos-delivery#4074`).
- **Feature bullets lead with a bolded imperative clause**, then the detail: `**Store instance state under the host-assigned persistence path** (#51). The module writes under the directory its host assigned it…`. Fix and dependency bullets are plain one-liners.
- **Write from the consumer's side.** Say what the module now does, what a caller passes, what an event now carries. Not which file changed, not which function was refactored.
- **A behaviour or dependency bullet carries its consequence when the consumer must act on it**: "legacy flat configs now get upstream's fixed defaults (`tcpPort` 60000, …) — pin ports explicitly or use the layered shape". Otherwise keep it to a line.
- Method and field names in backticks. Config shapes as inline JSON when short.
- Present tense, no "we", no "this PR".

### The `Upgrading <dep>` section

When the release carries a new bundled node or module pin, list only the highlights a consumer would notice — metrics renames, transports, reliability behaviour — grouped by theme, each linking its upstream PR. Then always give the full compare link:

```
All logos-delivery changes: https://github.com/logos-messaging/logos-delivery/compare/<old-sha>...<new-sha>
```

If nothing behavioural moved, say so in one line and give the compare link anyway ("Most changes are around project structure and CI improvements, no behavioural changes are expected").

## Hard rules

- **No Claude session links, no "Generated with Claude Code", no `Co-Authored-By: Claude`** — release notes, release PRs and release commits are all public. See the global rule in CLAUDE.md. (Earlier releases carry these; do not copy them forward.)
- **Do not paste `gh`'s auto-generated notes.** These notes are written, not generated.
- **No section for what didn't change**, no "Known issues" invented from speculation, no upgrade instructions beyond the pin.
- **Do not narrate the diff.** No file lists, no per-function catalogues, no refactors that a consumer cannot observe.
- A release with nothing but a dependency bump still gets a lead sentence and a `Changes & dependencies` section — never an empty body.
- **Show the notes to the user before publishing.** Publishing a release is outward-facing and irreversible in practice.

## Reference releases

Read these before writing; they are the house style.

- [delivery-module v0.2.0](https://github.com/logos-co/logos-delivery-module/releases/tag/v0.2.0) — the full-shape release: features, breaking, behaviour, fixes, `Upgrading logos-delivery`, docs, CI.
- [chat-module v0.2.1](https://github.com/logos-co/logos-chat-module/releases/tag/v0.2.1) — bolded feature clauses and a `Contract` section for an API reshape.
- [chat-ui v0.2.2](https://github.com/logos-co/logos-chat-ui/releases/tag/v0.2.2) — a pin-only release, with `Compatibility`.
- [delivery-demo v0.2.0](https://github.com/logos-co/logos-delivery-demo/releases/tag/v0.2.0) — a consumer app tracking a module release.
