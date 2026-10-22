# Notes — How large is the market for a public-data service, in Italy and in Europe

## 22 October 2026 — SJ-0: Constitution loaded
- Loaded spec/constitution.md and spec/specjournalism.md.
- Language: Italian and English, explicit user instruction recorded in story-brief.md (Article 11).

## 22 October 2026 — SJ-1: Story Brief
- Produced story-brief.md v1.0 (angle 1 of 4 chosen by the user: market-size analysis).
- Audience: policy-aware reader. Hook: structural relevance (no specific event).

## 22 October 2026 — SJ-2: Clarifications
- Q1 Geographic scope: Italy, Germany, France, Spain, EU27 (proposed by Claude, approved).
- Q2 Time period: latest year available per source, years stated (approved).
- Q3 Comparison baseline: source comparison for Italy (main), country weight on EU27 (context).
- Q4 Unit of analysis: absolute counts, shares as context.
- Q5 Audience calibration: explain active enterprise, size class, why sources differ.
- C2, C3: formulated by Claude on the user's delegation ("fai tu").

## 22 October 2026 — SJ-3: Null hypothesis
- Falsifiability, floor and scope trigger recorded in story-brief.md v1.1.
- Formulated by Claude on the user's delegation; flagged in the brief as a proposal.
- Disclosure: before this report, Claude had already queried Eurostat once for the TAM figure of
  the concept note (SBS_SC_1B_SE_R2 and SBS_NA_1A_SE_R2, 22 October 2026). Those figures are not
  used in the report; all numbers below come from the extractions listed in this file.

## 22 October 2026 — SJ-4: Data Design
- Produced data-design.md v1.0; approved by the user on 22 October 2026 ("vai").
- Datasets planned: A (ISTAT ASIA, four-digit, with size class), B (Eurostat SBS sectors), C (Eurostat SBS size class).

## 22 October 2026 — Phase 1: Dataset search
- Command: opensdmx --output json providers → 16 providers; used: eurostat (alias estat accepted), istat.
- Candidate search (read-only, SDMX search tool): istat "enterprises" → 183_277 family; eurostat "enterprises size class", "business demography", "SBS", "SBS_SC", "SBS_NA", "NACE Rev. 2.1".
- Selected: 183_277_DF_DICA_ASIAUE1P_3 (ISTAT), SBS_NA_1A_SE_R2 (Eurostat), SBS_SC_1B_SE_R2 (Eurostat).
- Not found: Eurostat enterprise counts for these sectors after reference year 2020 (NACE Rev. 2 ends in 2020 in these series). This is a limit of these series, not of the provider.
- Constraints for the ISTAT dataflow list only NACE sections (A–S) because the constraint is shared at the DSD level; the actual four-digit codes were checked in the codelist (metadata/A_istat_asia-meta-ECON_ACTIVITY_NACE_2007.csv): 5813, 5814, 6391, 7022, 7320.

## 22 October 2026 — Phase 2: Dimensions and metadata
- Eurostat B: dimensions freq, nace_r2, indic_sb, geo. nace_r2 = J5813, J5814, J6391, M7022, M7320; indic_sb = V11110 (Enterprises - number); geo = EU27_2020, IT, DE, FR, ES.
- Eurostat C: dimensions freq, nace_r2, indic_sb, size_emp, geo. nace_r2 = J581, J639, M702, M732; size_emp = 0_1, 2-9, 10-19, 20-49, 50-249, GE250, TOTAL.
- ISTAT A: dimensions FREQ, REF_AREA, DATA_TYPE, ECON_ACTIVITY_NACE_2007, PERS_EMPL_SIZE_CLASS, LEGAL_FORM, Y_ENTER_WITH_EMPLOYEES, Y_CRAFTMEN. DATA_TYPE = AENTN (number of enterprises). Y_ENTER_WITH_EMPLOYEES: 0, 1, 9 (9 = total; 170 + 231 = 401 for code 5813 confirms 0 = without employees, 1 = with employees).
- Metadata saved: metadata/B_eurostat_sbs_sectors-meta-{nace_r2,geo,indic_sb}.csv, metadata/C_eurostat_sbs_sizeclass-meta-{size_emp,nace_r2}.csv, metadata/A_istat_asia-meta-ECON_ACTIVITY_NACE_2007.csv.

