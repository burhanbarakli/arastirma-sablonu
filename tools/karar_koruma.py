#!/usr/bin/env python3
"""Git guard for karar.json (pre-commit, and pre-push with --push).

Rules may change; they may not change silently. The guard blocks when:
- a frozen rule changes (thesis sentence and its date, threshold and its unit, oracle and simple-remedy definitions,
  planned seeds and what a seed means, pivot limit, the protocol fields, the Kapı 1 question, condition levels and
  threshold) without a complete new entry in "sapmalar" in the same commit;
- a frozen rule is written for the first time after measurements exist, or in the same commit as the first
  measurement (a threshold chosen after seeing results), without such an entry; for the Kapı 1 fields (soru.metin,
  soru.kosul_duzeyleri, soru.esik) the Kapı 1 drop ("bozulma") already counts as a measurement;
- "bozulma" is written for the first time while soru.metin, soru.kosul_duzeyleri, soru.esik or protokol.olcut was
  not yet in the previous commit (the question, its levels, its threshold and one metric come before the drop);
- a measured row in "uc_sayi.satirlar" is changed or removed, or a limitation is removed, without such an entry;
- in a method-transfer study (calisma_turu "aktarim"): the advantage axis, its metric and direction, δ, ε, the
  required seeds or the two pre-registered outcome sentences change, or are written after the first measurement in
  "aktarim.olcumler" / "aktarim.karsilastirmalar"; a first candidate enters "aktarim.adaylar" while the axis, its
  metric and direction, δ, ε and both outcome sentences were not yet in the previous commit; the row picked from a
  bottleneck map ("aktarim.on_kesif") or its metric changes, or the axis metric differs from the picked row's metric;
  or a measured row in
  "aktarim.olcumler" / "aktarim.karsilastirmalar" is changed or removed; each without such an entry;
- an entry is removed from or edited in "sapmalar", "donus.kayit" or "overrides" (these lists only grow; no sapma
  can excuse it);
- karar.json is deleted, is not valid UTF-8 JSON, or has a duplicate key.

A complete sapma entry is new (not a copy of an earlier entry), has a date (YYYY-AA-GG), and a real "ne" and
"gerekce" (not empty, not a placeholder such as "doldurulacak"). An incomplete earlier entry is completed by a new
entry that names it, e.g. {"tarih", "ne", "gerekce", "duzeltir": "<tarih of the old entry>"}; old entries are never
edited. Adding a frozen field with an empty value (syncing an old project to a newer schema) is not blocked. A
change to a filled frozen field also needs an entry before any result: the guard cannot know what was seen outside
git, so the entry says "sonuç görülmeden, planlama". Every staged file named karar.json is checked, so a project in
a subfolder is covered too, whatever letters its path has.

pre-commit: compares HEAD with the index. Commands that do not run the pre-commit hook (git revert, rebase,
commit-tree, a changed core.hooksPath) bypass it; `--push`, installed as .git/hooks/pre-push, checks every commit being
pushed against its parent, and the remote tip against the new tip, so such changes are caught before they leave the
machine. A project without a remote has only the pre-commit check.

Installed by proje-baslat. Bypass on purpose with `git commit --no-verify` / `git push --no-verify` (not advised).
"""
import json
import os
import re
import subprocess
import sys

FROZEN = [
    ("tez_cumlesi", "metin"), ("tez_cumlesi", "tarih"),
    ("uc_sayi", "esik"), ("uc_sayi", "birim"), ("uc_sayi", "kahin_tanimi"), ("uc_sayi", "basit_care_tanimi"),
    ("tohum", "plan"), ("tohum", "tanim"), ("donus", "sinir"),
    ("protokol", "karar_kurali"), ("protokol", "olcut"), ("protokol", "kilitli_test"), ("protokol", "durma_kurali"),
    ("soru", "metin"), ("soru", "kosul_duzeyleri"), ("soru", "esik"),
    ("calisma_turu",),
    ("aktarim", "eksen"), ("aktarim", "eksen_olcutu"), ("aktarim", "eksen_yonu"), ("aktarim", "performans_yonu"),
    ("aktarim", "delta"), ("aktarim", "epsilon"), ("aktarim", "tohum_gerekli"),
    ("aktarim", "sonuc_a"), ("aktarim", "sonuc_b"),
    ("aktarim", "on_kesif", "secilen_satir"), ("aktarim", "on_kesif", "olcut"),
]
# Kapı 1 fields: frozen once the Kapı 1 drop ("bozulma") exists, not only once three-number rows exist.
KAPI1 = [("soru", "metin"), ("soru", "kosul_duzeyleri"), ("soru", "esik")]
# Must already be committed when "bozulma" is first written (question, levels, threshold, one metric).
KAPI1_BEFORE_DROP = KAPI1 + [("protokol", "olcut")]
# Method-transfer study: must already be committed when the first candidate is named (axis before candidate).
AKTARIM_BEFORE_CANDIDATE = [("aktarim", "eksen"), ("aktarim", "eksen_olcutu"), ("aktarim", "eksen_yonu"),
                            ("aktarim", "delta"), ("aktarim", "epsilon"), ("aktarim", "sonuc_a"), ("aktarim", "sonuc_b")]
