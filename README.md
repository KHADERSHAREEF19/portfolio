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
assets/
  css/style.css             # all styles
  js/script.js              # navbar, preloader, timeline reveal, CTF
  js/vendor/confetti.browser.js  # vendored canvas-confetti v1.6.0 (no CDN)
  img/                      # certificates + project banners
tools/build_resume.py       # regenerates the ATS resume PDF
  KhaderShareef.pdf         # UAE resume, 1-page ATS (unlocked via CTF puzzle)
```

## CTF resume puzzle

The resume is behind a client-side puzzle (`#ctf`): Base64-decode Clue 1 and
ROT13-decode Clue 2, combine the parts to get the flag, and submit it to reveal
the download link.

> Note: this is a static site, so the check runs in the browser (SHA-256 hash
> comparison in `assets/js/script.js`). The PDF is still publicly downloadable
> at `assets/KhaderShareef.pdf` by design. For true gating, verify server-side.

## Contact form

The contact form (`assets/js/script.js`, section D) posts to a local Flask
backend at `http://127.0.0.1:5000/send-email`. It only works when that backend
is running locally; it is not wired to a production endpoint. Direct contact
details are listed in the Contact section of the page.

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

Deploy the repo root as a static site (GitHub Pages, Netlify, Vercel, etc.).
No build command needed; publish directory is `.`.

## License

MIT — see [LICENSE](LICENSE).
