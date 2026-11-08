# Reproducibility checklist

## Inputs
- [ ] Keep raw inputs immutable with a manifest and checksums.
- [ ] Record provenance, permission, license and restricted-data handling.
- [ ] Provide a data dictionary and sample metadata schema.

## Environment
- [ ] Record language, package and executable versions.
- [ ] Save an environment definition or suitable lockfile.
- [ ] Pin external references/databases and their release dates.
- [ ] Record resource requirements and stochastic seeds when relevant.
- [ ] Keep secrets outside source control; provide variable names only.

## Workflow
- [ ] Define a single documented entry point.
- [ ] Validate inputs and fail clearly when assumptions are violated.
- [ ] Record commands, parameters and versioned code commits.
- [ ] Use a non-sensitive miniature dataset for a reproducibility check.
- [ ] Check that a second person can follow the instructions.

## Outputs
- [ ] Record output schemas and expected checks.
- [ ] Keep full results and traceable figure-generation code.
- [ ] Document limitations, exclusions and interpretation boundaries.
- [ ] Separate an exploratory result from independently validated evidence.

Example input manifest:
```csv
sample_id,input_path,sha256,assay,reference_version
EXAMPLE_01,example.fastq.gz,REPLACE_WITH_HASH,RNA-seq,REPLACE_WITH_VERSION
```

Primary operational references:
[Python virtual environments](https://docs.python.org/3/tutorial/venv.html)
[SAMtools manual](https://www.htslib.org/doc/samtools.html)

Ask for workflow support: https://angsumi.online/inquiry/?category=research&campaign=research-checklist


ANGSUMI · Version 2026-11-08 · Adapt this checklist to your project.
