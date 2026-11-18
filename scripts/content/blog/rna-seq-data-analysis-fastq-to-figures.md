---
title: RNA-seq data analysis: from FASTQ to figures
description: A step-by-step guide to bulk RNA-seq analysis: quality control, alignment or quantification, count matrices, DESeq2 differential expression, enrichment and publication figures.
date: 2026-11-18
cluster: RNA-seq
service: rna-seq-analysis
guide: fastq-versus-count-matrix
faq:
  - q: Can I start the analysis from a count matrix instead of FASTQ files?
    a: Yes, if the counts are raw (unnormalized) and you can document how they were produced, including the reference genome and annotation versions. You lose the ability to repeat read-level quality control, so keep the original FASTQ files available.
  - q: How many biological replicates do I need?
    a: It depends on the effect sizes you care about and on biological variability. One systematic yeast study recommended at least six biological replicates per condition. Decide this before sequencing, because replication cannot be added during analysis.
  - q: Should I use DESeq2, edgeR or limma-voom?
    a: All three are established, documented methods for count-based differential expression. The choice matters less than a correct design formula, appropriate filtering and honest reporting. Use the method whose assumptions and documentation you can follow and cite.
  - q: Are TPM or FPKM values suitable input for DESeq2?
    a: No. DESeq2 expects raw counts or estimated counts imported with an appropriate route such as tximport. Normalized values like TPM or FPKM are not direct substitutes.
---

Bulk RNA-seq analysis turns raw sequencing reads (FASTQ files) into a table of genes that change between conditions. The core steps are quality control, alignment or quantification against a reference, building a count matrix, statistical testing for differential expression (for example with DESeq2), functional enrichment, and figures that report effect sizes and uncertainty.

This guide follows that path from beginning to end for a typical bulk RNA-seq experiment. Single-cell RNA-seq, de novo transcriptome assembly and long-read data each need a different workflow. For a broader review of design and analysis choices, see Conesa and colleagues' [survey of best practices for RNA-seq data analysis](https://doi.org/10.1186/s13059-016-0881-8).

## The workflow at a glance

