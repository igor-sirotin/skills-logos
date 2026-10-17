---
name: writing-logos-messaging-journey
description: Use when someone on Logos Messaging needs to write a "Journey" doc packet for the docs team and file it via the logos-docs doc-packet.yml issue template — a structured request describing a λChat / libchat / Waku / SDS user journey (run a node, send a message, sync, etc.) on local/devnet/testnet. Keywords: journey, doc packet, doc-packet.yml, logos-docs, documentation request, type:journey, SME packet, happy path.
---

# Writing a Logos Messaging Journey Doc Packet

## Overview

A **Journey doc packet** is the structured intake an R&D SME fills out so the Logos Docs team can write a user-journey page. You provide outcome, scope, the exact happy path, verification, config, and a point of contact; Docs drafts the page; the **Red Team runs the journey end-to-end** in a clean environment; you review the draft on the PR.

**Core principle: every command, output, config value, and handle in the packet must be verified against live repo state or a human — never guessed, never a placeholder.** Docs writes the page verbatim from your packet and the Red Team executes it on a clean box. A wrong command or stale endpoint ships a broken published page with your team's name on it. An empty required field ships a stub with a public "gap" flag.

Template (GitHub Issue Form): `logos-co/logos-docs` → `.github/ISSUE_TEMPLATE/doc-packet.yml`. Markdown equivalent for assembly: `resources/templates/doc-packet.md`.

## The Discipline (read first)

Two hard rules. Both failed in baseline testing.

**1. Never file the issue until the requester says go.** Filing opens a public issue on `logos-co/logos-docs` and starts Docs-team work — an outward-facing write. Draft the packet, show it to the requester, and submit only on an explicit go-ahead. A baseline run filed the issue unprompted.

**2. Verify, don't guess — especially the path and the POC.** The happy path must be the *real* journey, executed/traced in the actual repos, not a plausible substitute or an in-process demo. The point-of-contact (GitHub + Discord) is a person's identity: **ask the requester**, never infer it from commit counts or fill a placeholder. A baseline run guessed the Discord handle and admitted it couldn't verify it.

### Red flags — STOP

- About to run `gh issue create` / open the form without the requester's explicit go-ahead.
- Writing a POC handle you didn't get from a human ("placeholder", "worth correcting later", guessed from `git shortlog`).
- Featuring an **in-process / two-clients-in-one-binary demo** (e.g. `pingpong.nim`) for a journey titled "run a **node** … on **devnet**". A node journey runs a real node against the network.
- Copying devnet config (cluster id, shards, bootstrap peers) from the **client** repo without confirming it against the **transport** repo's devnet preset (`logos-delivery`).
- Featuring the raw delivery/Waku demo for an **"end-to-end encrypted"** journey — payload E2E encryption lives in **libchat**, not the bare transport.
- Using `logos-delivery-compose` for "devnet" — it joins cluster-id 1 (The Waku Network, RLN-gated), not devnet.
- Leaving any **required** field blank to "let Docs fill it in" — that publishes a stub with a public gap flag.

### Rationalization table

| Excuse | Reality |
|--------|---------|
| "It's basically ready, I'll just file it." | Filing is a public write that starts Docs work. Get the go-ahead first. |
| "I'll put a placeholder POC and fix it later." | Docs picks it up before you fix it. A required identity field is asked of a human, not invented. |
| "pingpong/the example demo proves the journey." | An in-process demo isn't "run a node on devnet." Feature the path the user actually runs. |
| "The client repo's config is the devnet config." | The client repo may carry stale ENRs/shards. The `logos.dev` preset in `logos-delivery` is the source of truth. |
| "The commands look right." | Docs publishes them verbatim and Red Team runs them clean. "Looks right" ships broken pages. Trace them in the repo. |
| "Docs will fill the blanks." | Blank required field → published stub + public gap flag, not a quiet TODO. |

## Procedure

1. **Confirm scope with the requester:** the one-sentence outcome, the runtime target (`local` / `devnet` / `testnet v0.1` / `testnet v0.2`), and **who the POC is** (GitHub + Discord). Don't guess any of these.
2. **Pick the path that matches the journey.** Match the title to the real flow: a "node on devnet" journey runs a real node; an "end-to-end encrypted" journey uses **libchat** (E2E lives there, not in bare transport). When unsure which client/binary, confirm with the requester.
3. **Gather + verify each field against live repos** (see field guide). Pin the repo to a branch/tag/commit SHA. For devnet config, read the **`logos-delivery` `logos.dev` preset** (cluster id, auto-sharding, bootstrap multiaddrs), not just the client's hardcoded values. Where you can, actually run the happy path or trace it command-by-command in the repo.
4. **Assemble the packet as markdown** following `resources/templates/doc-packet.md` (same sections/order as the form). Fill **all 11 required** fields; fill the optional 6 when you have verified content.
5. **Review with the requester.** Show the full draft. Flag any value you could not fully verify so they can confirm or correct it.
6. **Submit only on explicit go-ahead** (see Submission). Then the requester reviews the Docs draft on the PR.

