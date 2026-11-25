#!/usr/bin/env python3
"""Research status panel: reads karar.json and writes durum.html next to it.

Usage: python3 tools/durum.py [path/to/karar.json]
Standard library only (Python 3.8+). The active-project registry is read from ~/.claude/arastirma/projeler.json
when it exists.
"""
import datetime
import html
import json
import os
import re
import sys

STAGES = [
    ("okuma", "0", "Okuma", "zayif-nokta-raporu", "Makalenin zayıf noktaları kaynaklarıyla çıkarıldı mı?"),
    ("soru", "1", "Soru", "arastirma-kapisi", "Fikir ölçülmüş bir bozulmadan mı doğdu?"),
    ("yeniden_uretim", "2", "Yeniden üretim", "arastirma-kapisi", "Temel yöntem makalenin sayılarıyla üretildi mi?"),
    ("uc_sayi", "3", "Üç sayı", "arastirma-kapisi", "Taban, en güçlü basit çare ve adil kâhin ölçüldü mü?"),
    ("rakip_adaleti", "4", "Rakip adaleti", "arastirma-kapisi", "Rakipler aynı bütçe, ayar ve bilgiyle mi?"),
    ("protokol", "5", "Protokol", "arastirma-kapisi", "Karar kuralı, tohum, kilitli test ve durma kuralı sonuçtan önce yazıldı mı?"),
    ("ana_kosu", "·", "Ana koşu", "", "Protokole göre koşuldu mu?"),
    ("gerceklik", "6", "Gerçeklik ve tavan", "arastirma-kapisi", "Benzetimin kusursuzlukları ve tavan sınandı mı?"),
    ("kor_denetim", "·", "Kör denetim", "", "Sonucu bilmeyen biri baştan hesapladı mı?"),
    ("yazim", "7", "Yazım", "arastirma-kapisi", "Sınırlılıklar duruyor, iddialar ölçülen boşlukla uyumlu mu?"),
]
# Method-transfer study (calisma_turu "aktarim"): same stage keys, different questions.
STAGES_AKTARIM = [
    ("okuma", "0", "Okuma", "zayif-nokta-raporu", "M'nin makalesinin zayıf noktaları kaynaklarıyla çıkarıldı mı?"),
    ("soru", "A1", "Darboğaz ve eksen", "arastirma-kapisi",
     "M'nin darboğazı kendi koşunda ölçüldü mü; eksen, δ, ε ve iki sonuç cümlesi aday adı geçmeden yazıldı mı?"),
    ("yeniden_uretim", "2", "Yeniden üretim", "arastirma-kapisi", "M makalenin sayılarıyla üretildi mi?"),
    ("uc_sayi", "A3", "Kollar", "arastirma-kapisi",
     "Taban, M ve basit alternatifler (ilkenin ucuz eki dahil) ölçüldü mü; eksende pay var mı?"),
    ("rakip_adaleti", "4", "Rakip adaleti", "arastirma-kapisi", "M ve basit alternatifler aynı bütçe, ayar ve bilgiyle mi?"),
    ("protokol", "5", "Protokol", "arastirma-kapisi",
     "İki sonuçlu karar kuralı, hesaplanan tohum, kilitli test ve durma kuralı sonuçtan önce yazıldı mı?"),
    ("ana_kosu", "·", "Ana koşu", "", "Protokole göre, hesaplanan tohumla koşuldu mu?"),
    ("gerceklik", "6", "Gerçeklik ve tavan", "arastirma-kapisi", "Avantaj ekseni zor koşulda ya da gerçek testte sınandı mı?"),
    ("kor_denetim", "·", "Kör denetim", "", "Sonucu bilmeyen biri baştan hesapladı mı?"),
    ("yazim", "7", "Yazım", "arastirma-kapisi", "Alternatifin geride kaldığı yerler metinde mi; iddia sonucun türü kadar mı?"),
]
ORDER = [s[0] for s in STAGES]
STATUS_LABEL = {"gecti": "Geçti", "kosullu": "Koşullu", "durdu": "Durdu", "bekliyor": "Bekliyor"}
REGISTRY = os.path.expanduser("~/.claude/arastirma/projeler.json")


def esc(x):
    return html.escape("" if x is None else str(x))


def reached(state, stage):
    """True when every stage before `stage` has at least started (not 'bekliyor')."""
    i = ORDER.index(stage)  # both stage tables share the same keys and order
    return all(state.get("asamalar", {}).get(k, {}).get("durum", "bekliyor") != "bekliyor" for k in ORDER[:i])


PLACEHOLDER = re.compile(r"doldurulacak|sonra yazılacak|todo|tbd|xxx|^[\s.?…\-x]*$", re.IGNORECASE)