## 22 October 2026 — Phase 2: Download
- B: opensdmx get SBS_NA_1A_SE_R2 --provider eurostat --freq A --nace_r2 J5813+J5814+J6391+M7022+M7320 --indic_sb V11110 --geo EU27_2020+IT+DE+FR+ES --last-n 1 --yes --out output/B_eurostat_sbs_sectors.csv
  - Output: 25 rows, year 2020, 5 geographies. Edition: LAST UPDATE 01/03/24 23:00:00.
  - EU27 J5813: no value, CONF_STATUS = C (confidential). EU27 J5814 and M7320: flag u (low reliability). EU27 J6391: flag e (estimated).
- C: opensdmx get SBS_SC_1B_SE_R2 --provider eurostat --freq A --nace_r2 J581+J639+M702+M732 --indic_sb V11110 --size_emp 0_1+2-9+10-19+20-49+50-249+GE250+TOTAL --geo EU27_2020+IT+DE+FR+ES --last-n 1 --yes --out output/C_eurostat_sbs_sizeclass.csv
  - Output: 140 rows, year 2020. Flags: 7 confidential cells (C), 3 estimates (e), 2 low reliability (u).
- A: opensdmx get 183_277_DF_DICA_ASIAUE1P_3 --provider istat --FREQ A --REF_AREA IT --DATA_TYPE AENTN --ECON_ACTIVITY_NACE_2007 5813+5814+6391+7022+7320 --PERS_EMPL_SIZE_CLASS TOTAL+W0_9+W10_49+W50_249+W_GE250 --LEGAL_FORM TOT --last-n 1 --yes --out output/A_istat_asia.csv
  - Output: 15 rows, year 2024. Edition ID: not exposed in the CSV returned; to be checked before publication.
  - DISCREPANCY with data-design.md v1.0: only PERS_EMPL_SIZE_CLASS = TOTAL is returned for the four-digit codes. The size classes W0_9, W10_49, W50_249, W_GE250 exist in the DSD but not for this dataflow. The available split is Y_ENTER_WITH_EMPLOYEES (0 / 1 / 9). The user is consulted before any change (data-design.md, Handoff).

## 22 October 2026 — Double check
- Double check — SBS_NA_1A_SE_R2: Run 1 (opensdmx get): 25 rows; Run 2 (direct Eurostat API URL, curl): 25 rows, same values, flags and confidentiality status. Result: MATCH ✓
- Double check — SBS_SC_1B_SE_R2: Run 1: 140 rows; Run 2 (direct URL): 140 rows, same. Result: MATCH ✓
- Double check — 183_277_DF_DICA_ASIAUE1P_3: Run 1 (opensdmx get): 15 rows; Run 2 (direct ISTAT SDMX REST URL, curl): 15 rows, same values. Result: MATCH ✓
- Consistency with the concept note: ISTAT values reproduce TAM Italia 113,751 (401 + 1,423 + 509 + 106,054 + 5,364) and the enterprises with employees 15,698 (231 + 737 + 105 + 14,144 + 481).

## 22 October 2026 — Decision on the discrepancy (data-design v1.1)
- The user delegated the choice ("fai come ritieni più opportuno"). Option 1 chosen by Claude: for Italy the size split is enterprises with / without employees (Y_ENTER_WITH_EMPLOYEES); the European size classes (dataset C) are shown separately and never merged with the Italian split.
- data-design.md updated to v1.1. No filter other than the one already downloaded was changed; no new download.