## Field guide

Required fields (form `id` → what to put). Leaving a required field blank publishes a stub.

| Field id | What to put | Messaging notes / where to verify |
|---|---|---|
| `outcome` | One sentence: the end state. | "The user has a running λChat node and has sent an encrypted message on devnet." |
| `why-it-matters` | 1–2 sentences: what it enables/proves. | — |
| `key-components` | 2–5 components, one sentence each + how they relate. | Logos Chat SDK (`logos-chat`), `libchat` (E2E session/encryption), Waku transport (`logos-delivery`), SDS reliability (`nim-sds`), `chat_proto`. |
| `repo` | URL + branch/tag/**commit SHA**. | Pin a SHA; verify it's pushed. Multiple repos → one per line. |
| `runtime-target` | One of: `local` / `devnet` / `testnet v0.1` / `testnet v0.2`. | Must match the dropdown exactly. |
| `prerequisites` | OS, hardware, tools+versions, keys/tokens. | Note if no accounts/keys needed (ephemeral node key). |
| `happy-path` | Exact commands clean→working, expected output after each major step. | A copy-pasted real terminal session is ideal. Trace it in the repo; don't approximate. |
| `success-command` | One command/action proving completion. | e.g. a `/status` or REST `info` call. |
| `expected-result` | What the user sees from the success command. | Paste real output. |
| `poc-github` | GitHub handle of the R&D POC. | **Ask the requester.** Don't infer. |
| `poc-discord` | Discord handle of the R&D POC. | **Ask the requester.** Don't placeholder. |

Optional (improve quality, fill when verified): `config` (env vars, flags, config keys + example values, ports/endpoints — pull devnet values from the `logos-delivery` preset), `troubleshooting` (top-3 failure modes: symptom/cause/fix + out-of-scope items), `existing-docs`, `hardware`, `time-estimate`, `security-notes` (ephemeral keys, intro-bundle secrecy, data-loss/irreversible actions).

## Messaging resource map

GitHub org `logos-messaging` (transport/protocol) and `logos-co` (docs, umbrella):

- `logos-chat` — Logos Chat / λChat client SDK (Nim).
- `libchat` — E2E session & encryption library (X3DH / Double Ratchet / MLS); ships the `chat-cli` binary. **Required for "encrypted" journeys.**
- `logos-delivery` — Waku/messaging transport in Nim; holds the **`logos.dev` devnet preset** (bootstrap multiaddrs, cluster id, sharding). Source of truth for network config.
- `nim-sds` — Scalable Data Sync (e2e reliability protocol).
- `chat-store`, `chat_proto` — store, protobufs.
- `logos-delivery-compose` — nwaku docker-compose for **The Waku Network (cluster 1)**, not devnet. Don't use it for devnet journeys.
- `logos-co/logos-docs` — docs repo; Journey issues live here (`CONTRIBUTING.md`, templates under `resources/`).

## Submission

The template is a GitHub **Issue Form**. `gh issue create` has **no `--field` flag** — do not try to map form ids on the CLI. Two correct routes, both only after go-ahead:

- **CLI:** assemble the markdown packet (the `doc-packet.md` structure) and file it:
  `gh issue create -R logos-co/logos-docs --title "[Journey] <outcome>" --label "type:journey" --body-file <packet.md>`
  (The `type:journey` label is what routes it; it already exists in the repo.)
- **Web form (lets the requester pick the dropdown):** open `https://github.com/logos-co/logos-docs/issues/new?template=doc-packet.yml` and paste each section. The `?template=` URL shows a login wall to automated fetchers — read field definitions from `.github/ISSUE_TEMPLATE/doc-packet.yml` in the repo instead.

## Common mistakes

- **Filing before sign-off.** The single worst failure: a public issue + Docs work, unrequested. Always draft → review → go-ahead.
- **Placeholder/guessed POC.** Required identity fields come from the requester, full stop.
- **Demo-as-journey.** In-process examples don't prove a node-on-network journey. Match the real flow.
- **Client-repo config drift.** Verify devnet network params against the `logos-delivery` `logos.dev` preset, not stale client constants.
- **Wrong encryption layer.** "Encrypted" → libchat, not bare transport.
- **Unverified commands.** Trace or run every command; Docs and Red Team execute them verbatim.
