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
    """karar.json at a git ref, or None if the file is not there (e.g. first commit).

    Read as UTF-8 bytes on purpose: on Windows the default code page (cp1254 for Turkish) cannot decode the file.
    A file that exists but cannot be read raises, so the guard fails closed instead of passing every commit.
    """
    r = subprocess.run(["git", "show", ref], capture_output=True)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout.decode("utf-8-sig"))


def get(d, path):
    for k in path:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def main():
    try:  # a Windows console or pipe may not take every Turkish character; never crash on printing
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True,
                            encoding="utf-8").stdout.split()
    if "karar.json" not in staged:
        return 0
    try:
        old, new = git_show("HEAD:karar.json"), git_show(":karar.json")
    except Exception as e:
        print(f"\nAraştırma kapısı: karar.json okunamadı ({e}). Koruma çalışmadan commit'e izin verilmiyor.")
        print("Dosyayı geçerli UTF-8 JSON olarak düzelt; bilerek atlamak için: git commit --no-verify\n")
        return 1
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
