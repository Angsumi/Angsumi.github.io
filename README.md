# ANGSUMI research analysis website

Static website for bioinformatics and scientific data analysis inquiries.

## Build and verify

Run from this checkout:

```sh
python3 scripts/build_growth.py
python3 -m unittest discover -s tests -v
node --test tests/analytics.test.cjs tests/supabase.test.mjs
python3 scripts/check_growth.py
python3 scripts/build_public.py /tmp/angsumi-public-artifact
```

`build_growth.py` and `research_site.py` own the research journey. Authored policy bodies live in `scripts/content/`. Legacy generator names delegate to this build and cannot regenerate retired location, business or web-development offers. `retired_urls.json` enumerates removed source files. Unrelated pages have no equivalent research destination and return GitHub Pages 404s after publication.

The release checkout is `public-release` on `codex/angsumi-launch-polish`. The sibling `website` is an older linked worktree; do not edit both. GitHub Actions packages an allowlisted static artifact and deploys pushes to `main`. Backend, tests, scripts and operational notes are excluded.

The guided inquiry uses the existing Supabase API with consent, spam controls, idempotency and explicit saved/error states. Historical research/digital/training leads remain supported by the backend; only research and research training are offered publicly. No confidential file uploads are accepted. GA4 loads only with consent and uses fixed event labels without form contents or query strings.

Supported methods and delivery capacity require feasibility review. Repository descriptions do not establish client endorsements or validated outcomes.
