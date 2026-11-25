#!/usr/bin/env python3
"""Paired-difference intervals and seed counts for equivalence (non-inferiority) decisions.

Standard library only. Used by method-transfer studies (karar.json > calisma_turu "aktarim").

  python3 tools/aralik.py fark 0.012 -0.004 0.020
      One paired difference per seed (same seed, same initial states for both arms), oriented so that a positive
      value means "better" for the first arm (multiply by -1 when smaller is better). Prints n, mean, sd and the
      two-sided 90% t-interval. The 90% interval is the TOST test at alpha = 0.05: "lower bound > -delta" shows
      non-inferiority, "interval inside (-delta, +delta)" shows equivalence. Record [lo, hi] in
      karar.json > aktarim.karsilastirmalar; the panel applies the decision rule.

  python3 tools/aralik.py tohum --delta 0.05 --sd 0.03
  python3 tools/aralik.py tohum --delta 0.05 --pilot 0.012 -0.004
      Seeds needed so that an equivalence (TOST, alpha 0.05, power 80%) can be shown when the true difference is 0.
      --sd is the standard deviation of paired differences (for example from an earlier comparable project);
      --pilot gives pilot differences, and the 95% upper confidence bound of their sd is used, never the point
      estimate alone (with two pilot seeds that bound is about 16 times the estimate: two seeds cannot size a study).

The numbers are a planning aid, not a substitute for the pre-registered rule.
"""
import math
import statistics
import sys

# one-sided t quantiles, df = 1..30
T95 = [6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761, 1.753,
       1.746, 1.740, 1.734, 1.729, 1.725, 1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697]
T90 = [3.078, 1.886, 1.638, 1.533, 1.476, 1.440, 1.415, 1.397, 1.383, 1.372, 1.363, 1.356, 1.350, 1.345, 1.341,
       1.337, 1.333, 1.330, 1.328, 1.325, 1.323, 1.321, 1.319, 1.318, 1.316, 1.315, 1.314, 1.313, 1.311, 1.310]
# chi-square lower-tail 5% quantiles, df = 1..30 (for a 95% upper bound of sd)
CHI05 = [0.00393, 0.103, 0.352, 0.711, 1.145, 1.635, 2.167, 2.733, 3.325, 3.940, 4.575, 5.226, 5.892, 6.571, 7.261,
         7.962, 8.672, 9.390, 10.117, 10.851, 11.591, 12.338, 13.091, 13.848, 14.611, 15.379, 16.151, 16.928, 17.708,
         18.493]


def t95(df):
    return T95[df - 1] if df <= 30 else 1.645


def t90(df):
    return T90[df - 1] if df <= 30 else 1.282


def sd_upper(values):
    n = len(values)
    s = statistics.stdev(values)
    df = n - 1
    if df > 30:
        # Wilson-Hilferty approximation of the chi-square 5% quantile
        q = df * (1 - 2 / (9 * df) - 1.645 * math.sqrt(2 / (9 * df))) ** 3
    else:
        q = CHI05[df - 1]
    return s, s * math.sqrt(df / q)


def needed(delta, sd, cap=500):
    for n in range(2, cap + 1):
        if (t95(n - 1) + t90(n - 1)) * sd / math.sqrt(n) <= delta:
            return n
    return None


def numbers(args):
    out = []
    for a in args:
        try:
            out.append(float(a.replace(",", ".")))
        except ValueError:
            raise SystemExit(f"sayı değil: {a}")
    return out


def opt(args, name):
    if name in args:
        i = args.index(name)
        rest = []
        for a in args[i + 1:]:
            if a.startswith("--"):
                break
            rest.append(a)
        return rest
    return None


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if not argv or argv[0] not in ("fark", "tohum"):
        print(__doc__)
        return 2
    if argv[0] == "fark":
        d = numbers(argv[1:])
        if len(d) < 2:
            raise SystemExit("En az iki eşli fark gerekir (tohum başına bir tane).")
        n, m, s = len(d), statistics.mean(d), statistics.stdev(d)
        h = t95(n - 1) * s / math.sqrt(n)
        print(f"n = {n} tohum, ortalama fark = {m:.6g}, sd = {s:.6g}")
        print(f"%90 aralık (TOST, alfa 0.05): [{m - h:.6g}, {m + h:.6g}]   yarı genişlik = {h:.6g}")
        if n < 3:
            print("Uyarı: 3'ten az tohum. Sonuç pilottur; kapı geçirmez.")
        print("karar.json'a: [" + f"{m - h:.6g}, {m + h:.6g}" + "]")
        return 0
    delta = opt(argv, "--delta")
    if not delta:
        raise SystemExit("--delta gerekli (ana ölçütte eşdeğerlik payı).")
    delta = numbers(delta[:1])[0]
    sd = opt(argv, "--sd")
    pilot = opt(argv, "--pilot")
    if sd:
        sdv = numbers(sd[:1])[0]
        src = f"verilen sd = {sdv:.6g}"
    elif pilot:
        p = numbers(pilot)
        if len(p) < 2:
            raise SystemExit("--pilot için en az iki eşli fark gerekir.")
        s, sdv = sd_upper(p)
        src = f"pilot sd = {s:.6g} ({len(p)} tohum), %95 üst sınır = {sdv:.6g}"
    else:
        raise SystemExit("--sd ya da --pilot gerekli.")
    n = needed(delta, sdv)
    print(f"δ = {delta:.6g}; {src}")
    if n is None:
        print("500 tohumla bile gösterilemez: δ bu yayılıma göre çok dar ya da sd tahmini çok belirsiz.")
    else:
        print(f"Gereken tohum (TOST, alfa 0.05, güç %80, gerçek fark 0): {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
