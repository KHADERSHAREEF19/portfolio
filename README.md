# Khader Shareef Madani — Portfolio

Static portfolio site for **Khader Shareef Madani**, Cybersecurity Analyst (SOC / AI Threat Validation / IAM). Open to UAE relocation, immediate joiner.

Live: <https://khadershareef19.vercel.app>

Built with plain HTML, CSS, and vanilla JavaScript. No build step, no framework.

## Run locally

```bash
# from the repo root
python3 -m http.server 8000
# open http://localhost:8000
```

Any static server works (e.g. `npx serve .`, VS Code Live Server).

## Structure

```
index.html                  # single-page site (all sections)
favicon.svg                 # site icon
vercel.json                 # static-hosting config (clean URLs, cache, headers)
.vercelignore               # keeps tooling out of deployments
assets/
  css/style.css             # all styles (no inline <style> or style="" anywhere)
  js/script.js              # navbar, preloader, timeline reveal, CTF
  js/vendor/confetti.browser.js  # vendored canvas-confetti v1.6.0 (no CDN)
  img/                      # certificates + project banners
  KhaderShareef.pdf         # UAE resume, 1-page ATS
tools/build_resume.py       # regenerates the ATS resume PDF
tests/test_site.py          # stdlib smoke tests (58 checks)
```

All styling lives in `assets/css/style.css` and all behaviour in
`assets/js/script.js` — there are no inline `style` attributes, inline
`<style>` blocks or inline event handlers in `index.html`.

## CTF resume puzzle

The resume is behind a client-side puzzle (`#ctf`): Base64-decode Clue 1 and
ROT13-decode Clue 2, combine the parts to get the flag, and submit it to reveal
the download link.

> Note: this is a static site, so the check runs in the browser (SHA-256 hash
> comparison in `assets/js/script.js`). The PDF is still publicly downloadable
> at `assets/KhaderShareef.pdf` by design. For true gating, verify server-side.

## Contact

There is no form backend. The Contact section offers direct actions instead:
email, WhatsApp and a resume download. Nothing on the page depends on a
local or external server.

## Resume PDF

`assets/KhaderShareef.pdf` is generated, not hand-edited:

```bash
python3 tools/build_resume.py   # needs reportlab (pip install reportlab)
```

It produces a single-page ATS-friendly PDF (real text, standard headings,
author metadata set, ATS keywords). Edit `tools/build_resume.py`, not the PDF.

## Tests

Stdlib-only smoke tests (no dependencies):

```bash
python3 tests/test_site.py
```

They check HTML tag balance, that referenced local assets exist, that image
`alt` text is meaningful, and that the CTF hash matches the puzzle clues.

## Deploy

Static hosting — no build command, publish directory is `.`.

- **Vercel**: `vercel.json` sets clean URLs and long-lived caching for
  `/assets/*`, plus `nosniff`, `Referrer-Policy` and `X-Frame-Options`.
  `.vercelignore` keeps `tests/`, `tools/` and `.github/` out of the deploy.
- **GitHub Pages**: serves the whole branch, so `tests/` and `tools/` would be
  publicly fetchable. They contain no secrets; move them into `public/` if you
  want a strictly clean artifact.

Every reference is relative (`./assets/...`), so both hosts work without a
base-path change. The 37 local asset references are covered by the test suite.

## License

MIT — see [LICENSE](LICENSE).