## 22 October 2026 — Phase 3: Inspection
- A (output/A_istat_asia.csv): 15 rows = 5 codes x 3 values of Y_ENTER_WITH_EMPLOYEES; year 2024; no flags. Totals: 401, 1,423, 509, 106,054, 5,364 (sum 113,751). With employees: 231, 737, 105, 14,144, 481 (sum 15,698).
- B (output/B_eurostat_sbs_sectors.csv): 25 rows; year 2020. EU27: J5813 no value (confidential); J5814 20,000 (u); J6391 6,820 (e); M7022 844,034; M7320 30,000 (u). Italy: 282, 1,507, 481, 64,999, 3,685 (sum 70,954).
- C (output/C_eurostat_sbs_sizeclass.csv): 140 rows; year 2020. Confidential cells: J639 EU27 class 10-19; J639 Italy classes 20-49 and GE250; others as listed in the file. M732 EU27 total (30,000, u) equals B M7320 EU27 total (30,000, u).
- Transformations planned (to be applied on the page, never in output/): share of a country on the EU27 total = country value / EU27 value x 100, only where the EU27 value exists; shares by size class = class value / TOTAL value of the same row group, only where both exist; sums over codes exclude codes without a value and say so.

## 22 October 2026 — SJ-5 Cross-check

### Block A — Brief → Data coverage
- A1 Research question coverage: PASS — datasets A, B, C count enterprises in the five sector codes, directly the phenomenon of the brief.
- A2 Null hypothesis testability: PASS — floor (1): non-confidential EU27 values for 4 of 5 codes (J5813 is confidential) and Italy values for 5 of 5; floor (2): Italy comparable between A and B on 5 of 5 codes; floor (3): size-class counts in C.
- A3 Scope consistency: PASS — Italy, Germany, France, Spain and EU27 in B and C; Italy in A; latest year per source (2024 for A, 2020 for B and C), stated.

### Block B — Data Design → Downloaded Data
- B1 Dataflow match: PASS — A, B, C each have an output file.
- B2 Filter match: PASS — filters as in data-design.md v1.1 (the only change, with / without employees for Italy, is recorded in v1.1).
- B3 Visualisation feasibility: PASS — 5 sectors by 5 geographies (bars), 5 sectors for Italy in two sources (grouped bars), 7 size classes for 4 groups (stacked bars). Cells without value are omitted, not set to zero.
- B3b Visual honesty (Y-axis + no img): PASS — absolute-value charts set min 0 explicitly; share charts bounded 0–100 and labelled; all charts are Chart.js canvas.

### Block C — Data → Narrative plan
- C1 Finding cards feasibility: PASS — four cards, each traceable: (1) EU27 management consultancy 844,034 enterprises, about 94% of the sum of the four codes with a value; (2) Italy, A against B: 113,751 vs 70,954; (3) Italy enterprises with employees 15,698 of 113,751; (4) country weights: France highest in three of four codes with a value, Italy highest in market research (12.3%).
- C2 Executive summary pre-check: PASS — cross-entity (countries, sources) and surprise (the two sources differ) are present; no temporal pattern, since there is no time series.
- C3 Null hypothesis (preliminary): LIKELY REJECT — the null is that the data do not allow the counts; they do, with the stated limits.

### Overall result
ALL PASS → proceed to Phase 4.

## 22 October 2026 — Phase 0: Research question
- Original (verbatim from story-brief.md, journalistic angle): "Analisi di mercato (the user's wording). The analysis measures how many organisations operate in the sectors that could use a natural-language service for public data, in Italy and in Europe, by sector and by size class. It also states what the official figures do not allow to say."
- Cleaned: "How many enterprises operate in the sectors that could use a natural-language public-data service, in Italy and in Europe, by sector and by size class, and what do the official figures not allow to say?" (Italian version in index.html).
- Statistical proxy: number of enterprises in five sector codes. It is an imperfect proxy of the market: it counts organisations, not turnover or demand, and the sources count different populations.

