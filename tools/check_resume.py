"""Verify the generated resume PDF is ATS-deliverable.

Checks: single page, author metadata set, expected sections present in the
content stream (via the generator source, since ReportLab subsets fonts).
Exits non-zero on failure.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "assets" / "KhaderShareef.pdf"
GEN = ROOT / "tools" / "build_resume.py"


def main():
    raw = PDF.read_bytes()
    pages = raw.count(b"/Type /Page") - raw.count(b"/Type /Pages")
    problems = []

    if pages != 1:
        problems.append(f"resume must be 1 page, found {pages}")
    if b"Un-named" in raw:
        problems.append("author metadata still 'Un-named'")
    if b"Khader Shareef Madani" not in raw:
        problems.append("author/title metadata missing")

    src = GEN.read_text(encoding="utf-8")
    for needle in ("SC-200", "Immediate joiner", "MITRE ATT&amp;CK",
                   "Incident Response", "UAE visa valid to Feb 2027"):
        if needle not in src:
            problems.append(f"generator missing expected content: {needle}")

    if problems:
        print("resume check FAILED:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"resume OK: {pages} page, author set, {PDF.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