def incomplete_sapmalar(sp):
    """Entries with a placeholder or missing part that no later entry completes ("duzeltir": <its date>)."""
    fixed = {str(x.get("duzeltir")) for x in sp if isinstance(x, dict) and x.get("duzeltir")}
    out = []
    for x in sp:
        if not isinstance(x, dict):
            out.append(x)
            continue
        parts = [str(x.get(k) or "").strip() for k in ("tarih", "ne", "gerekce")]
        if any(len(p) < 5 or PLACEHOLDER.search(p) for p in parts[1:]) or not parts[0]:
            if str(x.get("tarih")) not in fixed:
                out.append(x)
    return out


def gap(u):
    rows = [r for r in u.get("satirlar", []) if None not in (r.get("basit_care"), r.get("kahin"))]
    if not rows:
        return None, None
    best = max(rows, key=lambda r: r["kahin"] - r["basit_care"])
    return best, best["kahin"] - best["basit_care"]


def is_aktarim(s):
    return s.get("calisma_turu") == "aktarim"


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def interval(x):
    return isinstance(x, (list, tuple)) and len(x) == 2 and all(num(v) for v in x)


def arm_value(at, role, key):
    """Mean of a measured value for one arm role (taban, M) in aktarim.olcumler; None when absent."""
    vals = [r.get(key) for r in at.get("olcumler") or [] if isinstance(r, dict) and r.get("rol") == role and num(r.get(key))]
    return sum(vals) / len(vals) if vals else None


def outcome(at, row):
    """Apply the pre-registered two-outcome rule to one comparison row. Returns (code, text)."""
    d, e, need = at.get("delta"), at.get("epsilon"), at.get("tohum_gerekli")
    if not (num(d) and num(e)):
        return "eksik", "δ ya da ε yazılmamış: kural uygulanamaz."
    n = row.get("tohum") or 0
    if not num(need):
        return "pilot", f"{n} tohum; gereken tohum hesaplanmamış: pilot."
    if n < max(3, need):
        return "pilot", f"{n} tohum < gereken {max(3, int(need))}: pilot, kapı geçirmez."
    pm, pb, ax = row.get("perf_aday_eksi_m"), row.get("perf_basit_eksi_aday"), row.get("eksen_aday_eksi_basit")
    if interval(pm) and pm[1] < -d:
        return "geride", "Aday M'nin δ kadar gerisinde: kapalı kapı."
    if interval(pm) and interval(ax) and pm[0] > -d and ax[0] > e:
        return "A", "Sonuç A: aday M'ye göre eksik değil ve eksende en güçlü basit alternatiften en az ε önde."
    if interval(pb) and interval(ax) and pb[0] > -d and ax[1] < e:
        return "B", "Sonuç B: basit alternatif adaya göre eksik değil; adayın eksendeki ε kadar üstünlüğü dışlandı."
    if not (interval(pm) and interval(ax)):
        return "eksik", "Aralıklar eksik ([alt, üst] olarak, tools/aralik.py fark ile)."
    return "belirsiz", "Belirsiz: aralıklar ne A'yı ne B'yi gösteriyor (daha çok tohum ya da belirsiz diye yazılır)."


