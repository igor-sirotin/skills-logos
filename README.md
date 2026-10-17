# skills-logos

[Claude Code](https://claude.com/claude-code) skills for working on [Logos](https://logos.co) Messaging. General-purpose ones live in [skills](https://github.com/igor-sirotin/skills).

Each top-level directory is one skill (a `SKILL.md`, plus any supporting files).
The repo lives anywhere; `link.sh` symlinks each skill into `~/.claude/skills/<name>`,
where Claude Code discovers it. `~/.claude/skills/` itself stays unversioned, so
Claude Code's own `synced/` and `.trash/` never touch this repo.

## Skills

- **bumping-a-logos-module-backend** — bump a module's backend library and apply the upstream changes.
- **logos-messaging-update-deck** — build a recurring Logos Messaging update deck.
- **releasing-a-logos-module** — cut a Logos module release and write its notes.
- **writing-logos-messaging-journey** — write a Logos Messaging "Journey" doc packet.

## Install

```sh
git clone https://github.com/igor-sirotin/skills-logos.git ~/src/skills-logos
~/src/skills-logos/link.sh
```

Re-run `link.sh` after adding, renaming or removing a skill: it links new ones,
prunes links to removed ones, and skips any real directory already in the way.
