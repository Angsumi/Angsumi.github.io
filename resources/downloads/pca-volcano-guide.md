# Read a PCA or volcano plot carefully

## PCA: questions to ask
1. What data transformation and feature filtering were used?
2. Are points biological samples or repeated measurements of the same sample?
3. What fraction of variation does each displayed component explain?
4. Do batches or known technical covariates align with apparent groups?
5. Are outliers explainable by QC, metadata or biology?

PCA summarizes variation; a visual cluster is not a significance test or causal result.
For RNA-seq exploratory PCA, use an appropriate transformation and document gene selection.
Do not compare PCA axes from separately fitted analyses as if they were the same coordinate system.

## Volcano: questions to ask
1. What contrast defines the sign of log2 fold change?
2. Does the vertical axis show raw p-values or adjusted p-values?
3. What hypothesis family and adjustment method were used?
4. Were low-information features filtered, and how are missing values handled?
5. Are fold changes shrunken or otherwise estimated differently from testing values?
6. Do labels emphasize only selected findings while hiding the tested universe?

A large effect is not automatically reliable; a small p-value is not a measure of biological importance.
Inspect counts, uncertainty, sample design and plausibility before interpreting a selected gene.

## Caption template
Data and transformation: ___
Feature universe / filtering: ___
Contrast and direction: ___
Model and adjustment: ___
Exploratory limitations: ___

Primary reference: [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

Ask for interpretation support: https://angsumi.online/inquiry/?category=research&campaign=research-checklist


ANGSUMI · Version 2026-11-08 · Adapt this checklist to your project.