def aktarim_checks(s, add):
    at = s.get("aktarim") or {}
    add("M'nin darboğazı ölçüldü", "ok" if at.get("darbogaz") else "eksik",
        at.get("darbogaz") or "Kendi koşunda ölçülmüş bir darboğaz cümlesi yok (makaleden okunan hipotezdir).", "soru")
    miss = [n for n, k in (("eksen", "eksen"), ("ölçütü", "eksen_olcutu"), ("yönü", "eksen_yonu"),
                           ("performans yönü", "performans_yonu")) if not at.get(k)]
    add("Avantaj ekseni adaydan önce yazıldı", "ok" if not miss else ("uyari" if at.get("adaylar") else "eksik"),
        f"{at.get('eksen')} · {at.get('eksen_olcutu')} ({at.get('eksen_yonu')})" if not miss
        else "Eksik: " + ", ".join(miss) + (" (aday bunlardan önce yazılmış)" if at.get("adaylar") else ""), "soru")
    d, e = at.get("delta"), at.get("epsilon")
    m, t = arm_value(at, "M", "performans"), arm_value(at, "taban", "performans")
    if not (num(d) and num(e)):
        add("δ ve ε önceden yazıldı", "eksik", "δ (ana ölçütte eşdeğerlik payı) ve ε (eksende sayılan üstünlük) yok.", "soru")
    elif m is None or t is None:
        add("δ ve ε önceden yazıldı", "ok", f"δ = {d:g}, ε = {e:g} · δ ≤ ½·(M − taban) henüz denetlenemiyor (M ya da taban ölçülmedi).", "soru")
    else:
        half = abs(m - t) / 2
        add("δ ve ε önceden yazıldı", "ok" if d <= half else "durdu",
            f"δ = {d:g}, ε = {e:g} · ½·(M − taban) = {half:g}" + ("" if d <= half else " → δ çok geniş, eşdeğerlik kendiliğinden çıkar: DUR"), "soru")
    add("İki sonuç ön kaydı", "ok" if at.get("sonuc_a") and at.get("sonuc_b") else "eksik",
        f"A: {at.get('sonuc_a')} · B: {at.get('sonuc_b')}" if at.get("sonuc_a") and at.get("sonuc_b")
        else "A (alternatif yöntem) ve B (X gerekli mi?) cümleleri sonuçtan önce yazılmalı.", "soru")
    ba = [x for x in at.get("basit_alternatifler") or [] if isinstance(x, dict)]
    cheap = [x for x in ba if x.get("tur") == "ucuz_ek"]
    add("Basit alternatifler", "ok" if len(ba) >= 3 and cheap else ("uyari" if ba else "eksik"),
        (f"{len(ba)} aday" + ("" if cheap else "; \"M + ilkenin ucuz eki\" (tur: ucuz_ek) yok") + ("" if len(ba) >= 3 else "; en az 3 olmalı"))
        if ba else "Liste yok: en ucuz üç yol ve \"M + ilkenin ucuz eki\".", "uc_sayi")
    ad = [x for x in at.get("adaylar") or [] if isinstance(x, dict)]
    bad = [x.get("ad", "?") for x in ad if not (x.get("gerekce") and x.get("beklenen_bozulma"))]
    add("Adaylar", "ok" if ad and len(ad) <= 2 and not bad else ("uyari" if ad else "eksik"),
        (f"{len(ad)} aday: " + ", ".join(str(x.get("ad")) for x in ad) + (" · 2'den fazla aday: dönüş sayılır" if len(ad) > 2 else "")
         + (" · gerekçe ya da beklenen bozulma eksik: " + ", ".join(bad) if bad else "")) if ad else "Henüz aday yok (kollar ölçüldükten sonra).", "uc_sayi")
    need = at.get("tohum_gerekli")
    add("Tohum hesabı", "ok" if num(need) and at.get("tohum_hesabi") else "eksik",
        f"gereken {need} · {at.get('tohum_hesabi')}" if num(need) else "tools/aralik.py tohum ile hesaplanmalı (sd'nin üst sınırıyla).", "protokol")
    rows = [r for r in at.get("karsilastirmalar") or [] if isinstance(r, dict)]
    if not rows:
        add("Karşılaştırma sonucu", "eksik", "Henüz karşılaştırma yok.", "ana_kosu")
    else:
        code, text = outcome(at, rows[-1])
        st = {"A": "ok", "B": "ok", "geride": "uyari", "belirsiz": "uyari", "pilot": "uyari", "eksik": "eksik"}[code]
        add("Karşılaştırma sonucu", st, f"{rows[-1].get('aday')} ↔ {rows[-1].get('basit')}: {text}", "ana_kosu")


