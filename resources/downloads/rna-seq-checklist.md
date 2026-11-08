# RNA-seq analysis planning checklist

Use before analysis, not as a promise that any dataset supports differential expression.

## Study question and design
- [ ] State the biological comparison and unit of replication.
- [ ] Separate biological from technical replicates.
- [ ] Record conditions, batch, subject pairing, sex or other relevant covariates.
- [ ] Check confounding: a condition perfectly aligned with batch cannot be separated by a model alone.
- [ ] Agree contrasts and multiple-testing control before interpreting selected genes.

## Inputs and quality
- [ ] Record organism, assay type, strandedness, read layout and library preparation.
- [ ] Keep sample identifiers consistent across reads, quantification and metadata.
- [ ] Review read quality, adapters, contamination and alignment/quantification diagnostics.
- [ ] Pin reference genome/transcriptome and annotation versions.
- [ ] Document exclusions with reasons; never remove a sample just to obtain significance.

## Analysis
- [ ] Use a suitable count-based workflow for DESeq2. Do not substitute TPM as raw counts.
- [ ] If importing transcript estimates, follow a supported import workflow and its assumptions.
- [ ] Review transformed-data exploratory plots separately from count-model inference.
- [ ] Report effect sizes, uncertainty and adjusted p-values, plus the tested design.
- [ ] Document gene identifiers, enrichment background and mapping losses.

## Handover
- [ ] Deliver scripts, environment versions, input checksums and execution instructions.
- [ ] Include complete tested results, not only selected significant rows.
- [ ] Record limitations and planned biological follow-up.

Primary reference, checked 8 November 2026:
[DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

Need a study-specific review? https://angsumi.online/inquiry/?category=research&campaign=research-checklist


ANGSUMI · Version 2026-11-08 · Adapt this checklist to your project.
