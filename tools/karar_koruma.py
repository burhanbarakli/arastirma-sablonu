#!/usr/bin/env python3
"""Git pre-commit guard for karar.json.

Rules may change; they may not change silently. The guard blocks a commit when:
- a frozen rule changes (thesis sentence and its date, threshold, oracle and simple-remedy definitions, planned seeds,
  pivot limit, the protocol fields) without a complete new entry in "sapmalar" in the same commit;
- a frozen rule is written for the first time after measurements exist (a threshold chosen after seeing results),
  without such an entry;
- a measured row in "uc_sayi.satirlar" is changed or removed, or a limitation is removed, without such an entry;
- an entry is removed from or edited in "sapmalar", "donus.kayit" or "overrides" (these lists only grow; no sapma
  can excuse it);
- karar.json is deleted.

A complete sapma entry has non-empty "tarih", "ne" and "gerekce". Every staged file named karar.json is checked, so a
project in a subfolder is covered too.

Installed by proje-baslat as .git/hooks/pre-commit. Bypass on purpose with `git commit --no-verify` (not advised).
"""
import json
import os
import subprocess
import sys

FROZEN = [
    ("tez_cumlesi", "metin"), ("tez_cumlesi", "tarih"),
    ("uc_sayi", "esik"), ("uc_sayi", "kahin_tanimi"), ("uc_sayi", "basit_care_tanimi"),
    ("tohum", "plan"), ("donus", "sinir"),
    ("protokol", "karar_kurali"), ("protokol", "olcut"), ("protokol", "kilitli_test"), ("protokol", "durma_kurali"),
]
GROW_ONLY = [("sapmalar",), ("donus", "kayit"), ("overrides",)]
EMPTY = (None, "", [], {})


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


def complete(entry):
    return isinstance(entry, dict) and all(str(entry.get(k) or "").strip() for k in ("tarih", "ne", "gerekce"))


def problems(old, new):
    """Return (excusable, fatal) lists of problems for one karar.json."""
    excusable, fatal = [], []
    measured = bool(get(old, ("uc_sayi", "satirlar")))
    for p in FROZEN:
        a, b = get(old, p), get(new, p)
        if a == b:
            continue
        name = ".".join(p)
        if a not in EMPTY:
            excusable.append(f"değişen: {name}  ({a!r} -> {b!r})")
        elif measured:
            excusable.append(f"ölçümden sonra ilk kez yazılan: {name}  (-> {b!r})")
    new_rows = get(new, ("uc_sayi", "satirlar")) or []
    for r in (get(old, ("uc_sayi", "satirlar")) or []):
        if r not in new_rows:
            excusable.append(f"değişen ya da silinen ölçüm satırı: {r.get('kosul', r) if isinstance(r, dict) else r}")
    for x in (old.get("sinirliliklar") or []):
        if x not in (new.get("sinirliliklar") or []):
            excusable.append(f"silinen sınırlılık: {x}")
    for p in GROW_ONLY:
        new_list = get(new, p) or []
        for x in (get(old, p) or []):
            if x not in new_list:
                fatal.append(f"{'.'.join(p)} listesinden silinen ya da değiştirilen kayıt: {x}")
    return excusable, fatal


def check(path):
    try:
        old, new = git_show(f"HEAD:{path}"), git_show(f":{path}")
    except Exception as e:
        print(f"\nAraştırma kapısı: {path} okunamadı ({e}). Koruma çalışmadan commit'e izin verilmiyor.")
        print("Dosyayı geçerli UTF-8 JSON olarak düzelt; bilerek atlamak için: git commit --no-verify\n")
        return 1
    if old is None:
        return 0
    if new is None:
        print(f"\nAraştırma kapısı: {path} siliniyor. Karar kaydı silinemez; projeyi arşivlemek için durumunu değiştir.\n")
        return 1
    excusable, fatal = problems(old, new)
    added = (new.get("sapmalar") or [])[len(old.get("sapmalar") or []):]
    added_ok = any(complete(x) for x in added)
    if fatal:
        print(f"\nAraştırma kapısı ({path}): bu listeler yalnız büyüyebilir; eski kayıt silinemez ya da değiştirilemez.")
        for x in fatal:
            print(f"  - {x}")
        print("Kaydı geri koy. Düzeltme gerekiyorsa eskisini silme, yeni bir kayıt ekle.\n")
        return 1
    if excusable and not added_ok:
        print(f"\nAraştırma kapısı ({path}): dondurulmuş bir kural ya da ölçüm sessizce değişiyor.")
        for x in excusable:
            print(f"  - {x}")
        if added:
            print("Eklenen sapma eksik: 'tarih', 'ne' ve 'gerekce' alanlarının üçü de dolu olmalı.")
        print("Aynı commit'te 'sapmalar' listesine tarih, ne değişti ve gerekçe ekle; ya da değişikliği geri al.\n")
        return 1
    return 0


def main():
    try:  # a Windows console or pipe may not take every Turkish character; never crash on printing
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    staged = subprocess.run(["git", "diff", "--cached", "--name-only", "--no-renames"], capture_output=True,
                            text=True, encoding="utf-8").stdout.splitlines()
    rc = 0
    for path in staged:
        if os.path.basename(path) == "karar.json":
            rc = max(rc, check(path))
    return rc


if __name__ == "__main__":
    sys.exit(main())
