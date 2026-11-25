---
name: zayif-nokta-raporu
description: Weak-point report for a research paper, before reproducing it ("step 0"). Use when the user gives one or more papers (PDF path, arXiv/OpenReview/DOI link or title) and wants to know where the method may break, what it assumes, which constants were hand-picked, which conditions were never tested, whether results sit at the ceiling, what reviewers and GitHub issues say, or wants an assumption table across several papers of a new field. Triggers include "zayıf nokta raporu", "makaleyi zorla", "nerede bozulur", "varsayım tablosu", "0. adım", "weak points of this paper", "where does this method break". Also has an explained reading mode (anlatımlı okuma): the agent reads the paper and finds the weak points itself, then walks the user through them one at a time, each with the exact place to read ("şurayı oku"), so the user studies only the spots that matter; no quizzing: use it for "anlatarak oku", "anlatımlı okuma", "şurayı oku de", "birlikte okuyalım", "rehberli oku", "rehberli okuma", "zayıf noktaları anlat". Also has a field survey mode for literature search on a topic: use it for "alan taraması", "literatür tara", "makale ara", "bu konuda ne var", "alanı tanımak istiyorum", "temel makale bul", "bunu kim çözmüş", for a candidate pool of recent or other-field methods in a method-transfer study ("aday yöntem ara", "güncel yöntemler", "hangi yeni yöntem buna uyar", "aday havuzu"), and for a bottleneck map before any project exists ("ön keşif", "darboğaz haritası", "alternatif yöntem için fikir ver", "nereden başlasam"). Not for summarising a paper or writing a review of the user's own manuscript.
---

# Zayıf nokta raporu (0. adım)

Goal: before anyone spends weeks reproducing a paper, find where its method is most likely to break, with every claim
pinned to a place in the source, and end with the research-gap sentence the user can fill in. Write the report in the
user's language (Turkish unless they write in another language).

## Ground rules (apply to every step)

1. **Work from sources, not memory.** Read the PDF (Read tool with `pages`, 20 pages per call), the official code,
   the review page and the issues page. Never describe a paper from memory. If a source cannot be opened, say so in
   the report and skip what depends on it.
2. **Every claim gets a location and a short quote** (section or page, and at most one sentence quoted). After
   drafting, re-open each cited place and check the quote is really there; drop or mark any claim you cannot verify.
3. **Do not take the user's hypothesis as the question.** If the user says "I think it breaks under delay", still
   run the full search and report what the sources show, including evidence against their hunch. Ask "where does it
   break?", never "does it break where I think?".
4. **Say "emin değilim" (not sure) where you are not sure.** An honest gap beats a confident guess.
5. **Every external paper you mention must exist.** Verify each one through the Semantic Scholar API or its DOI /
   arXiv page before listing it (`verify_reference` where available), and give the link. Never list a paper you have
   not opened; a row whose identifier does not resolve goes to "Doğrulanamayanlar", not into a table.
5b. **No absence claims.** Never write "kimse uygulamamış", "daha önce denenmemiş" or "not applied before": an agent
   cannot prove an absence. Write a query record instead: date, the queries, the databases, the number of hits and the
   three closest papers. Agreement between two agents is not evidence either; only a verified quote (page and
   sentence) or a measured number is.
5c. **Live search for anything recent.** Never propose recent methods from memory. Search arXiv and OpenAlex for the
   last 24 months and write the search date; without web access, write "son 24 ay taranmadı".
6. **Privacy.** Send only public identifiers (paper title, arXiv id, DOI, repo name) to outside services. Never send
   the user's own unpublished ideas, drafts or data.
7. **Park method ideas.** If a method idea comes up during reading or a survey (from the user or from you), write it
   in one line under "Fikirler (park edildi)" and do not develop it. Methods come only after Kapı 3 of
   `arastirma-kapisi` (in a method-transfer study, `calisma_turu: aktarim`, after Kapı A3, through purpose D of the
   field survey).
8. **The user picks the problem.** End with the top three weak points, each with its cheapest experiment, and let the
   user choose; do not choose for them. A drop seen in a paper, a toy or a derivation is a hypothesis for Kapı 1, not a
   measured failure.
