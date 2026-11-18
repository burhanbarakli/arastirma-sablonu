---
name: zayif-nokta-raporu
description: Weak-point report for a research paper, before reproducing it ("step 0"). Use when the user gives one or more papers (PDF path, arXiv/OpenReview/DOI link or title) and wants to know where the method may break, what it assumes, which constants were hand-picked, which conditions were never tested, whether results sit at the ceiling, what reviewers and GitHub issues say, or wants an assumption table across several papers of a new field. Triggers include "zayıf nokta raporu", "makaleyi zorla", "nerede bozulur", "varsayım tablosu", "0. adım", "weak points of this paper", "where does this method break". Not for summarising a paper or writing a review of the user's own manuscript.
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

## Blind audit (optional, on request)

When the user has reached a conclusion and wants it checked, start a separate subagent that receives the paper, the
code and the data but not the user's conclusion, and asks it to recompute the result and find errors. Report where it
agrees and disagrees.