| Step | Input | Output | Common tools |
|---|---|---|---|
| Quality control | FASTQ | QC reports | [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/), [MultiQC](https://doi.org/10.1093/bioinformatics/btw354) |
| Trimming (when justified) | FASTQ | Cleaned FASTQ | [fastp](https://doi.org/10.1093/bioinformatics/bty560) |
| Alignment or quantification | FASTQ + reference | BAM files or transcript estimates | [STAR](https://doi.org/10.1093/bioinformatics/bts635), [HISAT2](https://doi.org/10.1038/s41587-019-0201-4), [Salmon](https://doi.org/10.1038/nmeth.4197) |
| Counting | BAM or estimates | Gene count matrix | [featureCounts](https://doi.org/10.1093/bioinformatics/btt656), [tximport](https://doi.org/10.12688/f1000research.7563.2) |
| Differential expression | Counts + sample metadata | Results table | [DESeq2](https://doi.org/10.1186/s13059-014-0550-8), [limma-voom](https://doi.org/10.1186/gb-2014-15-2-r29) |
| Interpretation | Results table | Enrichment, figures | [GSEA](https://doi.org/10.1073/pnas.0506580102) and related methods |

## 1. Start with the design, not the data

Before you open a FASTQ file, write down the comparison you want to make. List the groups, the biological replicates in each group, any pairing (for example the same patient before and after treatment), and the batches in which samples were extracted, prepared and sequenced.

This matters because the statistical model is built from this table. If every control sample was sequenced in one batch and every treated sample in another, the treatment effect and the batch effect cannot be separated, and no software can recover that comparison. On replication, [Schurch and colleagues](https://doi.org/10.1261/rna.053959.115) tested replicate numbers systematically in yeast and recommended at least six biological replicates per condition.

## 2. Check read quality

Run [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) on every FASTQ file and summarise the reports with [MultiQC](https://doi.org/10.1093/bioinformatics/btw354). Look for:

- per-base quality falling sharply towards the read ends
- adapter content
- unexpected overrepresented sequences, such as ribosomal RNA
- samples whose read counts or GC content differ clearly from the rest

FastQC flags are prompts to investigate, not automatic failures. RNA-seq libraries routinely show duplication and composition patterns that FastQC marks as warnings. Trim adapters and low-quality bases with a tool such as [fastp](https://doi.org/10.1093/bioinformatics/bty560) when the reports justify it, and record the settings you used.

## 3. Align or quantify against a reference

There are two standard routes:

- **Alignment-based.** A splice-aware aligner such as [STAR](https://doi.org/10.1093/bioinformatics/bts635) or [HISAT2](https://doi.org/10.1038/s41587-019-0201-4) maps reads to the genome and writes BAM files. You then count reads per gene with [featureCounts](https://doi.org/10.1093/bioinformatics/btt656). BAM files also support visual inspection and other downstream uses.
- **Quantification-based.** [Salmon](https://doi.org/10.1038/nmeth.4197) estimates transcript abundance directly from reads without writing full alignments. Its transcript-level estimates are summarised to genes with [tximport](https://doi.org/10.12688/f1000research.7563.2).

Either way, record the exact genome assembly and annotation release (for example the Ensembl or GENCODE version). Results are only reproducible against the same reference.

## 4. Build and inspect the count matrix

The count matrix has one row per gene and one column per sample. Pair it with a sample sheet whose identifiers match the column names exactly.

Before testing anything, look at the samples as a whole. The [DESeq2 vignette](https://www.bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) shows how to apply a variance-stabilising transformation and draw a PCA plot and a sample-distance heatmap. These plots reveal sample swaps, outliers and batch structure. A sample that clusters with the wrong group deserves an explanation before analysis continues.

## 5. Test for differential expression

[DESeq2](https://doi.org/10.1186/s13059-014-0550-8) models raw counts with a negative binomial distribution and estimates size factors to account for differences in sequencing depth. You supply a design formula, such as `~ batch + condition`, that names the variables to adjust for and the one you want to test.

Points that often go wrong:

- **Input type.** DESeq2 expects raw or estimated counts, not TPM, FPKM or other normalised values.
- **Multiple testing.** Thousands of genes are tested at once. Report adjusted p-values, which DESeq2 calculates with the [Benjamini–Hochberg](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) procedure, rather than raw p-values.
- **Effect size.** Fold changes estimated from low counts are noisy. Shrinkage estimators such as [apeglm](https://doi.org/10.1093/bioinformatics/bty895) give more stable values for ranking and plotting.

[edgeR](https://bioconductor.org/packages/edgeR/) and [limma-voom](https://doi.org/10.1186/gb-2014-15-2-r29) are well-documented alternatives. Choose one method, state the version, and avoid running several methods only to report the most convenient result.

## 6. Interpret the results

A list of significant genes is rarely the final answer. Common next steps are:

- **Over-representation analysis**, which asks whether a pathway appears in your significant gene list more often than expected. The background ("universe") should be the genes that were actually tested, not the whole genome.
- **Gene set enrichment analysis** ([GSEA](https://doi.org/10.1073/pnas.0506580102)), which uses the full ranked list rather than a significance cut-off.

Enrichment results depend on the annotation database and its version, so record both. Enrichment describes association with a gene set. It does not show that a pathway is active or that it causes the phenotype.

## 7. Make figures that report uncertainty

Standard RNA-seq figures each answer a specific question:

- **PCA plot:** do samples group by biology, by batch, or neither?
- **Volcano plot:** how do effect size and statistical evidence relate across all genes?
- **MA plot:** do fold changes depend on expression level?
- **Heatmap:** how do selected genes behave across individual samples?

Label axes with units and transformations, say in the caption which test and threshold were used, and show sample counts. Our [scientific figure quality checklist](/resources/downloads/figure-quality.md) lists further checks.

## 8. Make it reproducible

Record software versions, parameters, reference identifiers and the commands that produced each output. Workflow frameworks such as [nf-core/rnaseq](https://nf-co.re/rnaseq) package many of these steps with version control ([Ewels et al.](https://doi.org/10.1038/s41587-020-0439-x)). Whatever you use, another analyst should be able to rerun the work from your README. Our guide to [what a reproducible bioinformatics handover should contain](/resources/reproducible-handover/) lists what to include.