9. **Resource fit.** Read `kaynak.json` in the personal folder (its path is in
   `~/.claude/arastirma/kisisel_yolu.txt`; a missing file or empty lists mean no limit). For every paper that may
   become a base paper or an experiment, record what running it needs: training or fine-tuning or only a released
   checkpoint, the GPU memory for that, the operating system, and graphics or driver needs (for example a renderer
   that needs Vulkan or OpenGL on the GPU). A paper that matches an item in `izin_yok` stays in the map and the
   tables, marked with the reason, but is never offered as a base paper or experiment candidate. A paper that matches
   `ilk_tercih_degil` goes last among those candidates; say so in one line with the reason. Items in `izin_verilen`
   (for example a Linux subsystem the machine has) count as fitting. Unknown needs are marked "?" and checked in the
   code's README or issues before the paper is recommended.

## Three modes

- **Rapor modu** (default): the steps below, ending in a written report.
- **Alan taraması modu**: when the user wants to search the literature on a topic, get to know a field, find a base
  paper to stress, or find who already solved a property. See "Alan taraması modu" near the end.
- **Anlatımlı okuma modu**: when the user wants to go through the paper together, be told where to read, or have the
  weak points explained ("anlatarak oku", "şurayı oku de", "birlikte okuyalım", "rehberli oku"). You do the reading and
  find the weak points; the user reads only the places you point to. See "Anlatımlı okuma modu" near the end.

## Inputs to collect

Ask only for what is missing and cannot be found:
- the paper(s): local PDF path, or a link / title you can resolve;
- optionally the official code repository, and the OpenReview forum if the venue uses it;
- optionally what the user wants to push on (task, deployment setting). Use it to prioritise, not to filter.

For a new field (several papers), go to "Assumption table" after running steps A1–A5 on each paper in a shorter form.

## Step A: inside the paper (one pass per paper)

A1. **What is not shown.** List the experimental conditions: what was varied, what was held fixed, number of seeds or
trials, error bars or intervals, and whether a simple baseline (fixed setting, hand rule, classical method) is
compared. A condition that never changes is a candidate weak point.

A2. **Assumptions.** List explicit assumptions ("we assume…") and implicit ones (perfect sensing, no delay, known
geometry, i.i.d. data, fixed horizon, clean labels, a given model of the environment…). For each: where it appears,
and when it would fail in practice.

A3. **Hand-picked constants.** Every value chosen by hand, by trial and error, or "empirically": what it is, how it was
chosen, and whether the best value would plausibly change with conditions.

A4. **Ceiling check.** Collect the headline success rates / scores. Flag any task already near the ceiling (for
example above 95%): there is little left to improve there.

A5. **Appendix and supplementary.** Failure cases, tuning details, compute cost, anything that contradicts or narrows
the main text.

## Step B: around the paper

B1. **Reviews.** If an OpenReview forum exists, fetch it (web page, or `https://api2.openreview.net/notes?forum=<id>`).
Separate the weaknesses reviewers raised from those the authors answered convincingly, and list the ones left
unanswered.

B2. **GitHub issues of the official code.** `gh api "repos/<owner>/<repo>/issues?state=all&per_page=100"` (paginate if
needed). Group reported problems: cannot reproduce, crashes, fails on other data or conditions, undocumented settings.
Count each group and quote one representative issue with its link.

B3. **Citing papers.** Semantic Scholar:
`https://api.semanticscholar.org/graph/v1/paper/<arXiv:id or DOI:doi>/citations?fields=title,year,externalIds,url&limit=100`.
Pick the ones that use this method as a baseline (title/abstract mention comparison, benchmark, or "outperform").
Open the most relevant few and record where this method lost and by how much. Link each one.

B4. **Benchmark status.** If the paper reports on a public benchmark, check whether results on it have stalled (a
saturated benchmark leaves little headroom) or whether a hard variant shows large drops.

## Step C: cheap checks (propose, and run only if the user agrees)

C1. **Paper-and-pencil analysis.** From the method's equations, what happens as a key quantity grows (delay, noise,
step size, horizon, data scarcity)? Is there a stability or validity limit? Derive it step by step and say how to
check it numerically.

