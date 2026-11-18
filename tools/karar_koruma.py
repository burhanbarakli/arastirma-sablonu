#!/usr/bin/env python3
"""Git pre-commit guard for karar.json.

Blocks a commit that changes a frozen rule (thesis sentence, threshold, oracle definition, planned seeds, pivot
limit) or removes a limitation, unless the same commit also adds an entry to "sapmalar". Rules may change; they may
not change silently.

Installed by proje-baslat as .git/hooks/pre-commit. Bypass on purpose with `git commit --no-verify` (not advised).
"""
import json
import subprocess
import sys

FROZEN = [("tez_cumlesi", "metin"), ("uc_sayi", "esik"), ("uc_sayi", "kahin_tanimi"), ("tohum", "plan"), ("donus", "sinir")]


def git_show(ref):
    try:
        return json.loads(subprocess.run(["git", "show", ref], capture_output=True, text=True, check=True).stdout)
    except Exception:
        return None


def get(d, path):
    for k in path:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def main():
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True).stdout.split()
    if "karar.json" not in staged:
        return 0
    old, new = git_show("HEAD:karar.json"), git_show(":karar.json")
    if old is None or new is None:
        return 0
    changed = [".".join(p) for p in FROZEN if get(old, p) not in (None, "", []) and get(old, p) != get(new, p)]
    lost = [x for x in (old.get("sinirliliklar") or []) if x not in (new.get("sinirliliklar") or [])]
    added_sapma = len(new.get("sapmalar") or []) > len(old.get("sapmalar") or [])
    if (changed or lost) and not added_sapma:
        print("\nAraştırma kapısı: karar.json'da dondurulmuş bir kural sessizce değişiyor.")
        for c in changed:
            print(f"  - değişen: {c}  ({get(old, c.split('.'))!r} -> {get(new, c.split('.'))!r})")
        for x in lost:
            print(f"  - silinen sınırlılık: {x}")
        print("Aynı commit'te 'sapmalar' listesine tarih, ne değişti ve gerekçe ekle; ya da değişikliği geri al.\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