def checks(s):
    u, a = s.get("uc_sayi") or {}, s.get("asamalar") or {}
    out = []

    def add(name, status, detail, stage):
        if status != "ok" and not reached(s, stage) and a.get(stage, {}).get("durum", "bekliyor") == "bekliyor":
            status = "henuz"
        out.append((name, status, detail))

    ak = s.get("aile_kontrolu") or {}
    if not (ak.get("onceki_proje") and ak.get("taranan_kaynaklar")):
        add("Aile kontrolü", "eksik", "Yapılmamış: koşul, taranan kaynaklar ve önceki proje (eşleşme yoksa \"yok\") yazılmalı.", "soru")
    elif str(ak.get("onceki_proje")).strip().lower() == "yok":
        add("Aile kontrolü", "ok", f"{ak.get('kosul') or '?'}: eşleşme yok ({len(ak.get('taranan_kaynaklar'))} kaynak tarandı).", "soru")
    else:
        why = ak.get("bu_kez_neden_farkli")
        add("Aile kontrolü", "ok" if why else "eksik",
            f"{ak.get('kosul') or '?'} daha önce: {ak.get('onceki_proje')} ({ak.get('onceki_sonuc') or 'sonuç yazılmamış'}). "
            + (f"Bu kez: {why}" if why else "\"Bu kez neden farklı?\" öngörüsü yok: DUR."), "soru")
    if is_aktarim(s):
        aktarim_checks(s, add)
    else:
        q = s.get("soru") or {}
        olcut = (s.get("protokol") or {}).get("olcut")
        qmiss = [n for n, v in (("soru", q.get("metin")), ("koşul düzeyleri", q.get("kosul_duzeyleri")),
                                ("eşik", q.get("esik")), ("ölçüt", olcut)) if v in (None, "", [], {})]
        add("Kapı 1 sorusu ölçümden önce yazıldı", "ok" if not qmiss else ("uyari" if s.get("bozulma") else "eksik"),
            (f"{q.get('metin')} · düzeyler {q.get('kosul_duzeyleri')} · eşik {q.get('esik')} · ölçüt {olcut}") if not qmiss
            else "Eksik: " + ", ".join(qmiss) + (" (bozulma bunlardan önce yazılmış)" if s.get("bozulma") else ""), "soru")
        add("Bozulma ölçüldü", "ok" if s.get("bozulma") else "eksik", s.get("bozulma") or "Ölçülmüş bir bozulma cümlesi yok.", "soru")
        t = s.get("tez_cumlesi", {})
        add("Tez cümlesi donduruldu", "ok" if t.get("metin") and t.get("tarih") else "eksik",
            f"{t.get('metin')} ({t.get('tarih')})" if t.get("metin") else "Tez cümlesi yazılmamış.", "soru")
        rows = u.get("satirlar", [])
        full = rows and all(None not in (r.get("taban"), r.get("basit_care"), r.get("kahin")) for r in rows)
        seeds_ok = rows and all((r.get("tohum") or 0) >= 3 for r in rows)
        add("Üç sayı tam", "ok" if full and seeds_ok else "eksik",
            f"{len(rows)} koşul" + ("" if seeds_ok else "; en az bir satırda 3'ten az tohum: pilot, kapı geçirmez") if rows else "Ölçüm yok.", "uc_sayi")
        b4 = u.get("basit_care_yontemden_once")
        add("Basit çare yöntemden önce kuruldu", "ok" if b4 is True else ("uyari" if b4 is False else "eksik"),
            u.get("basit_care_tanimi") or "Basit çare tanımlanmamış.", "uc_sayi")
        if u.get("kahin_tanimi"):
            add("Adil kâhin tanımlı", "ok", u.get("kahin_tanimi"), "uc_sayi")
        elif u.get("kahin_tanimlanamaz"):
            add("Adil kâhin tanımlı", "uyari", "Tanımlanamaz: " + u.get("kahin_tanimlanamaz"), "uc_sayi")
        else:
            add("Adil kâhin tanımlı", "eksik", "Kâhinin neyi, ne zamandan itibaren bildiği yazılmamış.", "uc_sayi")
        add("Eşik önceden yazıldı", "ok" if u.get("esik") is not None else "eksik",
            f"δ = {u.get('esik')} {u.get('birim', '')}" if u.get("esik") is not None else "Eşik yok.", "uc_sayi")
        best, g = gap(u)
        if g is None:
            add("Boşluk (kâhin − basit çare)", "eksik", "Hesaplanamıyor.", "uc_sayi")
        else:
            esik = u.get("esik")
            st = "eksik" if esik is None else ("ok" if g >= esik else "uyari")
            msg = f"En büyük boşluk {g:g} {u.get('birim', '')} ({best.get('kosul')})"
            if esik is None:
                msg += " → eşik önceden yazılmamış, boşluk yorumlanamaz"
            else:
                msg += " → yöntem için yer var" if g >= esik else " → eşiğin altında, yöntem için yer yok"
            add("Boşluk (kâhin − basit çare)", st, msg, "uc_sayi")
    pr = s.get("protokol", {})
    missing = [k for k in ("karar_kurali", "olcut", "kilitli_test", "durma_kurali") if not pr.get(k)]
    add("Protokol yazılı", "ok" if not missing else "eksik",
        "Karar kuralı, ölçüt, kilitli test ve durma kuralı yazılı." if not missing else "Eksik: " + ", ".join(missing), "protokol")
    rk = s.get("rakipler", [])
    unfair = [r.get("ad", "?") for r in rk if not (r.get("butce_esit") and r.get("ayar_esit") and r.get("bilgi_esit"))]
    add("Rakip adaleti", "ok" if rk and not unfair else ("uyari" if unfair else "eksik"),
        ("Eşitlenmesi gereken: " + ", ".join(unfair)) if unfair else (f"{len(rk)} rakip, hepsi eşit" if rk else "Rakip listesi yok."), "rakip_adaleti")
    tp = s.get("tohum", {})
    plan, run = tp.get("plan", 0), tp.get("kosulan", 0)
    st = "eksik" if plan < 3 else ("ok" if run >= plan else ("uyari" if a.get("ana_kosu", {}).get("durum") in ("gecti",) else "henuz_ok"))
    tanim = tp.get("tanim") or ""
    if not tanim and st in ("ok", "henuz_ok"):
        st = "eksik"
    add("Tohum", "ok" if st == "henuz_ok" else st, f"plan {plan}, koşulan {run}" + (" (plan 3'ün altında)" if plan < 3 else "")
        + (f" · tohum: {tanim}" if tanim else " · tohumun ne olduğu yazılmamış (eğitim mi, değerlendirme mi)"), "protokol")
    d = s.get("donus", {})
    n, lim = len(d.get("kayit", [])), d.get("sinir", 3)
    add("Dönüş sayacı", "ok" if n < lim - 1 else ("uyari" if n == lim - 1 else "durdu"),
        f"{n} / {lim}" + (" · durma kuralı devrede" if n >= lim else (" · bir sonraki dönüş sınırda" if n == lim - 1 else "")), "soru")
    add("Benzetimin kusursuzlukları listelendi", "ok" if s.get("benzetim_kusursuzluklari") else "eksik",
        "; ".join(s.get("benzetim_kusursuzluklari", [])) or "Liste yok.", "gerceklik")
    gd = s.get("gercek_dunya_testi", {})
    plat = f"Platform: {gd.get('platform') or '?'}, erişim {gd.get('erisim') or '?'}, eşleşme: {gd.get('eslesme') or '?'}. "
    if gd.get("durum") == "yapilmayacak":
        add("Gerçek dünya testi", "uyari", plat + "Yapılmayacak: iddia benzetimle sınırlı (sınırlılık olarak yazılı olmalı).", "yeniden_uretim")
    else:
        add("Gerçek dünya testi", "ok" if gd.get("durum") == "yapildi" else ("uyari" if gd.get("plan") else "eksik"),
            plat + (gd.get("plan") or "Planlanmamış."), "yeniden_uretim" if not gd.get("erisim") else "gerceklik")
    add("Sınırlılıklar yazılı", "ok" if s.get("sinirliliklar") else "eksik", "; ".join(s.get("sinirliliklar", [])) or "Liste yok.", "yazim")
    sp = s.get("sapmalar", [])
    eksik = incomplete_sapmalar(sp)
    if eksik:
        add("Sapmalar", "uyari", f"{len(eksik)} sapma kaydı eksik (yer tutucu ya da boş gerekçe): "
            + "; ".join(str(x.get("tarih") if isinstance(x, dict) else x) for x in eksik)
            + ". Eskisini düzenleme; \"duzeltir\": \"<tarih>\" alanlı yeni kayıtla tamamla.", "okuma")
    else:
        add("Sapmalar", "ok", f"{len(sp)} sapma kayıtlı (bilgi: dürüst kayıt, uyarı değil)" if sp else "Sapma yok.", "soru")
    ov = s.get("overrides", [])
    add("Aşılan kapı kararları", "ok" if len(ov) < 2 else "uyari",
        f"{len(ov)} kez" + (" · ikinci kez aşıldı: danışmanla konuş" if len(ov) >= 2 else "") if ov else "Yok.", "soru")
    return out