C2. **Toy version.** Outline (or, if asked, write) a minimal 2-D or small-data version of the core idea that can be run
in an afternoon, with three policies: baseline, simple hand rule, and a fair oracle that knows the hidden quantity but
only what the method could observe, and only from when it could observe it. An unfair oracle inflates the gap.

C3. **Targeted run of the official code.** Name the two or three stress conditions most worth trying with the
released code and checkpoints, instead of a full reproduction. Prefer runs that fit `kaynak.json` (ground rule 9).

## Assumption table (several papers, new field)

Make one table: rows are papers, columns are the assumptions and practices found in A1–A2. Fix the columns before
reading, from a general list (for example: perfect sensing?, delay modelled?, known geometry?, real robot / real
data?, simple baseline?, number of seeds, target data amount), never from the user's suspected condition alone. Mark
each cell from the paper, with a location. Then list **every** column that (almost) every paper marks the same way,
ranked by how likely it is to break the methods and how cheap it is to test; each is a candidate blind spot. Spot-check
by re-reading two papers' rows against the PDFs.

## Report

Save the report as a Markdown file next to the paper, or in the current directory, named
`zayif-nokta-<short-paper-name>.md`, and show its path. Structure:

1. **Özet:** three to five most promising weak points, each one line, ranked by how likely they are to break the
   method and how cheap they are to test. Any weak point that goes against the user's suspicion stays in.
1b. **Değerlendirilecek iddialar:** each Özet item again as a claim block with the exact place to read, so the user
   can check it in the paper. Judging the claims is optional; the "Senin değerlendirmen" lines may stay empty:

   ```markdown
   ### İddia N: <one sentence>
   Dayanak: <location and short quote>
   Kaynak türü: makalede yazıyor | dış kaynak (link) | ajanın kendi çıkarımı
   Ajanın güveni: yüksek | orta | düşük, with one reason
   Denetçi: doğrulandı | alıntı hatalı | akıl yürütme zayıf | abartılı, with one reason

   Senin değerlendirmen: [ ] doğru  [ ] yanlış  [ ] abartılı  [ ] emin değilim
   Makalede kontrol ettiğin yer:
   Önemli mi, test etmeye değer mi:
   ```

   Mark "ajanın kendi çıkarımı" honestly for anything derived rather than read (bounds from equations, guesses about
   behaviour); those are the claims most worth checking by hand.
2. **İçeride (A1–A5):** tables with location and quote for every row.
3. **Çevresinde (B1–B4):** grouped findings with links.
4. **Ucuz denemeler (C1–C3):** proposals, marked "önerildi" or "yapıldı".
5. **Varsayım tablosu** (when several papers).
6. **Boşluk cümlesi:** the template below, filled as far as the evidence allows, with `?` where a number still needs
   a measurement:

   > "[Yöntem], [koşul] altında [ölçüt]'te [X] kadar düşüyor. Sorunun kaynağını bilen bir kâhin [Y] kazandırıyor. En
   > iyi basit çare bunun [Z] kadarını kapatıyor. Geriye kalan [Y − Z], bizim hedefimiz."

7. **Doğrulanamayanlar:** every claim you could not verify, and every source you could not open.
8. **Fikirler (park edildi):** method ideas that came up, one line each, not developed.

End the reply with the top three weak points, each with the cheapest experiment that would measure it (baseline,
simple rule and fair oracle), and let the user pick one (ground rule 8). Do not start any experiment without the
user's go-ahead.

**Independent reader.** When a subagent tool is available, let a separate agent do the reading and drafting (steps
A–C and the report). Give it only the paper, the official code and review links, and this skill's rules, not the
conversation and not the user's hypothesis, so it does not confirm anyone's hunch. Then check its quotes yourself
(ground rule 2) before showing the report.

**Verifier.** After the reader's draft, start one more separate agent as verifier. Give it the paper, the code and
review links and the draft report, not the conversation. Its tasks, per claim block:
- quote and location: is the quoted sentence really at that place?
- reasoning: for "ajanın kendi çıkarımı" claims, check the derivation step by step; flag overstatement ("bozulur"
  where only "bozulabilir" is supported);
