---
name: logos-messaging-update-deck
description: "Use when the Logos Messaging lead needs a recurring team/stakeholder update presentation — quarterly reviews or per-testnet-release updates — summarizing what was accomplished in a period. Builds a Slidev deck from the Logos roadmap, PM issues, and verified repo state. Keywords: presentation, slides, slidev, deck, quarterly update, testnet release, roadmap, progress report."
---

# Logos Messaging Update Deck

## Overview

Build a ~10–15 minute Slidev deck that updates the team on what Logos Messaging accomplished in a given period. The deck mirrors the **roadmap** (what was *supposed* to happen) checked against **verified GitHub state** (what *actually* happened).

**Core principle: every progress claim on a slide must be backed by verified live GitHub state — never by the prose of a weekly update, a roadmap checkbox, or a merged PR alone.** A presentation that overstates progress is worse than no presentation: the lead loses credibility in front of the team.

Used quarterly and for each testnet release (the roadmap is split into testnets).

## The Verification Discipline (read first)

The biggest failure mode is **reporting planned work as done.** Weekly updates mix "achieved / next / blocked"; roadmap checkboxes lag reality; a merged PR is not a shipped milestone. Treat every source except live issue/PR state as a *lead*, not a *fact*.

For **every** item that gets a status on a slide:
1. Find the concrete GitHub artifact behind it (issue, PR).
2. Verify its live state: `gh pr view <n> -R logos-messaging/<repo> --json state,mergedAt,title` / `gh issue view <n> -R ... --json state,title`.
3. Use **`mergedAt` ≠ null** for "merged", `state` for open/closed. A **closed-not-merged** PR shipped nothing.
4. Map to slide status honestly: a milestone/epic issue that is still **OPEN** is "in progress", not "delivered", no matter how many of its PRs merged.

### Red flags — STOP, you are about to fabricate progress

- Copying a line from a weekly update onto a slide without opening the cited PR/issue.
- Writing "shipped / done / delivered / released" for a milestone whose epic issue is still open.
- Treating a roadmap `[x]` checkbox as proof of completion.
- Saying "v0.X released" because a "prepare release" PR exists (it may be closed-not-merged).
- "The weekly says it's done, that's good enough." It is not. Open the artifact.

### Rationalization table

| Excuse | Reality |
|--------|---------|
| "The weekly update already says it's achieved." | Weeklies state intent and are written before merge. Verify the PR's `mergedAt`. |
| "The PR is merged, so the milestone is done." | Milestone = many deliverables. If the epic issue is open, it's in progress. |
| "Roadmap checkbox is ticked." | Checkboxes lag and are hand-edited. They're a lead, not proof. |
| "Re-checking every item is slow." | One overstated slide in front of the team costs more than 20 minutes of `gh`. |
| "The lead knows the real state, the slide is just a summary." | The team doesn't. The slide is the claim of record. |

## Procedure

1. **Confirm scope with the user** (see Checkpoints). Don't guess the period.
2. **Resolve the period → testnet milestone.** List releases: `gh api repos/logos-messaging/pm/milestones --jq '.[] | "\(.title) due:\(.due_on) open:\(.open_issues) closed:\(.closed_issues)"'`. The current period is normally the open testnet nearest its due date. Confirm with the user.
3. **Get what *should* be covered** = the epic issues under that GitHub Milestone:
   `gh issue list -R logos-messaging/pm --milestone "Testnet 0.X" --state all --json number,title,state` — these are issue-type **Milestone** (epics/work-packages). Cross-read the roadmap (`content/messaging/` in `logos-co/roadmap`, published at roadmap.logos.co) for framing and any items not yet in PM.
4. **Expand each epic into deliverables:** `gh api repos/logos-messaging/pm/issues/<n>/sub_issues --jq '.[] | "\(.repository_url|split("/")|.[-2:]|join("/")) #\(.number) \(.state) \(.title)"'` (issue-type **Deliverable**). **A deliverable's number resolves in its own repo, not in `pm`** — many live in code repos (e.g. `nim-sds#55`). Always verify a sub-issue with the repo from its `repository_url`/`url`, never `-R logos-messaging/pm` (that number maps to an unrelated pm issue).
5. **Trace deliverables down to code repos and VERIFY** per the Verification Discipline above. Read recent weeklies (`content/messaging/updates/*.md`) only as *leads* to which PRs/issues to check, then verify each in `logos-messaging/*` (logos-delivery, logos-chat, libchat, …).
6. **Draft the narrative** (see Outline). Status per item from verified state only.
7. **Scaffold the deck** by copying an existing deck's structure (see Output).
8. **Write `slides.md`.** Markdown only — do not run a build unless asked.
9. **Review with the user**, tune depth to 10–15 min (~12–16 slides).

