"""Build the 1-page ATS-friendly UAE resume PDF.

Source of truth: KHADER_SHAREEF_MADANI_UAE_RESUME.pdf (user upload), with
ATS fixes applied:
  - author metadata set (was "Un-named")
  - missing ATS keywords added to the skills block
  - "riskbased" typo fixed
  - phone/email separation on the contact line
  - SC-200 (in progress) added to certifications
  - UAE availability line added
  - education end date aligned with LinkedIn (06/2026)

Run: python3 tools/build_resume.py
"""
import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "KhaderShareef.pdf"

FONT_DIR = pathlib.Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("DJ", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJB", str(FONT_DIR / "DejaVuSans-Bold.ttf")))

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#444444")
RULE = colors.HexColor("#999999")

BASE = 7.95
LEAD = 9.7


class Rule(Flowable):
    """Full-width horizontal rule."""

    def __init__(self, width, thickness=0.6, space_before=1, space_after=2, color=RULE):
        super().__init__()
        self.width_ = width
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after
        self.color = color

    def wrap(self, availWidth, availHeight):
        return (availWidth, self.thickness + self.space_before + self.space_after)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after
        self.canv.line(0, y, self.width_, y)


def styles():
    name = ParagraphStyle(
        "name", fontName="DJB", fontSize=19, leading=21, textColor=INK, spaceAfter=1
    )
    role = ParagraphStyle(
        "role", fontName="DJB", fontSize=9.6, leading=12, textColor=MUTED, spaceAfter=2
    )
    contact = ParagraphStyle(
        "contact", fontName="DJ", fontSize=BASE, leading=LEAD, textColor=MUTED
    )
    section = ParagraphStyle(
        "section",
        fontName="DJB",
        fontSize=9.4,
        leading=11,
        textColor=INK,
        spaceBefore=3.6,
        spaceAfter=0.6,
    )
    body = ParagraphStyle(
        "body",
        fontName="DJ",
        fontSize=BASE,
        leading=LEAD,
        textColor=INK,
        alignment=TA_JUSTIFY,
    )
    bullet = ParagraphStyle(
        "bullet",
        fontName="DJ",
        fontSize=BASE,
        leading=LEAD,
        textColor=INK,
        leftIndent=9,
        bulletIndent=1,
        spaceAfter=0.4,
    )
    jobhead = ParagraphStyle(
        "jobhead", fontName="DJ", fontSize=BASE, leading=LEAD, textColor=INK
    )
    small = ParagraphStyle(
        "small", fontName="DJ", fontSize=7.9, leading=9.9, textColor=MUTED
    )
    return dict(
        name=name,
        role=role,
        contact=contact,
        section=section,
        body=body,
        bullet=bullet,
        jobhead=jobhead,
        small=small,
    )


def bullets(items, st):
    """Bulleted paragraphs with a real glyph bullet (ATS-safe plain text)."""
    out = []
    style = st["bullet"]
    for text in items:
        out.append(Paragraph(text, style, bulletText="\u2022"))
    return out


def heading(text, st, width):
    return [Paragraph(text.upper(), st["section"]), Rule(width)]


def build():
    st = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=13 * mm,
        rightMargin=13 * mm,
        topMargin=8 * mm,
        bottomMargin=7 * mm,
        title="Khader Shareef Madani - Cybersecurity Analyst (UAE)",
        author="Khader Shareef Madani",
        subject="Curriculum Vitae - Cybersecurity Analyst / SOC Analyst / IAM",
        keywords=(
            "SOC Analyst, Cybersecurity Analyst, Microsoft Sentinel, KQL, "
            "Defender XDR, Entra ID, PingOne, IAM, Incident Response, "
            "MITRE ATT&CK, Threat Intelligence, Splunk, UAE"
        ),
        creator="Khader Shareef Madani",
    )
    W = doc.width
    f = []

    # ---------- header ----------
    f.append(Paragraph("KHADER SHAREEF MADANI", st["name"]))
    f.append(
        Paragraph(
            "Cybersecurity Analyst &nbsp;|&nbsp; SOC Analyst &nbsp;|&nbsp; "
            "AI Threat Validation &nbsp;|&nbsp; IAM &amp; Identity Security",
            st["role"],
        )
    )
    f.append(
        Paragraph(
            "+971 56 951 5117 (UAE) &nbsp;|&nbsp; +91 95157 87655 (India) &nbsp;|&nbsp; "
            "infa.khadershareef@gmail.com",
            st["contact"],
        )
    )
    f.append(
        Paragraph(
            "linkedin.com/in/khader-shareef-madani-129167260 &nbsp;|&nbsp; "
            "github.com/KHADERSHAREEF19 &nbsp;|&nbsp; khadershareef19.vercel.app",
            st["contact"],
        )
    )
    f.append(
        Paragraph(
            "<b>UAE-ready: Immediate joiner &nbsp;·&nbsp; UAE visa valid to Feb 2027 "
            "&nbsp;·&nbsp; Open to relocation across UAE &amp; GCC</b>",
            st["contact"],
        )
    )
    f.append(Rule(W, thickness=0.9, space_before=3, space_after=1))

    # ---------- summary ----------
    f += heading("Professional Summary", st, W)
    f.append(
        Paragraph(
            "Cybersecurity Analyst with hands-on experience in enterprise 24/7 "
            "Multi-Tenant Organization (MTO) SOC environments. Specialized in cross-vector "
            "threat triage across Microsoft Defender XDR (MDO, MDE, MDI, Entra ID, MDCA) and "
            "Microsoft Sentinel, incident response and containment, MITRE ATT&amp;CK-driven "
            "threat hunting, and custom Windows log visualization tooling. Currently working "
            "with PingOne and Microsoft Entra ID on SSO, MFA and identity security. Secured "
            "3rd Rank for Academic Excellence in B.E. CSE (Cybersecurity) across all Osmania "
            "University-affiliated colleges in Telangana State.",
            st["body"],
        )
    )

    # ---------- certifications ----------
    f += heading("Certifications", st, W)
    f.append(
        Paragraph(
            "<b>CCNA</b> – Cisco &nbsp;·&nbsp; <b>CompTIA Network+</b> – CompTIA &nbsp;·&nbsp; "
            "<b>Certified in Cybersecurity (CC)</b> – ISC2 &nbsp;·&nbsp; "
            "<b>CBTP</b> – Certified Blue Team Practitioner, The SecOps Group &nbsp;·&nbsp; "
            "<b>CNSP</b> – Certified Network Security Practitioner &nbsp;·&nbsp; "
            "<b>CSEDP</b> – Certified Social Engineering Defense Practitioner",
            st["small"],
        )
    )
    f.append(
        Paragraph(
            "SOC Level 1 – TryHackMe &nbsp;·&nbsp; DevSecOps – TryHackMe &nbsp;·&nbsp; "
            "Fundamentals of Cybersecurity – IBM &nbsp;·&nbsp; "
            "<b>Microsoft SC-200</b> (Security Operations Analyst) – In Progress",
            st["small"],
        )
    )

    # ---------- skills ----------
    f += heading("Technical Skills", st, W)
    skill_rows = [
        (
            "Security Operations",
            "SIEM (Microsoft Sentinel, Splunk Enterprise, Wazuh), Microsoft Defender XDR "
            "(MDO, MDE, MDI, MDCA), Log Analysis, Incident Response (IR playbooks), "
            "Threat Triage, MITRE ATT&amp;CK mapping, Threat Intelligence (CTI), "
            "Malware Analysis, EDR, SOAR (playbook-driven), Jira and ServiceNow ticketing, "
            "ISO 27001 awareness, NIST CSF",
        ),
        (
            "Identity &amp; Access Management",
            "PingOne (Workforce, Protect, DaVinci, Verify), Microsoft Entra ID, SSO, "
            "SAML 2.0, OIDC, MFA, RBAC, Customer IAM (CIAM), Privileged Access Management "
            "(PAM), PingAM, Okta and Saviynt (basic exposure)",
        ),
        (
            "Network &amp; Perimeter Security",
            "Fortinet FortiGate, Firewall policy, TCP/IP, Active Directory, DNS, VPNs, "
            "Wireshark, Nmap, OWASP ZAP, Burp Suite",
        ),
        (
            "Programming &amp; Automation",
            "Python, KQL, Bash, PowerShell, SQL, Git/GitHub, Docker, n8n, OpenClaw",
        ),
        (
            "Cloud &amp; Infrastructure",
            "AWS, Azure, Linux (Arch &amp; Ubuntu), Windows Server (2019/2022), Kubernetes",
        ),
    ]
    for label, text in skill_rows:
        f.append(
            Paragraph(f"<b>{label}:</b> {text}", st["small"])
        )
        f.append(Spacer(1, 1.2))

    # ---------- experience ----------
    f += heading("Work Experience", st, W)

    jobs = [
        (
            "Identity &amp; Access Management (IAM) Intern",
            "North Star Identity",
            "10/2026 – Present",
            "Texas, USA (Remote)",
            [
                "Configured enterprise Single Sign-On (SSO) integrations on PingOne Workforce "
                "using OIDC and SAML 2.0, managing user directories, custom attributes and "
                "Role-Based Access Control (RBAC) policies.",
                "Configured adaptive Multi-Factor Authentication (MFA) and threat-protection "
                "rules in PingOne Protect, applying risk-based step-up authentication driven by "
                "contextual risk signals and suspicious activity.",
                "Built identity workflows in PingOne DaVinci and integrated PingOne Verify for "
                "identity proofing (ID and selfie verification); reviewed platform audit logs to "
                "troubleshoot authentication failures.",
            ],
        ),
        (
            "AI Threat Validation Analyst",
            "Cyber Managed Services Inc. (CyberMSI)",
            "06/2026 – 07/2026",
            "Chicago, USA (Remote)",
            [
                "Monitored real-time alert streams across enterprise multi-tenant environments "
                "using Microsoft Sentinel and Defender XDR platforms.",
                "Conducted precise incident qualification to separate True Positives from False "
                "Positives across endpoint, email, and identity telemetry.",
                "Analyzed email header components (SPF, DKIM, DMARC), sandboxed payloads, and "
                "verified IOC reputations to mitigate phishing and business email compromise.",
                "Executed rapid first-response containment including network isolation of "
                "compromised hosts, file quarantines, and active session revocations.",
                "Drafted clear 5Ws (Who, What, Where, When, Why) investigation reports strictly "
                "adhering to client SLAs and corporate SOPs.",
            ],
        ),
    ]
    for title, org, dates, loc, pts in jobs:
        f.append(
            Paragraph(f"<b>{title}</b> &nbsp;—&nbsp; {org}", st["jobhead"])
        )
        f.append(Paragraph(f"{dates} &nbsp;|&nbsp; {loc}", st["small"]))
        f.extend(bullets(pts, st))

    # ---------- projects ----------
    f += heading("Projects", st, W)
    projects = [
        (
            "Home Lab: SOC Operations Environment",
            [
                "Built a virtualized SOC lab (Kali, Ubuntu Server, Windows 10 Pro) with Splunk "
                "SIEM and EDR to detect brute-force and suspicious login activity.",
            ],
        ),
        (
            "Active Directory Home Lab: Windows Domain Administration",
            [
                "Deployed Windows Server 2016 as an AD DS domain controller with DNS zones, OUs "
                "and Group Policy; delegated password resets (least-privilege access).",
            ],
        ),
        (
            "CereloX: Windows Event Log Visualization Tool",
            [
                "Python tool that parses and visualizes Windows Event Logs for faster triage; "
                "95% detection accuracy across 15+ simulated brute-force patterns.",
            ],
        ),
        (
            "SecureWipe: Data Sanitization Tool (SIH 2025 Finalist)",
            [
                "Secure data sanitization tool preventing forensic recovery; 25% faster wiping "
                "via multi-threaded disk I/O.",
            ],
        ),
    ]

    for title, pts in projects:
        f.append(Paragraph(f"<b>{title}</b>", st["jobhead"]))
        f.extend(bullets(pts, st))

    # ---------- education ----------
    f += heading("Education", st, W)
    f.append(
        Paragraph(
            "<b>Bachelor of Engineering (Cybersecurity, IoT and Blockchain Technology)</b> "
            "&nbsp;—&nbsp; Osmania University, Hyderabad",
            st["jobhead"],
        )
    )
    f.append(Paragraph("11/2022 – 06/2026 &nbsp;|&nbsp; 8.19 CGPA", st["small"]))

    # ---------- achievements ----------
    f += heading("Achievements", st, W)
    f.extend(
        bullets(
            [
                "3rd Rank in B.E. CSE (Cybersecurity): state-wide academic rank among Osmania "
                "University-affiliated colleges in Telangana.",
                "Smart India Hackathon 2025: national-level finalist for SecureWipe.",
                "TryHackMe Top 2% globally; CTF solver on Hack The Box, picoCTF and Root-Me; "
                "KodeKloud System Administrator (25,000+ points).",
            ],
            st,
        )
    )

    doc.build(f)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