- coverage: list at most three weak points the reader missed, each with location and quote.
Add one line to each claim block: `Denetçi: doğrulandı | alıntı hatalı | akıl yürütme zayıf | abartılı` with one
sentence why, and put the verifier's additions under a short "Denetçinin eklediği" list (each also as a claim block).
Fix plain quote errors before showing the report and say which ones were fixed. Keep it to one verifier: agreement of
two agents is not proof, since they share blind spots; the last checks are the user and the experiment. Say this once
in the report header.

**If the user judges any claims** (optional, in any mode). When the user brings filled claim blocks back:
- for every "doğru" without a checked location, ask where they checked it;
- where the user marks a claim "yanlış" or "abartılı", re-open the source and say plainly who is right; a claim the
  agent got wrong is a good catch, say so;
- append a block to `okuma-gunlugu.md` (project root or current directory): date, paper, each claim with the agent's
  source type and confidence, the user's verdict, and whether the verdict held up. Over several papers this shows how
  often agent claims of each source type fail and how well the user catches them.

## Anlatımlı okuma modu

Goal: the user understands the paper and its weak points quickly. You do the reading and the finding; the user reads
only the places that matter and works on them. Do not quiz the user, do not wait for them to discover things, and do not
use a hint ladder.

1. **Read first, independently.** When a subagent tool is available, the independent reader and the verifier from the
   "Report" section do the reading (steps A1–A5, B1–B3, B4 if cheap), with the same inputs: the paper, code and review
   links and this skill's rules, never the conversation or the user's hypothesis. You only order and explain what they
   return. Without subagents, read it yourself and say once that the reading was not independent. Either way, re-open
   every place you will cite and check the quote is there (ground rule 2).
2. **Order.** Rank the findings as in the report's Özet: how likely each is to break the method, and how cheap it is to
   test. Do not rank by the user's suspected condition or the gate they plan next (ground rule 3). Aim for 5–8
   findings per paper. Always keep: any finding that goes against the user's suspicion, any simple rival that beat or
   matched the method (A1, B3), seeds and ceiling problems (A1, A4). Findings left out are listed in one line at the
   end.
3. **One at a time.** Present one finding (or two or three short related ones) per message, each as:
   - **Bulgu:** one sentence.
   - **Oku:** the exact place (section and paragraph, table or figure, page) and what to look for there, with at most
     one quoted sentence.
   - **Neden önemli:** one to three plain sentences. Explain any term the user may not know (for example a
     correlation measure, a benchmark-specific metric, a checkpoint) in a sentence, with a tiny worked example when it
     helps; label made-up numbers as made up.
   - **Kaynak türü:** makalede yazıyor | dış kaynak (link) | ajanın kendi çıkarımı. Mark derived claims clearly.
   Then stop so the user can read that place. Continue on "devam" or answer their question first. If the user raises
   a point that is not on your list, check it in the source; if it holds, add it and say so plainly.
4. **Wrap up.** After the last finding, give one table of all findings (Ne | Yeri | Neden önemli | Kaynak türü |
   Denetçi), the one-line list of findings left out, "Doğrulanamayanlar" and "Fikirler (park edildi)". Then the gap
   sentence from the report (item 6), with `?` for every number not yet measured; then the top three weak points, each
   with the cheapest experiment that would measure it (baseline, simple rule and fair oracle), and let the user pick.
   Say that Kapı 1 needs that measured drop. Do not start anything without the user's go-ahead. Offer to save the
   table as `zayif-nokta-<kısa-ad>.md`.

All ground rules still apply: quotes are checked in the source, and anything you derive yourself (like a bound from
the equations) is labelled as yours. A derived or unverified finding is a hypothesis to measure, never a measured
failure: it does not go into `karar.json` `bozulma` until the drop is measured.

## Alan taraması modu

Goal: a verified, bounded map of a topic that ends in a base paper to stress or a blind spot, never in "nobody has
done X". The user's record: literature search tended to end in a method idea; keep it on problems.