> The PM **project boards** (e.g. #58 "Roadmap") are NOT reliable per-milestone status sources — their milestone fields are largely blank. Use **PM-repo issues filtered by the GitHub Milestone + live PR/issue state** as the source of truth. The hierarchy is Release (GitHub Milestone, e.g. "Testnet 0.2") → Milestone/Epic (issue type Milestone) → Deliverable (sub-issue) → task PRs in code repos.

## Resource map

| Resource | Location | Role |
|----------|----------|------|
| Roadmap | `logos-co/roadmap` (`content/messaging/`) · roadmap.logos.co | What *should* be covered + framing |
| PM | `logos-messaging/pm` (issues + milestones) | Releases → epics → deliverables |
| Code repos | `logos-messaging/*` (logos-delivery, logos-chat, libchat, …) | Verified actual state (PRs/issues) |
| Slidev theme | `@logos-co/slidev-theme-logos` (`logos-co/slidev-theme-logos`) | Brand styling + layouts |
| Output | Ask the user | Where decks live |
| Reference deck | A previous update deck in the output folder | Copy this structure |

## Output & deck conventions

- **Output dir:** ask the user; default a new folder next to the previous decks, named for the period (e.g. `2026-testnet-v0.2-messaging-update/`). Scaffold by copying `package.json`, `.npmrc`, `.gitignore` from the reference deck (depends on `@logos-co/slidev-theme-logos`).
- **Theme is authoritative for styling.** `theme: "@logos-co/slidev-theme-logos"` in frontmatter. Use its layouts; do **not** hardcode brand colors or hand-edit the theme. (The brand doc and theme README list slightly different hex values — trust the theme code.) If a needed layout is genuinely missing, add a new layout to the theme repo (a separate, deliberate change), don't inline CSS hacks.
- **Available layouts:** `cover, center, default, header, two-cols, three-column, two-panels, panel, purpose, steps, end`. Component: `<FrameBox label="...">`. Use `v-click` for progressive reveal. See the reference deck for idioms.
- **Demo:** insert a `layout: center` demo slide with speaker notes containing a live-demo script — do not claim a demo runs or embed screenshots unless the user confirms a working build. Example:
  ```md
  ---
  layout: center
  ---
  # Demo

  <!--
  Live demo script:
  1. nix run logos-delivery-demo
  2. createNode(logos.test, Edge); send a message; show the event log
  -->
  ```
- **Naming/voice:** current names only — Logos Delivery (not Waku/nwaku), Logos Chat (not Chat SDK/libchat), Logos Messaging = umbrella. Declarative, institutional tone (see brand doc).
- **Length:** ~12–16 slides for 10–15 min.

## Suggested outline (~14 slides)

1. Cover — "Logos Messaging — Testnet vX.Y Update", date, presenter.
2. Where we are — prior testnet shipped → this one in flight, due date (`layout: center`).
3. Period at a glance — epic count + verified status split (done / in progress / blocked).
4–N. One section per track (Delivery, Chat, Core, Status, Maintenance), highlighting key epics with **verified** status.
N+1. Blockers & risks.
N+2. Demo (optional, placeholder + script).
N+3. What's next — the following testnet.
N+4. End slide.

## Checkpoints — ask the user when unsure

1. **Period** — exact testnet (e.g. v0.2), or a calendar/sprint window? Anything to exclude?
2. **Audience** — internal team, broader Logos all-hands, or external? (Sets depth + how much to caveat blockers.)
3. **Scope** — is Status-integration work in or out? Which items to *highlight* vs. just list?
4. **Demo** — Logos Delivery or Logos Chat, and is there a build known to run?
5. **Output location** — confirm folder (default above).
6. **Metrics** — any fleet/adoption numbers to include that aren't in the roadmap?

## Common mistakes

- Lifting weekly-update prose onto slides without verifying the cited PR/issue (→ overstated progress).
- Marking an open epic as "delivered" because its PRs merged.
- Using a project board for status (its milestone fields are blank).
- Hardcoding brand colors instead of relying on the theme.
- Building the deck (running slidev) when only markdown was asked for.
- Covering everything ever done instead of just the period's roadmap items.
- Resolving a sub-issue number against `pm` when it actually lives in a code repo (use its `repository_url`).
