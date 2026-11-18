---
title: 16S vs 18S vs shotgun metagenomics: which should you choose?
description: How 16S rRNA, 18S rRNA and shotgun metagenomic sequencing differ in what they detect, their taxonomic and functional resolution, and when each one fits your research question.
date: 2026-11-18
cluster: Metagenomics
service: metagenomics-analysis
guide: microbiome-analysis-planning
faq:
  - q: Can 16S sequencing identify bacteria to species level?
    a: Sometimes, but not reliably. Resolution depends on the variable region sequenced, read length and the reference database. Many short-read 16S studies report confident assignments only to genus level.
  - q: Can I get functional information from 16S data?
    a: Only indirectly. Tools such as PICRUSt2 predict gene content from marker-gene sequences and reference genomes. These predictions are not measurements; shotgun metagenomics measures gene content directly.
  - q: Does shotgun sequencing detect fungi and other eukaryotes?
    a: It can detect any organism whose DNA is in the sample, but classification depends on reference genomes, which are less complete for many eukaryotes than for bacteria. Targeted 18S or ITS sequencing is often used alongside it.
  - q: Do I need negative controls?
    a: Yes, especially for low-biomass samples such as air, skin, tissue or clean water. Extraction blanks and no-template controls show which sequences come from reagents or the laboratory rather than the sample.
---

Choose 16S rRNA amplicon sequencing to profile bacteria and archaea, and 18S rRNA amplicon sequencing to profile microbial eukaryotes such as protists and algae. Choose shotgun metagenomics when you need finer taxonomic resolution, all domains of life at once, or direct evidence of gene content and metabolic potential. The research question, sample type and budget should decide.

All three methods sequence DNA extracted from a mixed community, but they look at it differently. Amplicon methods (16S and 18S) amplify one marker gene with PCR primers. Shotgun metagenomics sequences random fragments of all the DNA present. That single difference explains most of the trade-offs below.

## Side-by-side comparison