1. **Purpose first.** Ask which one, if not clear:
   - **A. Temel makale:** find the method to stress (current best or most used for the task) → 1–2 papers, then the
     normal report.
   - **B. Alanı tanımak:** 5–10 core papers → assumption table and blind spot.
   - **C. Kim çözmüş:** a field-free property sentence from method search (arastirma-kapisi) → candidates from any
     field.
   - **D. Aday havuzu (aktarım):** in a method-transfer study after Kapı A3: M, its measured bottleneck, the advantage
     axis and the field-free property sentence → recent methods (about the last two years) and classical ones from
     any field that have that property. Precondition: `aktarim.eksen`, `delta`, `epsilon` and both outcome sentences
     are committed; if not, say so and stop (the axis comes before the candidates). The table holds at least one
     classical tool (more than 5–10 years old, or the standard tool of its field).
   - **E. Darboğaz haritası (ön keşif):** before any project exists, to choose where to measure: for a task or
     field, the strong methods M in use and their known, measurable bottlenecks. It is a side task with a time box of
     one to two sessions. See "Darboğaz haritası (E)" below; it never names candidate methods.
2. **Search sentence, not a method name.** Write it with the user: task + condition (e.g. "policies that learn
   contact-rich insertion under noisy force sensing"), plus an optional field-free property sentence. A method name
   in the sentence locks the search onto that method; say so if the user proposes one.
3. **Seeds.** Two or three known papers or a survey from the user; otherwise find candidates with `search_works` /
   `paper-search` (OpenAlex) and arXiv, and let the user pick.
4. **Snowball.** For each seed, backward (its references) and forward (papers citing it) with `citation_neighbours`
   (OpenAlex) or the Semantic Scholar API; add keyword searches with the sentence. Use `deep-research` only for a wide
   sweep. Record which papers were expanded.
5. **Triage table** from title and abstract, one row per candidate: paper (year, venue, link) | task | what is varied |
   simple baseline? | real robot / real data? | seeds | code | resource fit (ground rule 9). Mark unknown cells "?".
   For D the columns are: method (paper, year, link) | field | principle | why it should move the axis (one
   sentence) | where it should be worse | assumptions that may fail here | already applied to this task? | resource
   fit | code. For D, the candidates come from an agent that does not see the user's favourite (when a subagent tool
   is available); the user's own candidates join the table. Record which fields were searched.
