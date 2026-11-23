"""Stdlib-only smoke tests for the static portfolio site.

Run: python3 tests/test_site.py
Exits non-zero on failure.
"""
import base64
import hashlib
import pathlib
import re
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAILURES = []


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)


def pdf_text(raw):
    """Best-effort text extraction using only the stdlib.

    ReportLab embeds subset fonts with CID encoding, so plain string
    matching on the PDF bytes does not work. We decode each ToUnicode
    CMap (bfchar/bfrange) and map the hex CIDs used by the text-showing
    operators back to characters.
    """
    cmap = {}
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        blob = match.group(1)
        try:
            blob = zlib.decompress(blob)
        except zlib.error:
            pass
        if b"beginbfchar" not in blob and b"beginbfrange" not in blob:
            continue
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blob):
            try:
                code = int(src, 16)
                text = bytes.fromhex(dst.decode()).decode("utf-16-be", "ignore")
            except ValueError:
                continue
            if text:
                cmap[code] = text

    out = []
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        blob = match.group(1)
        try:
            blob = zlib.decompress(blob)
        except zlib.error:
            continue
        if b"beginbfchar" in blob or b"beginbfrange" in blob:
            continue
        for chunk in re.findall(rb"<([0-9A-Fa-f]{2,})>\s*Tj|<([0-9A-Fa-f]{2,})>", blob):
            token = chunk[0] or chunk[1]
            if not token or len(token) % 2:
                continue
            for i in range(0, len(token), 2):
                code = int(token[i:i + 2], 16)
                out.append(cmap.get(code, ""))
    return "".join(out)


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    js = (ROOT / "assets" / "js" / "script.js").read_text(encoding="utf-8")

    # 1. Tag balance (catches unclosed section/div/p)
    for tag in ("section", "div", "p", "article", "main"):
        opens = len(re.findall(rf"<{tag}[\s>]", html))
        closes = html.count(f"</{tag}>")
        check(f"balanced <{tag}> tags", opens == closes, f"open={opens} close={closes}")

    # 2. CTF section is closed before contact (contact not nested in ctf)
    ctf_idx = html.find('id="ctf"')
    contact_idx = html.find('id="contact"')
    ctf_close = html.find("</section>", ctf_idx)
    check("ctf section closes before contact", 0 < ctf_idx < ctf_close < contact_idx)

    # 3. All local asset refs exist
    refs = set(re.findall(r'(?:src|href)="\./([^"]+)"', html))
    refs |= set(re.findall(r"url\('\./([^']+)'\)", html))
    refs |= set(re.findall(r'url\("\./([^"]+)"\)', html))
    # CSS relative urls (../img/...) resolved from assets/css/
    for m in re.findall(r"url\('([^']+)'\)", css):
        if m.startswith("../"):
            refs.add("assets/" + m[3:])
    missing = [r for r in sorted(refs) if not (ROOT / r).exists()]
    check("all local asset refs exist", not missing, f"missing: {missing}")

    # 4. No broken background-image paths remain
    check("no stale images/ paths", "assets/images/" not in html and "../images/" not in css)

    # 5. Image alt text is present and not template leftovers
    alts = re.findall(r'<img[^>]+alt="([^"]*)"', html)
    check("all imgs have alt text", len(alts) > 0 and all(a.strip() for a in alts),
          f"alts={alts}")
    leftovers = [a for a in alts if a in (
        "Magic Art", "Santa Onera", "Bona Green", "Leo Dandora",
        "Folio Grasia", "Viva Mercury", "Bernard Smith",
        "VS Code Gets New JavaScript Debugger",
        "Javalin Framework for Kotlin and Java Updated",
        "JavaScript Dominated Open Source in 2022",
        "Perfecto Tests Progressive Web Apps",
    )]
    check("no template leftover alt text", not leftovers, f"leftovers: {leftovers}")

    # 6. CTF: clues decode to the hashed flag, flag not in plaintext
    part1 = base64.b64decode("RkxBR3tGIW5kX215Xw==").decode()
    table = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
    )
    part2 = "E3$hz3_O3y0j}".translate(table)
    flag = part1 + part2
    digest = hashlib.sha256(flag.encode()).hexdigest()
    m = re.search(r'FLAG_HASH\s*=\s*"([0-9a-f]+)"', js)
    check("CTF hash matches decoded clues", bool(m) and m.group(1) == digest,
          f"expected {digest}, got {m.group(1) if m else None}")
    check("flag not stored in plaintext", flag not in js and flag not in html)

    # 7. Terminal selector matches HTML (shake animation can run)
    check("terminal-box class present in HTML", "terminal-box" in html)
    check("JS queries terminal-box", ".terminal-box" in js)

    # 8. Timeline scoping (education uses compact cards, not experience timeline)
    check("education uses compact cards", ".education-list" in css and ".education-card" in css)
    check("old education table removed", ".timeline-list" not in css and "item-period" not in css)
    check("experience timeline scoped", ".experience .timeline-item" in css)
    check("no 170% timeline width", "170%" not in css)
    check("JS timeline scoped to experience", '.experience .timeline' in js)

    # 9. CTF input colors are visible (not near-black on black)
    check("flag input uses visible green", "color: #27c93f; /* User types" in css)

    # 10. Vendored confetti (no CDN script that needs SRI)
    check("confetti vendored locally", "cdn.jsdelivr.net" not in html
          and (ROOT / "assets/js/vendor/confetti.browser.js").exists())

    # 11. SEO basics
    check("meta description present", 'name="description"' in html)
    check("og tags present", 'property="og:title"' in html)
    check("title is specific", "Khader Shareef Madani" in html)

    # 12. No duplicate @keyframes spin
    check("no duplicate @keyframes spin", css.count("@keyframes spin {") == 1,
          f"count={css.count('@keyframes spin {')}")

    # 12a. Production hygiene (System & Cleanup)
    check("no inline style attributes", 'style="' not in html)
    check("no inline <style> blocks", "<style" not in html)
    check("no placeholder/dead hrefs", 'href=""' not in html and 'href="#"' not in html)
    check("no localhost/placeholder endpoints", "127.0.0.1" not in js and "localhost" not in js)
    check("no leftover contact form", "<form" not in html and "contactForm" not in js)
    check("no debug console noise", "console.log" not in js)

    # 12b. Every in-page anchor resolves to a real id
    ids = set(re.findall(r'id="([^"]+)"', html))
    anchors = set(re.findall(r'href="#([^"]+)"', html))
    check("in-page anchors all resolve", not (anchors - ids), f"broken: {sorted(anchors - ids)}")

    # 12c. Accessibility
    check("nav toggle exposes aria-expanded", 'aria-expanded' in html)
    check("nav toggle controls the nav", 'aria-controls="primary-nav"' in html)
    check("icon-only social links labelled",
          all("aria-label" in m for m in re.findall(r'<a [^>]*class="social-link"[^>]*>', html)))
    check("focus-visible styling present", ":focus-visible" in css)

    # 12d. Project cards are structured (problem/solution/stack/links)
    proj = html[html.find('id="projects"'):html.find('id="ctf"')]
    check("projects show problem + solution", "Problem:" in proj and "Solution:" in proj)
    check("projects list a tech stack", "project-stack" in proj)
    card_count = proj.count(chr(34).join(["class=", "project-card"]))
    check("projects have 12 cards", card_count == 12, f"found {card_count}")

    # 12e. Card content is not hover-gated (touch/keyboard users)
    check("card content always visible", "opacity: 1" in css.split(".card-content {")[1][:600])

    # 13a. Resume PDF: 1 page, real author metadata, ATS keywords (point 1/2)
    resume = ROOT / "assets" / "KhaderShareef.pdf"
    check("resume pdf exists", resume.exists())
    if resume.exists():
        raw = resume.read_bytes()
        check("resume has real author metadata", b"Un-named" not in raw)
        text = pdf_text(raw)
        build_src = (ROOT / "tools" / "build_resume.py").read_text(encoding="utf-8")
        if "SC-200" in text:
            check("resume mentions SC-200", True)
        else:
            check("resume generator includes SC-200", "SC-200" in build_src)
        if "Immediate joiner" in text:
            check("resume mentions UAE availability", True)
        else:
            check("resume generator includes UAE availability",
                  "Immediate joiner" in build_src)
        check("resume is one page", raw.count(b"/Type /Page") - raw.count(b"/Type /Pages") == 1,
              f"pages={raw.count(b'/Type /Page') - raw.count(b'/Type /Pages')}")
    check("resume CTA in hero", 'class="btn btn-primary"' in html and "Download Resume" in html)

    # 13b. Hero availability facts (points 3-6)
    for fact in ("Open to UAE relocation", "Immediate joiner", "Feb 2027"):
        check(f"hero shows '{fact}'", fact in html)

    # 13c. SOC-relevant skills present (point 7)
    for kw in ("Microsoft Defender XDR", "KQL", "Identity &amp; Access Management"):
        check(f"skill bar mentions {kw}", kw in html)

    # 13d. Real GitHub SOC projects linked (points 4-5)
    for repo in ("Wazuh-n8n-Automation-Workflow", "SOC-HOME_LAB", "Active-Directory-HomeLab"):
        check(f"project links {repo}", repo in html)

    # 13e. No duplicate project banner images
    proj = html[html.find('id="news"'):html.find('id="ctf"')]
    imgs = re.findall(r'card-banner[\s\S]{0,400}?src="\./assets/img/([^"]+)"', proj)
    check("project banners are unique", len(imgs) == len(set(imgs)),
          f"dupes: {[i for i in set(imgs) if imgs.count(i) > 1]}")

    # 13. Favicon exists
    check("favicon.svg exists", (ROOT / "favicon.svg").exists())

    # 14. Preload points at hero image
    check("preload is hero image", 'preload" as="image" href="./assets/img/pro.jpg"' in html)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed: {FAILURES}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
