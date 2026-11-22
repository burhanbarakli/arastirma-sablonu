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
ORDER = [s[0] for s in STAGES]
STATUS_LABEL = {"gecti": "Geçti", "kosullu": "Koşullu", "durdu": "Durdu", "bekliyor": "Bekliyor"}
REGISTRY = os.path.expanduser("~/.claude/arastirma/projeler.json")


def esc(x):
    return html.escape("" if x is None else str(x))


def reached(state, stage):
    """True when every stage before `stage` has at least started (not 'bekliyor')."""
    i = ORDER.index(stage)
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
    cur = next((x for x in STAGES if x[0] == current), None)
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
    for key, num, name, skill, q in STAGES:
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
<header><span class="eb">Araştırma durumu · {esc(s.get('tur'))} proje</span><h1>{esc(s.get('proje'))}</h1>
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
<section><h2>Üç sayı</h2><div class="tw"><table class="num"><thead><tr><th>Koşul</th><th>Taban</th><th>Basit çare</th><th>Adil kâhin</th><th>Kâhin − çare</th><th>Tohum</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted">Eşik δ = {fmt(u.get('esik'))} {esc(u.get('birim',''))} · Kâhin: {esc(u.get('kahin_tanimi') or '—')}</p>
<div class="card"><span class="lbl">Boşluk cümlesi</span><p class="sent">{sentence}</p></div></section>
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
