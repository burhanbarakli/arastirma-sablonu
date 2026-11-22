#!/bin/sh
# Installs the research skills into ~/.claude/skills and records where this template lives.
# Run again after every `git pull` to update the skills. macOS / Linux.
# Usage: ./kur.sh [personal folder]  (default: the saved path, else _arastirma-kisisel next to this template)
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
# Personal folder: this researcher's own kaynak.json, kapali_kapilar.json and gecmis.md. Never overwrite a file.
KTXT="$HOME/.claude/arastirma/kisisel_yolu.txt"
if [ -n "$1" ]; then K="$1"
elif [ -f "$KTXT" ]; then K="$(cat "$KTXT")"
else K="$(dirname "$HERE")/_arastirma-kisisel"; fi
mkdir -p "$K"
K="$(cd "$K" && pwd)"
for f in "$HERE"/kisisel-ornek/*; do
  b="$(basename "$f")"
  [ -e "$K/$b" ] || { cp "$f" "$K/$b"; echo "kişisel dosya oluşturuldu: $K/$b"; }
done
printf '%s\n' "$K" > "$KTXT"
echo "kişisel klasör: $K"
