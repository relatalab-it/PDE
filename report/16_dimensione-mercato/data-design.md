# Data Design — How large is the market for a public-data service, in Italy and in Europe
Linked to: story-brief.md v1.2 dated 22 October 2026 (design v1.1)

## Methodological approach
Count the active enterprises in five sector codes (publishing of newspapers, publishing of
periodicals, news agencies, management consultancy, market research) for Italy, Germany,
France, Spain and the EU27, using the latest year of each source. Compare, for Italy, the
national statistical office figure with the European one on the same codes, and break the
counts down by size class where the sources allow it. No forecast and no causal claim.
The method is a descriptive comparison of counts, tested against the methodological floor
in the brief (three of five codes, non-confidential, comparable between sources for Italy).

## Datasets

### Dataset A — Italy, enterprises by sector and size class (national source)
- Source: ISTAT
- Dataset ID: 183_277_DF_DICA_ASIAUE1P_3 (Enterprises and persons employed, NACE 2007 four digit)
- Dimensions / filters: REF_AREA = Italy (national); ECON_ACTIVITY_NACE_2007 = 58.13, 58.14, 63.91, 70.22, 73.20; PERS_EMPL_SIZE_CLASS = TOTAL (the size classes are not available for the four-digit codes in this dataflow); LEGAL_FORM = TOT; DATA_TYPE = AENTN (number of enterprises); Y_ENTER_WITH_EMPLOYEES = 0 (without employees), 1 (with employees), 9 (total)
- Time range: latest year available (2024, confirmed on download)
- Geographic scope: Italy, national level
- Unit: number of active enterprises
- Output file: output/A_istat_asia.csv
- Query file: queries/A_istat_asia.yaml
- Covers: Italian count by sector, split between enterprises with and without employees; main side of the source comparison

### Dataset B — Enterprises by sector, countries and EU27 (European source)
- Source: Eurostat
- Dataset ID: SBS_NA_1A_SE_R2 (Detailed annual enterprise statistics for services, NACE Rev. 2)
- Dimensions / filters: freq = A; nace_r2 = J5813, J5814, J6391, M7022, M7320; indic_sb = V11110 (number of enterprises); geo = EU27_2020, IT, DE, FR, ES
- Time range: latest year available (2020 in the series seen so far; to be confirmed)
- Geographic scope: EU27 total and four countries
- Unit: number of enterprises
- Output file: output/B_eurostat_sbs_sectors.csv
- Query file: queries/B_eurostat_sbs_sectors.yaml
- Covers: European total, weight of the four countries, second side of the source comparison for Italy

### Dataset C — Enterprises by size class, EU27 and countries (European source)
- Source: Eurostat
- Dataset ID: SBS_SC_1B_SE_R2 (Services by employment size class, NACE Rev. 2, three digit)
- Dimensions / filters: freq = A; nace_r2 = J581, J639, M702, M732; indic_sb = V11110; size_emp = all classes; geo = EU27_2020, IT, DE, FR, ES
- Time range: latest year available (2020)
- Geographic scope: EU27 total and four countries
- Unit: number of enterprises
- Output file: output/C_eurostat_sbs_sizeclass.csv
- Query file: queries/C_eurostat_sbs_sizeclass.yaml
- Covers: size-class breakdown for the European side. Three-digit groups are broader than the four-digit codes of dataset B (J581 contains 58.13 and 58.14 and other publishing; J639 contains 63.91 and 63.99; M702 contains 70.21 and 70.22); only M732 coincides with 73.20. The report states this wherever dataset C is shown.

## Visualisation plan

| Section ID | Dataset | Chart type | Library | Note |
|---|---|---|---|---|
| eu-sectors | B | Horizontal bar | Chart.js | EU27 enterprises by sector, latest year. Management consultancy dominates; the four smaller sectors are shown in a second chart, same unit, Y-axis from zero |
| it-sources | A, B | Grouped bar | Chart.js | Italy: national source against European source, same codes, years labelled in the legend |
| country-weight | B | Horizontal bar | Chart.js | Share of Italy, Germany, France, Spain in the EU27 total, by sector |
| employees-it | A | Stacked horizontal bar (shares of the total) | Chart.js | Italy: enterprises with and without employees, by sector (not comparable with C: no merge) |
| size-class-eu | C | Stacked horizontal bar (shares of the total) | Chart.js | EU27: distribution by size class, by sector; three-digit groups, class 0–1 persons includes the self-employed |

All charts use Chart.js. Absolute-value charts start at zero (Article 7). Share charts state
that the axis is bounded 0–100%. No dual axes. No D3.

## Data quality risks
- Dataset A: the national figure counts the active enterprises of the national register; the
  universe and the reference year differ from dataset B. Revision risk: the register is updated
  yearly; the edition ID is recorded in notes.md.
- Dataset B: confidential cell for EU27 in 58.13 (observed in a preliminary look); flags u (low
  reliability) and e (estimate) on some EU27 values; reference year 2020, older than dataset A;
  NACE Rev. 2 ends in 2020 in this series, a limit of the series and not of the provider.
- Dataset C: three-digit groups broader than the four-digit codes (see above); same year limit as B.
- Cross-source: the same Italian sectors give different totals in A and B (preliminary look: the
  European source is lower). The report must present this as a difference between sources and
  must not sum or merge the two.

## Methodological commitments
- Method: descriptive comparison of counts, no model.
- Threshold: the methodological floor in story-brief.md v1.1 (three of five codes with
  non-confidential counts for Italy and EU27; Italy comparable between sources on three codes;
  size-class counts in at least one source).
- Baseline: EU27 total for country weights; the national source for the Italy comparison.
- If the floor fails: scope down to the codes with data and state what is missing; do not
  change the method silently (Article 3).
- Years are never harmonised by assumption: each figure carries its year.

## Version history
- 22 October 2026 v1.0 — initial design
- 22 October 2026 v1.1 — after the download: for Italy the size split is with / without employees (the size classes are not available for four-digit codes in the national dataflow); the user delegated the choice ("fai come ritieni più opportuno"). Recorded in notes.md.
