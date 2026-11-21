---
name: proje-baslat
description: Start a new research project from the user's research template (~/CALISMALAR/_arastirma-sablonu) so it uses the research-gate structure (karar.json, KARAR.md, durum.html status panel, commit guard) from day one. Use when the user says "yeni proje", "yeni araştırma projesi başlat", "proje-baslat", "projeyi kur", "şablonu kullan", or opens an empty folder for a new study, paper or thesis line. Also use to add the structure to an existing project folder that has no karar.json ("bu projeye kapı yapısını ekle").
---

# Proje başlat

Set up a research project so that the `arastirma-kapisi` gates, the `zayif-nokta-raporu` reading step and the status
panel are in place before any work starts. Speak Turkish.

Template: the folder written in `~/.claude/arastirma/sablon_yolu.txt` (set by the template's `kur.sh` / `kur.ps1`);
if that file is missing, `~/CALISMALAR/_arastirma-sablonu/`. It holds CLAUDE.md, KARAR.md, karar.json, README.md,
tools/durum.py, tools/karar_koruma.py and `kaynak.json` (resource preferences; read it, do not copy it). Registry: `~/.claude/arastirma/projeler.json`. On Windows use `python`
where these steps say `python3` if `python3 -c ""` fails (it does for the Microsoft Store shortcut).

## Steps

1. **Where.** Use the folder the user names, or the current working directory. If it already has a `karar.json`,
   stop and say so (offer to open the panel instead). If it has other files, do not overwrite anything: copy only
   the template files that are missing; if a `CLAUDE.md` exists, append the template's section under a heading
   instead of replacing it.
2. **Focus check (before copying).** Read the registry. The rule is one main project and one small side task. If
   there is already an active main project (`"durum": "aktif", "tur": "ana"`) or an active side task (`"tur": "yan"`),
   say so plainly: "Şu an aktif ana proje: X; yan iş: Y. Kural: bir ana, bir küçük yan iş." Ask what this new project
   is and which existing one is archived or paused to make room. If the registry is empty or missing, it may only
   mean this machine has no record: ask which projects are active on any machine and register them first. Do not
   continue until the user answers.
3. **Copy** the template files into the folder (`cp -n`), keep `tools/` executable. Copy only CLAUDE.md, KARAR.md,
   karar.json, README.md and tools/. Never copy `.git/`, `ornek/` (a filled example panel), `skills/`, `kur.sh`,
   `kur.ps1` or `.gitignore`; skip `README.md` if the project already has one.
4. **Git.** If the folder is not a git repository, run `git init`. Install the guard as two hooks,
   `.git/hooks/pre-commit` and `.git/hooks/pre-push` (in a repository root found with `git rev-parse --git-dir`),
   each with these lines, then `chmod +x`:
   `#!/bin/sh`, then `K="tools/karar_koruma.py"`, then
   `if python3 -c "" >/dev/null 2>&1; then exec python3 "$K" "$@"; fi`, then `exec python "$K" "$@"`;
   in `pre-push` write `--push "$@"` in place of `"$@"` on both exec lines. Hooks run from the repository root: if the
   project folder is a subfolder of the repository, prefix `K` with `git rev-parse --show-prefix`. Write the hooks
   as plain UTF-8 without BOM and with LF line endings (on Windows PowerShell 5.1 use
   `[IO.File]::WriteAllText(path, text, (New-Object Text.UTF8Encoding($false)))`, never `Set-Content -Encoding UTF8`,
   which adds a BOM and makes Git refuse to run the hook). Test that `python3` runs, not that it exists: on Windows
   `python3` is often the Microsoft Store shortcut, which exists but is not Python. If a hook already exists, do not
   replace it; tell the user how to chain it. The guard is tested after the first commit (step 8).
5. **Intake.** Ask only these, in one message:
   - project name and one-line goal;
   - the base paper/method (title or link), whether its code is available, and what it needs to run (training or
     only a checkpoint, GPU memory, operating system). Compare with `kaynak.json` in the template; if it matches an
     item in `ilk_tercih_degil`, say so now and ask whether to look for a fitting base paper first;
   - the condition the user suspects breaks it (if any). Record it as a hypothesis in KARAR.md; never pass it to the
     reader agents of `zayif-nokta-raporu`;
   - whether this condition or task was studied in an earlier project, and whether a simple rule or rival won there.
     If yes, fill `aile_kontrolu` and say that "bu kez neden farklı?" needs a measurable answer before any work.
   Fill `karar.json`: `proje`, `tur`, `olusturma` (today's absolute date), `temel_yontem`. Leave `bozulma` and the
   thesis sentence empty: they are filled only from measurements. Set `son_karar` to
   `{"karar": "KOŞULLU DEVAM", "neden": "Proje kuruldu; henüz ölçüm yok.", "siradaki_adim": "Temel makale için zayıf nokta raporu (0. adım)."}`.
   Mirror the same in `KARAR.md` (project name, date, base method).
6. **Register.** Add `{"ad", "yol", "tur", "durum": "aktif", "olusturma"}` to the registry (create the folder and
   file if missing; keep it a JSON list).
7. **Panel.** Run `python3 tools/durum.py` (or `python` as above) and tell the user the path of `durum.html`. Open it in the browser pane if
   one is available.
8. **First commit and guard test.** `git add -A && git commit -m "Proje kuruldu: araştırma şablonu"` only if the user
   agrees to a commit; otherwise leave it staged-free and say the guard is not tested yet. After the first commit,
   test that the guard **blocks**: change `donus.sinir` in `karar.json`, `git add karar.json`, run
   `.git/hooks/pre-commit` directly (no commit is made) and expect exit code 1 and the block message; then restore
   with `git checkout HEAD -- karar.json`. A guard that never blocks is off; say so if the test passes the change.
9. **Hand-off.** End with the next step: run `zayif-nokta-raporu` on the base paper. Remind once that the
   `arastirma-kapisi` gates run from now on whenever a method, pivot, rule change or submission comes up.

## Archiving

When the user says a project is finished or stopped ("projeyi kapat", "arşivle"), set its registry entry to
`"durum": "arsiv"` with the date and a one-line reason, set `son_karar` accordingly, and regenerate the panel. A
stopped project with a written negative result counts as finished, not failed.
