# Research acquisition implementation — 8 November 2026

Status: local implementation and bounded OpenSEO audit complete; not committed, pushed, merged or deployed.

## Source and deployment

- Edited only `/home/angsuman/extra_spac/Angsumi/public-release`, branch `codex/angsumi-launch-polish`, initial HEAD `0e10a49`.
- Sibling `website`, branch `codex/angsumi-lead-machine`, initial HEAD `56eded4`, is a linked older worktree and remains clean and unchanged.
- Both worktrees were clean at the start. Remote: `https://github.com/Angsumi/Angsumi.github.io.git`.
- GitHub Pages workflow packages an allowlisted artifact on pushes to main. The workflow now regenerates research pages before checks. No deployment was performed.
- Live HTTP and www homepage variants reach `https://angsumi.online/`; the live homepage and sampled research services declare self-referencing canonicals. Full reads: `live-baseline.json`.

## Implemented

- Research-only homepage, shared navigation/footer, services index, about, research portfolio, inquiry, resource index and updated policy presentation.
- Six existing research service URLs retained; distinct input requirements, prerequisites, limitations, scope factors, Service schema and breadcrumbs added.
- Five referenced planning guides: RNA-seq quote preparation, FASTQ versus counts, microbiome planning, reproducible handover, manuscript figures/methods.
- Public intake now offers research and research training. Service context is allowlisted and prefilled into the existing project_type field. Contact consent, optional marketing, honeypot, idempotency, success/error states and API contract remain intact. Backend still supports historical digital leads.
- Research-only portfolio and an explicitly illustrative deliverable structure. No new client endorsements or outcome claims.
- 311 local HTML URLs retired (290 location pages, 13 unrelated service pages, business, tools and unrelated learning pages); 360 retired files including downloads, learning assets and unused homepage handler. `retired_urls.json` prevents resurrection. `research-migration.csv` records URL decisions.
- Real GitHub Pages 404 behavior is expected only for removed files controlled by this release after deployment. No blanket redirect, meta refresh or claim of an HTTP 301. Independent project sites and already missing old sitemap entries are documented separately.
- Sitemap now contains 24 canonical URLs, including existing independently hosted research destinations and CV. Robots no longer blocks retired location pages from being crawled.
- All six legacy generator names delegate to the research build. Research service source data replaces old agency data; old location data is empty.

## Verification

- 24 Python unit tests pass.
- Node analytics and Supabase suites pass.
- `scripts/check_growth.py`: 22 pages checked for metadata, JSON-LD, IDs, form labels, destinations, retirement, sitemap and inquiry contracts.
- All seven generator entry points produce identical output; retired offers stay absent.
- Clean rebuild in an isolated temporary copy: remove generated pages, regenerate, and pass static contracts.
- Public artifact `/tmp/angsumi-research-final-20261108` generated; private backend, tests, scripts, documentation and database material excluded.
- Python syntax, JavaScript syntax and `git diff --check` pass.
- Before the owner requested no browser use, a synthetic localhost inquiry completed with reference `ANG-2EA897E65358AEAA`. Local database confirmed research category, RNA-seq context, contact_consent true and marketing_consent false. No production lead or outbound message was sent.
- Mobile browser check was interrupted and remains unverified. No further browser use after the owner's instruction.

## OpenSEO

Created the owner-approved free project for `angsumi.online`, separate from the blog, with India/English default and a separately labeled US/English sample. Revised positioning and key pages saved. Plain 50-page live crawl completed; no Lighthouse. Source evidence and opportunity decisions are in `seo-evidence.json` and `opportunities.md`.

Report: https://app.openseo.so/p/a62af541-4084-41c6-9b63-ffcd4585f6e0/reports/b1e3c956-1f7d-4347-a067-ec0d61215a9d

Search Console connection: https://app.openseo.so/p/a62af541-4084-41c6-9b63-ffcd4585f6e0/search-performance

The audit found nine existing sitemap 404s. Keyword and backlink figures are provider estimates, not measured visits or a complete per-URL inventory. No existing research winner is established. No traffic, conversion or ranking improvement is promised.

## Outstanding

1. Review and authorize publication; production status still reflects the previous mixed offering. After publication, verify retired HTTP responses, canonical sitemap and research inquiry storage/notification delivery without browser use unless the owner changes that preference.
2. Connect Search Console and obtain per-URL traffic/link evidence. Migration decisions are not based on measured URL-level traffic and may need refinement before publishing.
3. Two or three validated, licensed public-data or permissioned scientific case studies are not yet produced. Existing repository descriptions are explicitly limited and the handover example is illustrative. Confirm contribution, licensing and rerun status before stronger claims.
4. Owner confirms broad bioinformatics availability. Specific assays, tools, frameworks, capacity, data transfer, retention, code rights and support remain project-scoping decisions. No production pipeline capability or security certification is inferred.
5. Mobile visual/accessibility/performance verification remains incomplete. Automated structural and privacy checks do not replace it.
6. Record actual launch date after deployment. Inspect indexing and qualified inquiries at approximately 30, 60 and 90 days; no automation or unsolicited outreach was created.