6. **Core and depth.** Pick 5–10 with the user (purpose A: 1–2). For B, fill the assumption table from the PDFs (the
   "Assumption table" section above) and name the blind spot. For A, hand over to the normal report. For C, run the
   transfer check in arastirma-kapisi on each candidate. For D, hand the table to "Aday seçimi" in arastirma-kapisi
   (devil's advocate, at most two candidates, toy test); do not pick for the user.
7. **Verify existence.** Every paper listed is checked through OpenAlex, arXiv or its DOI (`verify_reference` where
   available) and linked. Nothing from memory. Unverifiable items go to "Doğrulanamayanlar".
8. **Stop rule.** Agree a time box (default: one to two working sessions). Stop when new papers add no new column
   value or finding to the table (saturation), and write which rounds added nothing.

Save as `alan-taramasi-<short-topic>.md`: purpose, search sentence, seeds, snowball log, triage table, core list,
assumption table and candidate blind spots (B), stop note, Doğrulanamayanlar, Fikirler (park edildi). End with one next step: for A the weak-point
report on the chosen paper; for B "the blind spot is a candidate problem, not a problem yet: pick a method it would
break and measure the drop" (Kapı 1); for C the transfer check. If the conclusion drifts to "kimse yapmamış", say
plainly that this is mistake 1 and give the Kapı 1 step instead.

## Darboğaz haritası (E)

Goal: a map of where a strong method M is measurably weak, so the user can pick one bottleneck to measure at Kapı A1
of a method-transfer study. It is built so the pick is made by the bottleneck, not by a method the user likes.

1. **Blind builder, fixed brief.** When a subagent tool is available, one agent builds the map. It gets only this
   brief, filled in and otherwise unchanged; it never gets the conversation, the personal folder's path or files,
   `gecmis.md`, `kapali_kapilar.json` or the user's favourite method. Before filling it, remove any method name
   from the user's task line (it goes to `fikirler-park.md`).
   ```
   Görev / alan: <görev, yöntem adı olmadan>
   Kaynak dönemi: <bugünün tarihi> itibarıyla son 24 ay canlı tarama, ve alanın standart güçlü yöntemleri (M).
   İş: zayif-nokta-raporu skill'inin "Darboğaz haritası (E)" bölümündeki 2., 3., 4. ve 7. adımları uygula.
   Kurallar: Tabloya yöntem ya da yöntem ailesi adı yazma; karşılaştığın her yöntem adını ayrı bir park listesine
   koy. Darboğaz kaynağı yalnız M'nin kendi makalesi, resmi kodunun issue'ları ve M'yi içeren benchmark
   sonuçlarıdır; her satır yer ve kısa alıntıyla bir hipotezdir. "Kimse yapmamış" yazma. Kullanıcının tercihlerini,
   geçmiş projelerini ya da bu konuşmayı bilmiyorsun; sorma, tahmin etme. Kapalı kapı sütununu boş bırak.
   Çıktı: tablo, elenenler, Doğrulanamayanlar, park listesi.
   ```
   The map file starts with a section "Ajana verilen girdi" holding the filled brief word for word, so the
   blindness can be checked later. After the agent returns, search the table for every name in the park list; a
   hit moves to the park file. This hides the user's preference from the agent; it does not remove the agent's own
   prior knowledge, which is why the sources are restricted (step 2).
2. **Sources of a bottleneck.** Only M's own paper (limitations, failure tables, appendix), the official code's
   issues, and benchmark results that include M. A sentence in a newer method's paper saying "M is weak at X" is
   not a source. Each bottleneck is a hypothesis with a location and a short quote.
3. **Columns, one row per (M, bottleneck):** M (paper, year, link) | bottleneck hypothesis (quote and page) |
   cheapest measurement (condition, metric, rough cost) | known simple remedy | needs training, or measurable with
   a released checkpoint and paired evaluation seeds | resource fit (`kaynak.json`) | a current line of work targets
   this bottleneck: var / yok (one verified source, no method names) | closed-door flag (filled in step 4).
   The training column matters: under a seed cap, Sonuç A can be shown only for M and candidate pairs that need no
   training (Kapı A5 of `arastirma-kapisi`).
4. **No method names.** Candidate methods and method families never appear in the map. Any method name the builder
   meets goes into a separate file `fikirler-park.md` (one line each), which stays closed until Kapı A3 of the
   project and is opened only by purpose D.
5. **Family check per row (separate pass).** After the builder finishes, run the family check of
   `arastirma-kapisi` (Step 0.4: `kapali_kapilar.json` in the personal folder, memory, registry, earlier decision
   files) on every row. A row that touches a closed door is marked; it stays only with a numbered "bu kez neden
   farklı" prediction, otherwise it is struck.
6. **The pick.** The user picks one row and writes the reason in the language of use ("[kullanım] için [hedef]
   gerekir"), not in the language of a method. The pick goes into the new project's `karar.json` as
   `aktarim.on_kesif` (`harita`, `secilen_satir`, `olcut`, `gerekce`, `tarih`) and is committed before the first
   measurement. The row's metric becomes `aktarim.eksen_olcutu` at Kapı A1 unchanged; a different metric is a
   Sapma. Going back to the map for another row is a pivot.
7. **Verify and stop.** Every paper is verified (ground rule 5); the time box and saturation rule of the field survey
   apply.

Save as `darbogaz-haritasi-<short-topic>.md`: Ajana verilen girdi, task, sources searched with dates, the table, struck rows with the
closed door they touch, Doğrulanamayanlar. `fikirler-park.md` is saved beside it. End with: "Bir satır seç, gerekçeyi
kullanım diliyle yaz; ölçüm Kapı A1'de." Do not pick for the user.

## Blind audit (optional, on request)

When the user has reached a conclusion and wants it checked, start a separate subagent that receives the paper, the
code and the data but not the user's conclusion, and asks it to recompute the result and find errors. Report where it
agrees and disagrees.