def registry():
    """The registry list; [] when the file is missing; None when it exists but cannot be read."""
    if not os.path.exists(REGISTRY):
        return []
    try:
        with open(REGISTRY, encoding="utf-8-sig") as f:  # -sig: older kur.ps1 wrote a BOM
            reg = json.load(f)
        return reg if isinstance(reg, list) else None
    except Exception:
        return None


def lines_of(reg, kind):
    """Active lines of work of one kind. A project with "hatlar" counts each line, not the folder."""
    out = []
    for p in reg:
        if p.get("durum") != "aktif":
            continue
        hat = p.get("hatlar")
        if hat:
            out += [f"{p.get('ad')} / {h.get('ad')}" for h in hat if h.get("tur") == kind]
        elif p.get("tur") == kind:
            out.append(p.get("ad"))
    return out


def render(s, karar_path):
    a = s.get("asamalar") or {}
    current = next((k for k in ORDER if a.get(k, {}).get("durum", "bekliyor") != "gecti"), None)
    stages = STAGES_AKTARIM if is_aktarim(s) else STAGES
    cur = next((x for x in stages if x[0] == current), None)
    ch = checks(s)
    nbad = sum(1 for c in ch if c[1] in ("eksik", "durdu", "uyari"))
    reg = registry()
    active_main = lines_of(reg or [], "ana")
    active_side = lines_of(reg or [], "yan")
    sk = s.get("son_karar") or {}
    u = s.get("uc_sayi") or {}
    best, g = gap(u)
    def fmt(v):
        return "?" if v is None else f"{v:g}"
    if best:
        drop = f"{fmt(best.get('taban'))}"
        sentence = (f"[{esc(s.get('temel_yontem') or 'Yöntem')}], [{esc(best.get('kosul'))}] koşulunda tabanda {fmt(best.get('taban'))}. "
                    f"Kâhin {fmt(best.get('kahin'))}, en iyi basit çare {fmt(best.get('basit_care'))}. "
                    f"Geriye kalan {fmt(g)} {esc(u.get('birim', ''))} hedefimiz.")
    else:
        sentence = "[Yöntem], [koşul] altında [ölçüt]'te [X] kadar düşüyor. Kâhin [Y] kazandırıyor. En iyi basit çare [Z] kadarını kapatıyor. Geriye kalan [Y − Z] hedefimiz."

    stage_html = []
    for key, num, name, skill, q in stages:
        st = a.get(key, {})
        d = st.get("durum", "bekliyor")
        cls = d + (" now" if key == current else "")
        extra = f'<span class="sk">{esc(skill)}</span>' if skill else ""
        note = esc(st.get("not", ""))
        date = esc(st.get("tarih", ""))
        stage_html.append(
            f'<li class="st {cls}"><span class="dot" aria-hidden="true">{esc(num)}</span>'
            f'<div><div class="row"><b>{esc(name)}</b><span class="pill {d}">{STATUS_LABEL.get(d, d)}</span>{extra}</div>'
            f'<p class="q">{esc(q)}</p>' + (f'<p class="n">{date} · {note}</p>' if note or date else "") + "</div></li>")

    chk_html = []
    icon = {"ok": "✓", "uyari": "!", "eksik": "✕", "durdu": "✕", "henuz": "·"}
    lab = {"ok": "Tamam", "uyari": "Uyarı", "eksik": "Eksik", "durdu": "Durma kuralı", "henuz": "Henüz değil"}
    for name, st, det in ch:
        chk_html.append(f'<tr class="{st}"><td class="i" aria-hidden="true">{icon[st]}</td><td><b>{esc(name)}</b><br><span>{esc(det)}</span></td>'
                        f'<td class="l">{lab[st]}</td></tr>')

    rows = "".join(f"<tr><td>{esc(r.get('kosul'))}</td><td>{fmt(r.get('taban'))}</td><td>{fmt(r.get('basit_care'))}</td>"
                   f"<td>{fmt(r.get('kahin'))}</td><td><b>{fmt(None if None in (r.get('kahin'), r.get('basit_care')) else r['kahin'] - r['basit_care'])}</b></td>"
                   f"<td>{fmt(r.get('tohum'))}</td></tr>" for r in u.get("satirlar", [])) or '<tr><td colspan="6">Henüz ölçüm yok.</td></tr>'

    if is_aktarim(s):
        at = s.get("aktarim") or {}
        arm_rows = "".join(f"<tr><td>{esc(r.get('rol'))}</td><td>{esc(r.get('kol'))}</td><td>{fmt(r.get('performans'))}</td>"
                           f"<td>{fmt(r.get('eksen'))}</td><td>{fmt(r.get('tohum'))}</td><td>{'pilot' if r.get('pilot') else ''}</td></tr>"
                           for r in at.get("olcumler") or [] if isinstance(r, dict)) or '<tr><td colspan="6">Henüz ölçüm yok.</td></tr>'
        def iv(x):
            return f"[{x[0]:g}, {x[1]:g}]" if interval(x) else "?"
        cmp_rows = "".join(f"<tr><td>{esc(r.get('tarih'))}</td><td>{esc(r.get('aday'))}</td><td>{esc(r.get('basit'))}</td><td>{fmt(r.get('tohum'))}</td>"
                           f"<td>{iv(r.get('perf_aday_eksi_m'))}</td><td>{iv(r.get('perf_basit_eksi_aday'))}</td><td>{iv(r.get('eksen_aday_eksi_basit'))}</td>"
                           f"<td><b>{esc(outcome(at, r)[0])}</b></td></tr>"
                           for r in at.get("karsilastirmalar") or [] if isinstance(r, dict)) or '<tr><td colspan="8">Henüz karşılaştırma yok.</td></tr>'
        last = [r for r in at.get("karsilastirmalar") or [] if isinstance(r, dict)]
        code, text = outcome(at, last[-1]) if last else ("", "")
        if code == "A":
            res = esc(at.get("sonuc_a") or text)
        elif code == "B":
            res = esc(at.get("sonuc_b") or text)
        elif last:
            res = esc(text)
        else:
            res = ("[M], [koşul] altında [ölçüt]'te [değer]; darboğazı [eksen]'de [değer]. "
                   "A: aday M'ye göre en fazla δ geride ve eksende en güçlü basit alternatiften en az ε önde. "
                   "B: basit alternatif yetiyor; adayın eksendeki üstünlüğü ε'un altında.")
        main_section = f"""<section><h2>Kollar</h2><p class="muted">Darboğaz: {esc(at.get('darbogaz') or '—')} · Eksen: {esc(at.get('eksen') or '—')} ({esc(at.get('eksen_olcutu') or '?')}, {esc(at.get('eksen_yonu') or '?')}) · δ = {fmt(at.get('delta'))} · ε = {fmt(at.get('epsilon'))} · gereken tohum {fmt(at.get('tohum_gerekli'))}</p>
<div class="tw"><table class="num"><thead><tr><th>Rol</th><th>Kol</th><th>Performans</th><th>Eksen</th><th>Tohum</th><th></th></tr></thead><tbody>{arm_rows}</tbody></table></div></section>
<section><h2>Karşılaştırmalar (%90 aralıklar, pozitif = ilk kol daha iyi)</h2><div class="tw"><table class="num"><thead><tr><th>Tarih</th><th>Aday</th><th>Basit alt.</th><th>Tohum</th><th>Perf. aday − M</th><th>Perf. basit − aday</th><th>Eksen aday − basit</th><th>Sonuç</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
<div class="card"><span class="lbl">Sonuç cümlesi</span><p class="sent">{res}</p></div></section>"""
    else:
        main_section = f"""<section><h2>Üç sayı</h2><div class="tw"><table class="num"><thead><tr><th>Koşul</th><th>Taban</th><th>Basit çare</th><th>Adil kâhin</th><th>Kâhin − çare</th><th>Tohum</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted">Eşik δ = {fmt(u.get('esik'))} {esc(u.get('birim',''))} · Kâhin: {esc(u.get('kahin_tanimi') or '—')}</p>
<div class="card"><span class="lbl">Boşluk cümlesi</span><p class="sent">{sentence}</p></div></section>"""

    piv = "".join(f"<li>{esc(p.get('tarih'))}: {esc(p.get('neden'))}</li>" for p in s.get("donus", {}).get("kayit", [])) or "<li>Dönüş yok.</li>"
    sap = "".join(f"<li>{esc(p.get('tarih'))}: {esc(p.get('ne'))} <i>({esc(p.get('gerekce'))})</i></li>" for p in s.get("sapmalar", [])) or "<li>Sapma yok.</li>"
    ovr = "".join(f"<li>{esc(p.get('tarih'))}: {esc(p.get('kapi'))} {esc(p.get('karar'))} aşıldı <i>({esc(p.get('gerekce'))})</i></li>" for p in s.get("overrides", []))
    if ovr:
        sap += ovr
    if reg is None:
        focus = ('<div class="card warnc"><span class="lbl">Odak</span><p>Proje kaydı (~/.claude/arastirma/projeler.json) '
                 'okunamadı: geçerli bir JSON listesi değil. Odak sayılamıyor; kaydı düzelt.</p></div>')
    else:
        if not reg:
            focus = ('<div class="card warnc"><span class="lbl">Odak</span><p>Bu makinenin proje kaydı boş ya da yok. Başka makinede ya da kayıt '
                     'dışında aktif proje olabilir; ajan sormadan "tek proje" saymasın.</p></div>')
        else:
            names = ", ".join(esc(p) for p in active_main)
            side = ", ".join(esc(p) for p in active_side)
            warn = len(active_main) > 1 or len(active_side) > 1
            focus = (f'<div class="card {"warnc" if warn else ""}"><span class="lbl">Odak</span><p><b>{len(active_main)}</b> aktif ana proje: {names or "yok"}. '
                     f'<b>{len(active_side)}</b> yan iş: {side or "yok"}.'
                     + (" Kural: bir ana, bir küçük yan iş. Hangisi duruyor?" if warn else "") + "</p></div>")
    verdict = sk.get("karar") or "Henüz karar yok"
    vcls = {"DUR": "durdu", "KOŞULLU DEVAM": "kosullu", "DEVAM": "gecti"}.get(verdict, "bekliyor")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(s.get('proje'))} · durum</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@500&display=swap">
