---
name: zayif-nokta-raporu
description: Weak-point report for a research paper, before reproducing it ("step 0"). Use when the user gives one or more papers (PDF path, arXiv/OpenReview/DOI link or title) and wants to know where the method may break, what it assumes, which constants were hand-picked, which conditions were never tested, whether results sit at the ceiling, what reviewers and GitHub issues say, or wants an assumption table across several papers of a new field. Triggers include "zayıf nokta raporu", "makaleyi zorla", "nerede bozulur", "varsayım tablosu", "0. adım", "weak points of this paper", "where does this method break". Also has a guided reading mode that coaches the user to find weak points themselves instead of handing over a report: use it for "rehberli oku", "rehberli okuma", "birlikte okuyalım", "okurken bana soru sor", "ipucu ver", "zayıf nokta bulmayı öğrenmek istiyorum". Not for summarising a paper or writing a review of the user's own manuscript.
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
   arXiv page before listing it, and give the link. Never list a paper you have not opened.
6. **Privacy.** Send only public identifiers (paper title, arXiv id, DOI, repo name) to outside services. Never send
   the user's own unpublished ideas, drafts or data.

## Two modes

- **Rapor modu** (default): the steps below, ending in a written report.
- **Rehberli okuma modu**: when the user asks to read together, to be asked questions, for hints, or to learn to find
  weak points. The user finds the weak points; you coach. See "Rehberli okuma modu" near the end. If the user has not
  read the paper yet and only asks for "zayıf nokta raporu", mention once that guided mode exists, then do what they
  asked.

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
in an afternoon, with three policies: baseline, simple hand rule, and an oracle that knows the hidden quantity.

C3. **Targeted run of the official code.** Name the two or three stress conditions most worth trying with the
released code and checkpoints, instead of a full reproduction.

## Assumption table (several papers, new field)

Make one table: rows are papers, columns are the assumptions and practices found in A1–A2 (for example: perfect
sensing?, delay modelled?, real robot / real data?, simple baseline?, number of seeds). Mark each cell from the paper,
with a location. Then state the **blind spot**: the column that (almost) every paper marks the same way. Spot-check by
re-reading two papers' rows against the PDFs.

## Report

Save the report as a Markdown file next to the paper, or in the current directory, named
`zayif-nokta-<short-paper-name>.md`, and show its path. Structure:

1. **Özet:** three to five most promising weak points, each one line, ranked by how likely they are to break the
   method and how cheap they are to test.
1b. **Değerlendirilecek iddialar:** each Özet item again as a claim block the user will judge against the paper. The
   user reads the report openly (it is not hidden), and judging each claim is part of their training:

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

End the reply with the single most promising weak point and the cheapest experiment that would measure it (baseline,
simple rule and fair oracle). Do not start that experiment without the user's go-ahead.

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

**After the user judges the claims.** When the user brings the filled claim blocks back:
- for every "doğru" without a checked location, ask where they checked it;
- where the user marks a claim "yanlış" or "abartılı", re-open the source and say plainly who is right; a claim the
  agent got wrong is a good catch, say so;
- append a block to `okuma-gunlugu.md` (project root or current directory): date, paper, each claim with the agent's
  source type and confidence, the user's verdict, and whether the verdict held up. Over several papers this shows how
  often agent claims of each source type fail and how well the user catches them.

## Rehberli okuma modu

Goal: the user learns to see weak points. Do not hand over findings; every weak point the user finds alone is worth
more than one you list.

1. **Prepare silently.** Read the paper yourself first (step A, and B if cheap) so you know what there is to find,
   with locations. Do not show this list.
2. **Start.** Suggest 30–45 minutes of reading alone first, keeping the table *Ne / Makaledeki yeri / Şüphem*. If the
   user already has a table, take it and go to step 5. If they found nothing alone, that is normal: start step 3.
3. **Section by section.** The user reads one section (abstract and experiments first, then method, appendix,
   limitations last). After each, ask one to three short questions built on the A1–A5 lenses, without the answer:
   - A1 *gösterilmeyen*: "Bu deneyde hiç değişmeyen ne var?" "Kaç tohum, hangi rakip?"
   - A2 *varsayım*: "Yazarlar neyi basitlik için dışarıda bırakıyor?"
   - A3 *elle seçilen*: "Değeri verilmeyen sabit var mı? Hangisi sonucu en çok etkiler?"
   - A4 *tavan*: "Bu sayı iyileştirmeye ne kadar yer bırakıyor?"
   - A5 *ek*: "Ekte ana metni daraltan bir şey var mı?"
   Answer feedback is short and specific: "doğru", "yarısı doğru: şuraya bir daha bak", or "bunu ben görmemiştim"
   (say this honestly when the user finds something outside your list, and verify it in the source).
4. **Hint ladder.** When the user is stuck, give one level at a time, only on request or after a wrong attempt:
   (1) *yer*: the section, page or figure; (2) *tür*: the kind of weakness (a rate limit, a missing rival, an untested
   condition…); (3) *cevap*: the weak point, with location and a short quote. Note the level at which each one was
   found.
5. **Compare.** Put the user's list next to yours. For each missed item, say which lens would have caught it and why
   it was easy to miss. Credit what the user found that you did not.
6. **Reading log.** Append one block to `okuma-gunlugu.md` in the project root (or the current directory): date,
   paper, and for each weak point: found alone / found at hint level 1–3 / missed, with its lens (A1–A5). After a few
   papers, point out the lens the user misses most and suggest looking there first next time.
7. **Then the report**, if the user wants it: run steps B and C and write the normal report, marking which items the
   user found.

All ground rules still apply: quotes are checked in the source, and anything you derive yourself (like a bound from
the equations) is labelled as yours and left for the user to check by hand.

## Blind audit (optional, on request)

When the user has reached a conclusion and wants it checked, start a separate subagent that receives the paper, the
code and the data but not the user's conclusion, and asks it to recompute the result and find errors. Report where it
agrees and disagrees.