| | 16S rRNA amplicon | 18S rRNA amplicon | Shotgun metagenomics |
|---|---|---|---|
| What is sequenced | Part of the bacterial and archaeal 16S rRNA gene | Part of the eukaryotic 18S rRNA gene | Fragments of all DNA in the sample |
| Organisms targeted | Bacteria and archaea | Microbial eukaryotes (protists, algae, some fungi and animals) | All domains, including viruses with DNA genomes |
| Typical taxonomic resolution | Usually genus; species sometimes | Varies widely by lineage and region | Species and sometimes strain, where references exist |
| Function | Predicted only | Predicted only, and rarely | Measured gene content and pathways |
| Host DNA | Little effect, because PCR targets the marker | Can co-amplify host 18S in animal or plant samples | Can take up much of the sequencing in host-rich samples |
| Main reference databases | [SILVA](https://doi.org/10.1093/nar/gks1219), GTDB | [PR2](https://doi.org/10.1093/nar/gks1160), [SILVA](https://doi.org/10.1093/nar/gks1219) | Genome collections used by tools such as [Kraken 2](https://doi.org/10.1186/s13059-019-1891-0) and [MetaPhlAn 4](https://doi.org/10.1038/s41587-023-01688-w) |
| Relative cost per sample | Lower | Lower | Higher, and rises with the sequencing depth needed |

## 16S rRNA amplicon sequencing

The 16S rRNA gene is present in all bacteria and archaea. It contains conserved regions, where universal primers can bind, and variable regions (V1–V9), whose sequence differences distinguish taxa. Most studies sequence one or two variable regions, such as V4 with the [Earth Microbiome Project 515F/806R primers](https://earthmicrobiome.org/protocols-and-standards/16s/).

Reads are usually denoised into amplicon sequence variants (ASVs) with [DADA2](https://doi.org/10.1038/nmeth.3869), which resolves exact sequences rather than clustering at a similarity threshold. [Callahan and colleagues](https://doi.org/10.1038/ismej.2017.119) set out why ASVs are more reusable and comparable across studies than OTUs. [QIIME 2](https://doi.org/10.1038/s41587-019-0209-9) provides a documented, reproducible environment for the whole workflow.

**Choose 16S when** your question concerns bacterial or archaeal community composition, diversity, or differences between groups across many samples.

**Know the limits.** Primer choice affects which taxa are detected. The region sequenced limits species-level resolution. The number of 16S gene copies differs between taxa ([Kembel et al.](https://doi.org/10.1371/journal.pcbi.1002743)), so read proportions are not cell proportions.

## 18S rRNA amplicon sequencing

The 18S rRNA gene is the eukaryotic counterpart of 16S. It is widely used for protists, microalgae and other microbial eukaryotes in water, soil and sediment, often targeting the V4 or V9 region ([Earth Microbiome Project 18S protocol](https://earthmicrobiome.org/protocols-and-standards/18s/)). Taxonomy is commonly assigned against the curated [PR2 database](https://doi.org/10.1093/nar/gks1160).

**Choose 18S when** eukaryotic plankton, protists or other microbial eukaryotes are central to your question, for example in environmental metabarcoding of lakes or the ocean.

**Know the limits.** Resolution varies a great deal between lineages. For fungi, the internal transcribed spacer (ITS) region was proposed as the formal DNA barcode ([Schoch et al.](https://doi.org/10.1073/pnas.1117018109)), so ITS sequencing is often the better choice for fungal communities. In samples rich in animal or plant tissue, host 18S sequences can dominate unless blocking primers or other strategies are used.

## Shotgun metagenomics

Shotgun sequencing fragments all the DNA in a sample and sequences it without targeting a gene. [Quince and colleagues](https://doi.org/10.1038/nbt.3935) review the full process from sampling to analysis. There are two main analysis approaches:

- **Read-based profiling.** Reads are classified against reference genomes or marker genes with tools such as [Kraken 2](https://doi.org/10.1186/s13059-019-1891-0) or [MetaPhlAn 4](https://doi.org/10.1038/s41587-023-01688-w). Functional profiles come from tools such as [HUMAnN 3](https://doi.org/10.7554/eLife.65088).
- **Assembly and binning.** Reads are assembled into contigs and grouped into metagenome-assembled genomes (MAGs). This can recover organisms that are absent from reference databases, but it needs greater sequencing depth and more compute.

**Choose shotgun when** you need species- or strain-level resolution, functional genes (for example antimicrobial resistance genes or metabolic pathways), all domains together, or genomes of uncultured organisms.

**Know the limits.** In host-rich samples such as tissue, much of the sequencing can be host DNA ([Pereira-Marques et al.](https://doi.org/10.3389/fmicb.2019.01277)), which raises the depth needed per sample. Classification is only as good as the reference collection for your environment.

## Problems all three methods share

- **Contamination.** Reagents and kits contain trace microbial DNA, which can dominate low-biomass samples ([Salter et al.](https://doi.org/10.1186/s12915-014-0087-z)). Include extraction blanks and no-template controls, and report how they were used ([Eisenhofer et al.](https://doi.org/10.1016/j.tim.2018.11.003)).
- **Compositional data.** Sequencing gives relative abundances: an increase in one taxon lowers the proportion of the others. [Gloor and colleagues](https://doi.org/10.3389/fmicb.2017.02224) explain why this needs compositionally aware statistics.
- **Batch effects.** Extraction kit, run and operator can all leave signatures. Spread study groups across batches rather than processing each group separately.

## How to decide

1. Write down the question. Is it "which bacteria are present and how do communities differ?" (16S), "which microbial eukaryotes are present?" (18S or ITS), or "what can this community do, at what resolution?" (shotgun)?
2. Consider the sample type. Host-rich and low-biomass samples change both cost and feasibility.
3. Check the references. If your environment is poorly represented in genome databases, plan for assembly or treat profiling results with caution.
4. Plan controls and replication before sampling.
5. Consider combining methods. Many studies sequence 16S across all samples and shotgun on a subset.

For a checklist of what to prepare before analysis, read our [microbiome analysis planning guide](/resources/microbiome-analysis-planning/).