<style>
:root{{--bg:#f3f6f5;--paper:#fff;--fg:#17211f;--muted:#56635f;--accent:#0f6b63;--accent-soft:#e1eeeb;--rule:#d3dcd9;--warn:#8a4b12;--warn-soft:#f6ebdf;--bad:#9b2c2c;--bad-soft:#f7e3e1;
--fd:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;--fb:"Source Serif 4",Georgia,serif;--fm:"JetBrains Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root{{--bg:#101615;--paper:#161e1d;--fg:#e4ebe9;--muted:#9aa8a4;--accent:#5cbcae;--accent-soft:#1b2b29;--rule:#2a3633;--warn:#e2a368;--warn-soft:#2a2119;--bad:#ec8e86;--bad-soft:#2e1b1a;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--fb);font-size:17px;line-height:1.55;padding:40px max(16px,env(safe-area-inset-left)) 64px max(16px,env(safe-area-inset-right))}}
.wrap{{max-width:56rem;margin:0 auto;display:flex;flex-direction:column;gap:32px}}
h1{{font-family:var(--fd);font-size:clamp(1.8rem,5vw,2.6rem);line-height:1.1;margin:0}}h2{{font-family:var(--fd);font-size:1.3rem;margin:0}}
.eb{{font-family:var(--fm);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}}.muted{{color:var(--muted);font-size:15px}}
.top{{display:grid;grid-template-columns:1.2fr 1fr;gap:16px}}.card{{background:var(--paper);border:1px solid var(--rule);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:6px;min-width:0}}
.card.warnc{{border-color:var(--warn);background:var(--warn-soft)}}.lbl{{font-family:var(--fm);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.verdict{{font-family:var(--fd);font-size:1.6rem;font-weight:700}}.verdict.durdu{{color:var(--bad)}}.verdict.kosullu{{color:var(--warn)}}.verdict.gecti{{color:var(--accent)}}
.big{{font-family:var(--fd);font-size:1.25rem}}
ol.stages{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0;background:var(--paper);border:1px solid var(--rule);border-radius:12px}}
.st{{display:grid;grid-template-columns:2.2rem 1fr;gap:12px;padding:12px 16px;border-top:1px solid var(--rule)}}.st:first-child{{border-top:0}}
.st.now{{background:var(--accent-soft)}}.dot{{width:1.9rem;height:1.9rem;border-radius:50%;display:grid;place-items:center;font-family:var(--fm);font-size:13px;border:2px solid var(--rule);color:var(--muted)}}
.st.gecti .dot{{background:var(--accent);border-color:var(--accent);color:var(--paper)}}.st.kosullu .dot{{border-color:var(--warn);color:var(--warn)}}.st.durdu .dot{{border-color:var(--bad);color:var(--bad)}}
.row{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}.q{{margin:2px 0 0;color:var(--muted);font-size:15px}}.n{{margin:2px 0 0;font-size:14.5px}}
.pill{{font-family:var(--fm);font-size:11px;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:var(--bg);color:var(--muted)}}
.pill.gecti{{background:var(--accent-soft);color:var(--accent)}}.pill.kosullu{{background:var(--warn-soft);color:var(--warn)}}.pill.durdu{{background:var(--bad-soft);color:var(--bad)}}
.sk{{font-family:var(--fm);font-size:11px;color:var(--muted)}}
.tw{{overflow-x:auto;background:var(--paper);border:1px solid var(--rule);border-radius:12px}}table{{border-collapse:collapse;width:100%;font-size:15px}}
td,th{{text-align:left;padding:9px 12px;border-top:1px solid var(--rule);vertical-align:top}}tr:first-child td,thead th{{border-top:0}}th{{font-family:var(--fm);font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);font-weight:500}}
td span{{color:var(--muted);font-size:14px}}td.i{{width:2rem;font-family:var(--fm);font-size:15px;text-align:center}}td.l{{font-family:var(--fm);font-size:11.5px;text-transform:uppercase;white-space:nowrap}}
tr.ok td.i,tr.ok td.l{{color:var(--accent)}}tr.uyari td.i,tr.uyari td.l{{color:var(--warn)}}tr.eksik td.i,tr.eksik td.l,tr.durdu td.i,tr.durdu td.l{{color:var(--bad)}}tr.henuz td{{color:var(--muted)}}
.sent{{font-family:var(--fd);font-size:1.05rem;line-height:1.45}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}ul{{margin:0;padding-left:1.2rem}}
.num td{{font-variant-numeric:tabular-nums}}
@media (max-width:720px){{.top,.two{{grid-template-columns:1fr}}}}
</style></head><body><main class="wrap">
<header><span class="eb">Araştırma durumu · {esc(s.get('tur'))} proje · {'aktarım çalışması (iki sonuçlu)' if is_aktarim(s) else 'boşluk çalışması'}</span><h1>{esc(s.get('proje'))}</h1>
<p class="muted">{esc(karar_path)} · üretildi {now} · {nbad} açık uyarı ya da eksik</p></header>
<div class="top">
 <div class="card"><span class="lbl">Son karar ({esc(sk.get('tarih'))})</span><span class="verdict {vcls}">{esc(verdict)}</span><p>{esc(sk.get('neden'))}</p>
 <p><b>Sıradaki adım:</b> {esc(sk.get('siradaki_adim') or '—')}</p></div>
 <div class="card"><span class="lbl">Şu an buradayız</span><span class="big">{esc(cur[2]) if cur else 'Bütün aşamalar geçti'}</span>
 <p class="muted">{esc(cur[4]) if cur else ''}</p>{('<p class="muted">Skill: ' + esc(cur[3]) + '</p>') if cur and cur[3] else ''}</div>
</div>
{focus}
<section><h2>Aşamalar</h2><ol class="stages">{''.join(stage_html)}</ol></section>
<section><h2>Yeterlilik denetimleri</h2><div class="tw"><table><tbody>{''.join(chk_html)}</tbody></table></div></section>
{main_section}
<div class="two"><section class="card"><span class="lbl">Dönüşler ({len(s.get('donus',{}).get('kayit',[]))} / {s.get('donus',{}).get('sinir',3)})</span><ul>{piv}</ul></section>
<section class="card"><span class="lbl">Sapmalar ve aşılan kararlar</span><ul>{sap}</ul></section></div>
</main></body></html>"""


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "karar.json"
    if not os.path.exists(path):
        print(f"{path} yok. Bu proje kararlarını başka bir düzende tutuyor olabilir; panel için önce proje-baslat ile "
              "karar.json ekle (projenin kendi dosyaları değişmez).")
        return 1
    with open(path, encoding="utf-8-sig") as f:
        s = json.load(f)
    out = os.path.join(os.path.dirname(os.path.abspath(path)), "durum.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(s, os.path.basename(os.path.dirname(os.path.abspath(path))) + "/karar.json"))
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
