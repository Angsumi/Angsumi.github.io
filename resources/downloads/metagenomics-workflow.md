# Choose a microbiome workflow

First identify the assay. Do not treat marker-gene profiles as whole-community functional measurements.

| Question | Starting point | Main limitation to discuss |
|---|---|---|
| Marker-gene community composition | Amplicon denoising, taxonomy and diversity | Primer bias, reference coverage and compositionality |
| Shotgun community profiling | Quality control, host-read strategy and taxonomic profiling | Reference bias and depth |
| Genomic reconstruction | Assembly, binning and quality assessment | Coverage, contamination, strain mixtures |
| Functional potential | Appropriate gene/pathway annotation | Potential is not measured activity |

## Before choosing a tool
- Record marker/primers, platform, paired layout and sample handling.
- Include negative controls and other assay-appropriate controls in the analysis plan.
- Check metadata consistency, batches, repeated measures and relevant covariates.
- Define whether the question is descriptive, comparative or exploratory.
- Match the classifier/reference to the marker and expected taxa.
- Record filtering and normalization decisions; justify diversity/comparison methods.
- Avoid causal or absolute-abundance interpretations from relative profiles alone.
- Keep provenance, tool versions and all exclusion decisions.

## A short scoping template
Assay: ___
Samples / controls: ___
Question: ___
Available metadata: ___
Desired outputs: ___
Known limitations: ___

Primary reference, checked 8 November 2026:
[QIIME 2 amplicon documentation](https://amplicon-docs.qiime2.org/en/stable/)

Discuss scope: https://angsumi.online/inquiry/?category=research&campaign=research-checklist


ANGSUMI · Version 2026-11-08 · Adapt this checklist to your project.
