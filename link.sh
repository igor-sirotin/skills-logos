#!/usr/bin/env bash
# Symlink every skill in this repo into ~/.claude/skills/<name>.
# Safe to re-run: refreshes our links, prunes links to skills that no longer
# exist here, and never touches real directories (e.g. Claude Code's synced/).
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"

for skill in "$repo"/*/SKILL.md; do
  [ -e "$skill" ] || continue
  src="$(dirname "$skill")"
  name="$(basename "$src")"
  link="$dest/$name"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "skip   $name (real directory exists at $link)" >&2
    continue
  fi
  ln -sfn "$src" "$link"
  echo "link   $name"
done

# Remove dangling links that point back into this repo.
for link in "$dest"/*; do
  [ -L "$link" ] && [ ! -e "$link" ] || continue
  case "$(readlink "$link")" in
    "$repo"/*) rm "$link"; echo "prune  $(basename "$link")" ;;
  esac
done