MEASURED_ROWS = [("uc_sayi", "satirlar"), ("aktarim", "olcumler"), ("aktarim", "karsilastirmalar")]
GROW_ONLY = [("sapmalar",), ("donus", "kayit"), ("overrides",)]
EMPTY = (None, "", [], {})
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER = re.compile(r"doldurulacak|sonra yazılacak|todo|tbd|xxx|^[\s.?…\-x]*$", re.IGNORECASE)
ZERO = "0" * 40


def git(*args):
    """Run git with paths printed raw (no quoting of non-ASCII letters)."""
    return subprocess.run(["git", "-c", "core.quotepath=off", *args], capture_output=True)


def no_duplicates(pairs):
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise ValueError(f"yinelenen anahtar: {', '.join(dup)}")
    return dict(pairs)


def git_show(spec):
    """karar.json at a git object spec ("HEAD:path", ":path", "<sha>:path"), or None if it is not there.

    Read as UTF-8 bytes on purpose: on Windows the default code page (cp1254 for Turkish) cannot decode the file.
    A file that exists but cannot be read raises, so the guard fails closed instead of passing every commit.
    """
    r = git("show", spec)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout.decode("utf-8-sig"), object_pairs_hook=no_duplicates)


def get(d, path):
    for k in path:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def complete(entry):
    if not isinstance(entry, dict):
        return False
    tarih, ne, gerekce = (str(entry.get(k) or "").strip() for k in ("tarih", "ne", "gerekce"))
    return bool(DATE.match(tarih)) and all(len(x) >= 5 and not PLACEHOLDER.search(x) for x in (ne, gerekce))


def problems(old, new):
    """Return (excusable, fatal) lists of problems for one karar.json."""
    excusable, fatal = [], []
    measured = any(get(old, p) or get(new, p) for p in MEASURED_ROWS)
    dropped = measured or bool(get(old, ("bozulma",)) or get(new, ("bozulma",)))
    for p in FROZEN:
        a, b = get(old, p), get(new, p)
        if a == b:
            continue
        name = ".".join(p)
        if p == ("calisma_turu",) and a is None and b == "bosluk":
            continue  # an old project synced to the schema keeps its default type
        if a not in EMPTY:
            excusable.append(f"değişen: {name}  ({a!r} -> {b!r})")
        elif b not in EMPTY and (dropped if p in KAPI1 else measured):
            # an empty field added to an old project (schema sync) is not a rule being written
            excusable.append(f"ölçümden sonra ya da ölçümle birlikte ilk kez yazılan: {name}  (-> {b!r})")
    if get(old, ("bozulma",)) in EMPTY and get(new, ("bozulma",)) not in EMPTY:
        missing = [".".join(p) for p in KAPI1_BEFORE_DROP if get(old, p) in EMPTY]
        if missing:
            excusable.append("Kapı 1 bozulması, şunlar önceki bir commit'te yazılmadan girildi: " + ", ".join(missing))
    if get(old, ("aktarim", "adaylar")) in EMPTY and get(new, ("aktarim", "adaylar")) not in EMPTY:
        missing = [".".join(p) for p in AKTARIM_BEFORE_CANDIDATE if get(old, p) in EMPTY]
        if missing:
            excusable.append("ilk aday, şunlar önceki bir commit'te yazılmadan girildi (eksen adaydan önce): "
                             + ", ".join(missing))
    ok_row = get(new, ("aktarim", "on_kesif", "olcut"))
    ax = get(new, ("aktarim", "eksen_olcutu"))
    if ok_row not in EMPTY and ax not in EMPTY and ax != ok_row and (
            ax != get(old, ("aktarim", "eksen_olcutu")) or ok_row != get(old, ("aktarim", "on_kesif", "olcut"))):
        excusable.append(f"eksen ölçütü haritada seçilen satırın ölçütünden farklı: {ax!r} ≠ {ok_row!r}")
    for rp in MEASURED_ROWS:
        new_rows = get(new, rp) or []
        for r in (get(old, rp) or []):
            if r not in new_rows:
                label = (r.get("kosul") or r.get("kol") or r.get("rol") or r.get("aday") or r) if isinstance(r, dict) else r
                excusable.append(f"değişen ya da silinen ölçüm satırı ({'.'.join(rp)}): {label}")
    for x in (old.get("sinirliliklar") or []):
        if x not in (new.get("sinirliliklar") or []):
            excusable.append(f"silinen sınırlılık: {x}")
    for p in GROW_ONLY:
        new_list = get(new, p) or []
        for x in (get(old, p) or []):
            if x not in new_list:
                fatal.append(f"{'.'.join(p)} listesinden silinen ya da değiştirilen kayıt: {x}")
    return excusable, fatal