## 22 October 2026 — Phase 4: Charts
- Seven Chart.js charts, all canvas, tooltips on, uppercase labels, bilingual (language toggle re-renders the charts).
- ue and ue-small (dataset B): horizontal bars; the second chart repeats the data on a scale where the small sectors can be read. min 0.
- paesi (B): grouped horizontal bars of shares of the EU27 total; min 0.
- fonti-main and fonti-small (A, B): grouped horizontal bars, ISTAT against Eurostat, series side by side and never summed; min 0.
- dipendenti (A): stacked horizontal bars of shares, axis 0–100; classi (C): stacked horizontal bars of shares, axis 0–100. Cells without a value are left empty.
- Colours: palette of the current repository stylesheet, as in report 15 (blue, purple, cyan, orange), not the original six-colour list of the constitution; the repository palette is the one used by the existing reports.
- Rendering check in the browser: seven charts present, data counts as expected, no console error except the missing favicon (also present in the other reports).

## 22 October 2026 — Phase 5–6: Page and accountability
- index.html (bilingual, lang it, toggle ENG|ITA), reports.json (entry 16) and README updated. queries/transform.py reproduces every derived figure from output/*.csv.
- Reproducibility test: opensdmx run queries/A_istat_asia.yaml, queries/B_eurostat_sbs_sectors.yaml and queries/C_eurostat_sbs_sizeclass.yaml re-run on 22 October 2026 into a scratch folder: A 16 lines, B 26 lines, C 141 lines (header included), identical to output/*.csv. Result: MATCH ✓
- Known deviations from the specification: (1) the null hypothesis and clarifications C2 and C3 were formulated by the assistant on the user's delegation (flagged in the brief and on the page); (2) the colour palette (see Phase 4); (3) ISTAT edition ID not exposed in the CSV, not recorded; (4) licences of ISTAT and Eurostat data not verified on the dataset pages, stated on the page; (5) the legal-form dimension was fixed to the total and not shown.
- Not done: pre-publication checklist signed by the user, push to the public repository.

## 22 October 2026 — Phase 7: Patterns for executive summary
- Temporal: not available (no time series; one year per source).
- Cross-entity: EU27 2020: management consultancy 844,034 of 900,854 enterprises with a value (93.7%); France 19.8% against Italy 7.7% of EU27 consultancy (sections ue, paesi).
- Surprise: ISTAT 2024 counts 106,054 management consultancy enterprises in Italy and Eurostat 2020 counts 64,999 (61.3%); in journals and periodicals Eurostat 1,507 is above ISTAT 1,423 (sections fonti).
- Null hypothesis result: REJECTED — non-confidential counts for 4 of 5 codes for the EU27 and 5 of 5 for Italy; the two sources are comparable for Italy on 5 of 5 codes; size-class counts exist in Eurostat. Limits stated on the page.

## 22 October 2026 — Wording revision (page, catalogue, brief)
- At the user's request the page text was rewritten to avoid negative phrasing ("non", "né", "mai") where the same content can be stated positively, in Italian and English. Reserves on the facts stay: confidential cell, low-reliability and estimate flags, different reference years.
- Changes: title, research question and introduction, statistical proxy, scope-limit text, licence note, executive summary (paragraphs 1, 3, 4), notes of the five sections (heading "Reading limits" → "How to read the data"), transformation notes, methodology notes, one finding card, entry 16 of reports.json.
- Research question: kept in substance (the limits of the data are still part of the question: "quali limiti di anno e di copertura hanno i dati ufficiali"); story-brief.md updated to v1.2 with a version note, data-design.md header updated to link to v1.2. No data, filter or number was changed.
- Claim removed during the revision: "the two sources count different populations" (an inference not verified). The page now says that the reference years differ and that the methodological notes of the two sources are the next step to explain the ratio.
