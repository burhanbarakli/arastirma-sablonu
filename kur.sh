#!/bin/sh
# Installs the research skills into ~/.claude/skills and records where this template lives.
# Run again after every `git pull` to update the skills. macOS / Linux.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/.claude/skills" "$HOME/.claude/arastirma"
for s in "$HERE"/skills/*/; do
  name="$(basename "$s")"
  rm -rf "$HOME/.claude/skills/$name"
  cp -R "$s" "$HOME/.claude/skills/$name"
  echo "skill kuruldu: $name"
done
printf '%s\n' "$HERE" > "$HOME/.claude/arastirma/sablon_yolu.txt"
[ -f "$HOME/.claude/arastirma/projeler.json" ] || echo "[]" > "$HOME/.claude/arastirma/projeler.json"
chmod +x "$HERE"/tools/*.py
echo "şablon yolu: $HERE"