def check(old_spec, new_spec, label):
    """Compare karar.json between two object specs; print the reason and return 1 if blocked."""
    try:
        old, new = git_show(old_spec), git_show(new_spec)
    except Exception as e:
        print(f"\nAraştırma kapısı: {label} okunamadı ({e}). Koruma çalışmadan geçişe izin verilmiyor.")
        print("Dosyayı geçerli UTF-8 JSON olarak düzelt (yinelenen anahtar olmadan); bilerek atlamak için --no-verify\n")
        return 1
    if old is None:
        return 0
    if new is None:
        print(f"\nAraştırma kapısı: {label} siliniyor. Karar kaydı silinemez; projeyi arşivlemek için durumunu değiştir.\n")
        return 1
    excusable, fatal = problems(old, new)
    old_sapma = old.get("sapmalar") or []
    added = [x for x in (new.get("sapmalar") or []) if x not in old_sapma]
    added_ok = any(complete(x) for x in added)
    if fatal:
        print(f"\nAraştırma kapısı ({label}): bu listeler yalnız büyüyebilir; eski kayıt silinemez ya da değiştirilemez.")
        for x in fatal:
            print(f"  - {x}")
        print("Kaydı geri koy. Düzeltme gerekiyorsa eskisini silme, yeni bir kayıt ekle.\n")
        return 1
    if excusable and not added_ok:
        print(f"\nAraştırma kapısı ({label}): dondurulmuş bir kural ya da ölçüm sessizce değişiyor.")
        for x in excusable:
            print(f"  - {x}")
        if added:
            print("Eklenen sapma eksik: tarih YYYY-AA-GG, 'ne' ve 'gerekce' gerçek metin olmalı (yer tutucu olmaz).")
        print("Aynı commit'te 'sapmalar' listesine yeni bir kayıt ekle (tarih, ne değişti, gerekçe); ya da geri al.\n")
        return 1
    return 0


def karar_paths(names_z):
    return [p for p in names_z.decode("utf-8").split("\0") if p and os.path.basename(p) == "karar.json"]


def pre_commit():
    names = git("diff", "--cached", "--name-only", "-z", "--no-renames").stdout
    rc = 0
    for path in karar_paths(names):
        rc = max(rc, check(f"HEAD:{path}", f":{path}", path))
    return rc


def pre_push(lines):
    rc = 0
    for line in lines:
        parts = line.split()
        if len(parts) != 4 or parts[1] == ZERO:  # malformed, or a branch being deleted
            continue
        local, remote = parts[1], parts[3]
        known = remote != ZERO and git("cat-file", "-e", f"{remote}^{{commit}}").returncode == 0
        span = [f"{remote}..{local}"] if known else [local, "--not", "--remotes"]
        for c in git("rev-list", "--reverse", *span).stdout.decode().split():
            if git("rev-parse", "-q", "--verify", f"{c}^").returncode != 0:
                continue  # root commit: nothing to compare with
            names = git("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "--no-renames", f"{c}^", c).stdout
            for path in karar_paths(names):
                rc = max(rc, check(f"{c}^:{path}", f"{c}:{path}", f"{path} @ {c[:7]}"))
        if known:  # catches history rewritten under a pushed tip (dropped or reverted entries)
            names = git("diff", "--name-only", "-z", "--no-renames", remote, local).stdout
            for path in karar_paths(names):
                rc = max(rc, check(f"{remote}:{path}", f"{local}:{path}", f"{path} (uzak uç -> yeni uç)"))
    return rc


def main():
    try:  # Git Bash pipes need UTF-8; never crash on printing
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "--push" in sys.argv[1:]:
        return pre_push(sys.stdin.read().splitlines())
    return pre_commit()


if __name__ == "__main__":
    sys.exit(main())
