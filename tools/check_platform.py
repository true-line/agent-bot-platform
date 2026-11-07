#!/usr/bin/env python3
"""check_platform.py: the drift gate for agent-bot-platform.

Run from the repository root:

    .venv/bin/python tools/check_platform.py

Errors fail the run (exit 1). Warnings are reported, never fatal; they list
known gaps that are tracked elsewhere (trace gaps, seams without a contract).

Checks
  documents   front matter, status vocabulary, one H1 then a summary,
              no placeholders, no positional references, no machine-local
              paths, no conversion artifacts, every page in the mkdocs nav
  identifiers every R, T, PDR, WP, S, X and DRIFT cited in a controlled
              document resolves; repo-local ADRs are cited with their repo;
              retired labels are not used
  registries  requirements and tests agree in both directions; repos and
              seams agree on provider and consumer; each paper conversion
              matches its SHA-256 pin (and each private original too, when
              PLATFORM_SOURCES_DIR points at the owner's copy); PDR records
              carry Status, Date and Discussion and pass the platform test
  generated   every generated page matches tools/gen_docs.py output
  privacy     no personal or legal records anywhere in the tree that git
              would commit: no legal/identity filings by path or name, no
              binaries outside doc assets, no street addresses, ZIP+4 codes,
              phone numbers or personal email, and none of the owner's
              private terms (names) listed outside the repository in
              $PLATFORM_PRIVATE_TERMS or ~/.config/agent-bot-platform/private-terms

Run only the privacy check (fast):

    .venv/bin/python tools/check_platform.py --privacy

Papers and archive pages (Doc-Type paper or archive) are frozen provenance
and only get the document hygiene checks.
"""
import datetime
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "tools"))
import gen_docs  # noqa: E402

DOC_TYPES = {
    "index", "governance", "concept", "requirements", "explanation", "interface",
    "decision", "security", "intelligence", "strategy", "plan", "report",
    "runbook", "how-to", "tutorial", "reference", "paper", "archive", "generated",
}
STATUSES = {"Draft", "Proposed", "Accepted", "Superseded", "Retired", "Frozen"}
FROZEN_TYPES = {"paper", "archive"}
REVIEW_MAX_DAYS = 90

PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")
POSITIONAL = [
    re.compile(r"\b(?:see|discussed|mentioned|described|noted|shown|listed|outlined|explained)\s+(?:above|below|earlier|previously)\b", re.I),
    re.compile(r"\bas\s+(?:above|below)\b", re.I),
    re.compile(r"\bthe\s+(?:above|below)\s+(?:section|table|list|example|diagram|steps?|rules?)\b", re.I),
]
LOCAL_PATH = re.compile(r"/Users/|/private/tmp/|/var/folders/|(?<![\w.])/tmp/")
ARTIFACT = re.compile(r"&nbsp;|<o:p>|</o:p>|&#[0-9]+;")

ID_PATTERNS = {
    "R": re.compile(r"(?<![\w.-])R(\d{1,3})(?![\w-])"),
    "T": re.compile(r"(?<![\w.-])T(\d{2})(?![\w:-])"),
    "PDR": re.compile(r"(?<![\w-])PDR-(\d{4})(?![\w-])"),
    "WP": re.compile(r"(?<![\w-])WP(\d+)(?![\w-])"),
    "S": re.compile(r"(?<![\w.§-])S(\d{1,2})(?![\w-])"),
    "X": re.compile(r"(?<![\w-])X(\d{1,2})(?![\w-])"),
    "DRIFT": re.compile(r"(?<![\w-])DRIFT-(\d{3})(?![\w-])"),
    "QA": re.compile(r"(?<![\w-])QA-([A-Z0-9]{3,4}-\d{2})(?![\w-])"),
}
ADR = re.compile(r"(?:([\w.-]+)(?:/|\s+|#))?ADR-\d{4}")
LEGACY_DECISION = re.compile(r"(?<![\w.-])([DA])([1-9])(?![\w-])")
PDR_AFFECTS_TERMS = {"topology", "trust-model", "scope", "quality-bar", "governance"}

# Privacy: personal and legal records never enter this repository. It is
# shared with every agent that works on the platform and may be published.
PRIVATE_PATH = re.compile(
    r"(?i)(^|/)(\.local|legal|private|secrets?)(/|$)"
    r"|finaldocument_|certificate[-_ ]of[-_ ]formation|articles[-_ ]of[-_ ]organi[sz]ation"
    r"|operating[-_ ]agreement|(^|[-_/])(ein|ss-?4|w-?9|1099)([-_.]|$)|passport|driver'?s?[-_ ]licen[cs]e"
)
BINARY_OK = re.compile(r"^docs/(.+/)?assets/[^/]+\.(png|svg|drawio|mmd)$")
PRIVATE_TERMS_FILE = Path.home() / ".config" / "agent-bot-platform" / "private-terms"
PRIVATE_TEXT = [
    ("street address", re.compile(
        r"\b\d{1,6}\s+(?:[NSEW]\.?\s+)?(?:[A-Z][a-z]+\s+){1,3}"
        r"(?:St|Street|Ln|Lane|Rd|Road|Ave|Avenue|Dr|Drive|Blvd|Boulevard|Ct|Court|Way|Pkwy|Parkway|Cir|Circle|Trl|Trail|Pl|Place|Hwy)\b\.?")),
    ("ZIP+4 code", re.compile(r"\b\d{5}-\d{4}\b")),
    ("phone number", re.compile(r"(?<![\w.-])\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?![\w-])")),
    ("personal email", re.compile(
        r"\b[\w.%+-]+@(?!(?:example\.(?:com|org)|users\.noreply\.github\.com|anthropic\.com)\b)[\w-]+(?:\.[\w-]+)+\b")),
]
EMAIL_OK = re.compile(r"^(noreply|no-reply|git|security|support)@", re.I)

errors = []
warnings = []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


def load(name):
    with open(ROOT / "registry" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def split_front(text):
    if not text.startswith("---\n"):
        return None, text, 0
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text, 0
    meta = yaml.safe_load(text[4:end]) or {}
    body = text[end + 5:]
    return meta, body, text[: end + 5].count("\n")


def mask_code(lines):
    out, fence = [], None
    for line in lines:
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m and fence is None:
            fence = m.group(1)[0]
            out.append("")
            continue
        if m and fence and m.group(1)[0] == fence:
            fence = None
            out.append("")
            continue
        if fence:
            out.append("")
            continue
        line = re.sub(r"(`+)(.+?)\1", lambda mm: " " * len(mm.group(0)), line)
        line = re.sub(r"<!--.*?-->", "", line)
        out.append(line)
    return out


def nav_pages(nav):
    pages = []
    for item in nav:
        if isinstance(item, str):
            pages.append(item)
        elif isinstance(item, dict):
            for v in item.values():
                if isinstance(v, str):
                    pages.append(v)
                else:
                    pages.extend(nav_pages(v))
    return pages


def build_index():
    reqs = load("requirements.yaml")
    req, qa = reqs["requirements"], reqs.get("quality-attributes") or []
    tests = load("tests.yaml")["tests"]
    src = load("sources.yaml")
    repos = load("repos.yaml")
    seams = load("seams.yaml")["seams"]
    drift_ids = set(re.findall(r"^## (DRIFT-\d{3})\b", (DOCS / "00-governance/drift-register.md").read_text(encoding="utf-8"), re.M))
    pdrs = {}
    for p in sorted((DOCS / "04-decisions").glob("PDR-*.md")):
        m = re.match(r"PDR-(\d{4})-", p.name)
        if not m:
            err(str(p.relative_to(ROOT)), "PDR filename must be PDR-NNNN-slug.md")
        elif m.group(1) in pdrs:
            err(str(p.relative_to(ROOT)), f"PDR-{m.group(1)} is already used by {pdrs[m.group(1)].name}; a PDR number is its discussion number")
        else:
            pdrs[m.group(1)] = p
    return {
        "req": req, "qa": qa, "tests": tests, "src": src, "repos": repos, "seams": seams,
        "ids": load("ids.yaml"),
        "R": {r["id"][1:] for r in req},
        "QA": {q["id"][3:] for q in qa},
        "T": {t["id"][1:] for t in tests},
        "PDR": set(pdrs), "pdr_files": pdrs,
        "WP": {str(i) for i in range(1, 8)},
        "S": {s["id"][1:] for s in src["sources"]},
        "X": {x["id"][1:] for x in src["external"]},
        "DRIFT": {d.split("-")[1] for d in drift_ids},
        "repo_names": {r["name"] for r in repos["repos"]} | {g["name"] for g in repos["governance"]},
    }


def check_document(path, idx, nav):
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8")
    meta, body, offset = split_front(text)
    if meta is None:
        err(rel, "missing YAML front matter")
        return
    for key in ("Status", "Doc-Type", "Owner"):
        if not meta.get(key):
            err(rel, f"front matter missing {key}")
    status, dtype = meta.get("Status"), meta.get("Doc-Type")
    if dtype and dtype not in DOC_TYPES:
        err(rel, f"unknown Doc-Type {dtype!r}")
    if status and status not in STATUSES:
        err(rel, f"unknown Status {status!r}")
    if dtype == "paper" and status != "Frozen":
        err(rel, "papers are Frozen")
    if status == "Frozen" and dtype != "paper":
        err(rel, "only papers may be Frozen")
    if status == "Superseded" and not meta.get("Superseded-By"):
        err(rel, "Superseded needs Superseded-By")
    if dtype not in FROZEN_TYPES | {"generated"}:
        lr = meta.get("Last-Reviewed")
        if not lr:
            err(rel, "front matter missing Last-Reviewed")
        else:
            try:
                age = (datetime.date.today() - datetime.date.fromisoformat(str(lr))).days
                if status == "Accepted" and age > REVIEW_MAX_DAYS:
                    warn(rel, f"Accepted but not reviewed for {age} days")
            except ValueError:
                err(rel, f"Last-Reviewed {lr!r} is not YYYY-MM-DD")

    rel_docs = str(path.relative_to(DOCS))
    if rel_docs not in nav:
        err(rel, "not in mkdocs.yml nav (agents and readers cannot find it)")

    lines = body.split("\n")
    masked = mask_code(lines)
    headings = [(i, len(m.group(1))) for i, l in enumerate(masked) if (m := re.match(r"^(#{1,6})\s+\S", l))]
    if not headings or headings[0][1] != 1:
        err(rel, "first heading must be the single H1")
    elif sum(1 for _, lvl in headings if lvl == 1) > 1:
        err(rel, "more than one H1")
    else:
        h1 = headings[0][0]
        nxt = next((l for l in masked[h1 + 1:] if l.strip() and not l.startswith("<!--")), "")
        if not nxt or nxt.startswith(("#", "|", "```", "-", "*", "1.")):
            if dtype not in FROZEN_TYPES:
                err(rel, "no summary paragraph directly after the H1")
    prev = 0
    for i, lvl in headings:
        if prev and lvl > prev + 1 and dtype not in FROZEN_TYPES:
            err(f"{rel}:{i + offset + 1}", f"heading level skips from H{prev} to H{lvl}")
        prev = lvl

    for n, (raw, line) in enumerate(zip(lines, masked), start=offset + 1):
        where = f"{rel}:{n}"
        if LOCAL_PATH.search(raw):
            err(where, "machine-local path")
        if ARTIFACT.search(raw):
            err(where, "conversion artifact")
        if dtype in FROZEN_TYPES:
            continue
        if PLACEHOLDER.search(line):
            err(where, f"placeholder {PLACEHOLDER.search(line).group(1)!r} in controlled text")
        for pat in POSITIONAL:
            if pat.search(line):
                err(where, f"positional reference {pat.search(line).group(0)!r}; link the target instead")
        for kind, pat in ID_PATTERNS.items():
            for m in pat.finditer(line):
                if m.group(1) not in idx[kind]:
                    err(where, f"{kind}{'-' if kind in ('PDR', 'DRIFT', 'QA') else ''}{m.group(1)} does not resolve in its registry")
        for m in ADR.finditer(line):
            qual = (m.group(1) or "").split("/")[-1]
            if qual not in idx["repo_names"]:
                err(where, f"{m.group(0).strip()!r}: cite a repo-local ADR with its repository, e.g. 'agent-comms ADR-0028'")
        for m in LEGACY_DECISION.finditer(line):
            before = line[: m.start()].rstrip()
            if not (before.endswith("S1") or before.endswith("agent-bot-daemon")):
                err(where, f"{m.group(0)} is a retired label; qualify it ('S1 {m.group(0)}' or 'agent-bot-daemon {m.group(0)}')")


def check_registries(idx):
    tests = idx["tests"]
    qa_ns = next(n for n in idx["ids"]["namespaces"] if n["prefix"] == "QA")
    for q in idx["qa"]:
        where = f"registry/requirements.yaml:{q.get('id')}"
        if not re.fullmatch(qa_ns["pattern"], str(q.get("id", ""))):
            err(where, f"QA id must match {qa_ns['pattern']} (registry/ids.yaml)")
        for key in ("title", "statement", "status", "source", "specified-in", "first-gate"):
            if not q.get(key):
                err(where, f"missing {key}")
    req = idx["req"] + idx["qa"]
    rid = [r["id"] for r in req]
    tid = [t["id"] for t in tests]
    for name, seq in (("requirement", rid), ("test", tid)):
        dup = {x for x in seq if seq.count(x) > 1}
        if dup:
            err("registry", f"duplicate {name} ids {sorted(dup)}")
    r_to_t = {r["id"]: set(r.get("verified-by", [])) for r in req}
    t_to_r = {t["id"]: set(t.get("verifies", [])) for t in tests}
    for r, ts in r_to_t.items():
        for t in ts:
            if t not in t_to_r:
                err("registry/requirements.yaml", f"{r} verified-by unknown test {t}")
            elif r not in t_to_r[t]:
                err("registry/tests.yaml", f"{t} must list {r} in verifies (requirements.yaml says {r} is verified by {t})")
        if not ts and not req[rid.index(r)].get("verified-by-other"):
            err("registry/requirements.yaml", f"{r} has no verification method")
    for t, rs in t_to_r.items():
        for r in rs:
            if r not in r_to_t:
                err("registry/tests.yaml", f"{t} verifies unknown requirement {r}")
            elif t not in r_to_t[r]:
                err("registry/requirements.yaml", f"{r} must list {t} in verified-by")
    gaps = [t["id"] for t in tests if not t.get("verifies")]
    for t in tests:
        if not t.get("verifies") and not t.get("trace-gap"):
            err("registry/tests.yaml", f"{t['id']} verifies nothing and records no trace-gap")
    if gaps:
        warn("traceability", f"{len(gaps)} tests verify no requirement: {', '.join(gaps)}")

    repos = idx["repos"]["repos"]
    seams = {s["id"]: s for s in idx["seams"]}
    names = {r["name"] for r in repos}
    allowed = {"keep", "keep-and-split", "designate", "merge-into-agent-bot", "archive", "decide", "adjacent"}
    for r in repos:
        where = f"registry/repos.yaml:{r['name']}"
        if r["disposition"] not in allowed:
            err(where, f"unknown disposition {r['disposition']}")
        if r["disposition"] in {"keep", "keep-and-split", "designate"} and not r.get("criteria"):
            err(where, "a kept repository must meet at least one admission criterion")
        for key in ("provides", "consumes"):
            for s in r.get(key, []):
                if s not in seams:
                    err(where, f"{key} unknown seam {s}")
    for s in seams.values():
        where = f"registry/seams.yaml:{s['id']}"
        if s["provider"] not in names:
            err(where, f"provider {s['provider']} not in repos.yaml")
        elif s["id"] not in next(r for r in repos if r["name"] == s["provider"]).get("provides", []):
            err(where, f"{s['provider']} must list {s['id']} in provides")
        for c in s.get("consumers", []):
            if c not in names:
                err(where, f"consumer {c} not in repos.yaml")
            elif s["id"] not in next(r for r in repos if r["name"] == c).get("consumes", []):
                err(where, f"{c} must list {s['id']} in consumes")
        if s["contract-status"] in {"none", "plan", "repo-local"} and s.get("consumers"):
            warn("seams", f"{s['id']} is consumed by {len(s['consumers'])} repos but its contract is {s['contract-status']}")
    for r in repos:
        for s in r.get("provides", []):
            if s in seams and seams[s]["provider"] != r["name"]:
                err(f"registry/repos.yaml:{r['name']}", f"claims to provide {s}, but seams.yaml names {seams[s]['provider']}")

    originals_dir = os.environ.get("PLATFORM_SOURCES_DIR")
    for s in idx["src"]["sources"]:
        versions = [s] + list(s.get("superseded_versions", []))
        for v in versions:
            original, converted = v["original"], v.get("converted")
            if "/" in original:
                err("registry/sources.yaml", f"{s['id']} original {original!r} must be a bare filename; originals stay outside the repository")
            if originals_dir:
                p = Path(originals_dir).expanduser() / original
                if not p.exists():
                    err("registry/sources.yaml", f"{s['id']} original not found in PLATFORM_SOURCES_DIR: {original}")
                elif hashlib.sha256(p.read_bytes()).hexdigest() != v["sha256"]:
                    err("registry/sources.yaml", f"{s['id']} original does not match its pin: {original}")
            if converted:
                c = ROOT / converted
                if not c.exists():
                    err("registry/sources.yaml", f"{s['id']} conversion missing: {converted}")
                elif hashlib.sha256(c.read_bytes()).hexdigest() != v.get("converted_sha256"):
                    err("registry/sources.yaml", f"{s['id']} conversion {converted} changed without updating converted_sha256 (papers are frozen)")

    for num, p in idx["pdr_files"].items():
        rel = str(p.relative_to(ROOT))
        meta, body, _ = split_front(p.read_text(encoding="utf-8"))
        meta = meta or {}
        for key in ("Status", "Date", "Discussion"):
            if not meta.get(key):
                err(rel, f"PDR front matter missing {key}")
        if meta.get("Doc-Type") != "decision":
            err(rel, "PDR Doc-Type must be decision")
        disc = str(meta.get("Discussion", ""))
        m = re.match(r"^https://github\.com/true-line/agent-bot-platform/discussions/(\d+)$", disc)
        if not m:
            err(rel, "Discussion must be the decision discussion URL in true-line/agent-bot-platform")
        elif int(m.group(1)) != int(num):
            err(rel, f"PDR-{num} must match its discussion number (found #{m.group(1)})")
        if not re.search(rf"^# PDR-{num}\b", body, re.M):
            err(rel, f"H1 must start with PDR-{num}")
        if meta.get("Status") == "Accepted" and not meta.get("Accepted"):
            err(rel, "Accepted PDR needs an Accepted date")
        # The platform test (00-governance/change-control.md): a PDR binds two
        # or more repositories, or changes a seam, requirement, quality bar,
        # trust model, topology or scope. Otherwise it is a repo-local ADR.
        affects_repos = meta.get("Affects-Repos") or []
        affects = meta.get("Affects") or []
        for r in affects_repos:
            if r not in idx["repo_names"]:
                err(rel, f"Affects-Repos names unknown repository {r!r}")
        seam_ids = {s["id"] for s in idx["seams"]}
        bad = [a for a in affects if not (a in seam_ids or a in PDR_AFFECTS_TERMS
               or re.fullmatch(r"R\d+|QA-[A-Z0-9]{3,4}-\d{2}", str(a)))]
        if bad:
            err(rel, f"Affects items must be seam ids, R/QA ids or one of {sorted(PDR_AFFECTS_TERMS)}; got {bad}")
        if len(affects_repos) < 2 and not affects:
            err(rel, "fails the platform test: needs two or more Affects-Repos or a platform-level Affects; "
                     "a decision inside one repository is that repository's ADR")


def check_generated():
    for rel, text in gen_docs.render_all().items():
        p = ROOT / rel
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            err(rel, "out of date; run tools/gen_docs.py")


def committable_files():
    """Every file git would commit: tracked plus untracked-but-not-ignored."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode()
        return sorted({f for f in out.split("\0") if f and (ROOT / f).is_file()})
    except (OSError, subprocess.CalledProcessError):
        skip = {".git", ".venv", "site"}
        return sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                      if p.is_file() and not skip & set(p.relative_to(ROOT).parts))


def private_terms():
    """Owner-private terms (names). Never stored in the repository."""
    raw = os.environ.get("PLATFORM_PRIVATE_TERMS", "")
    if PRIVATE_TERMS_FILE.exists():
        raw += "\n" + PRIVATE_TERMS_FILE.read_text(encoding="utf-8")
    terms = [x.strip() for x in re.split(r"[\n,]", raw) if x.strip() and not x.strip().startswith("#")]
    return re.compile(r"(?i)(?<![\w])(?:" + "|".join(re.escape(x) for x in terms) + r")(?![\w])") if terms else None


def check_privacy():
    names = private_terms()
    for rel in committable_files():
        if PRIVATE_PATH.search(rel):
            err(rel, "looks like a personal or legal record; keep it outside this repository")
            continue
        data = (ROOT / rel).read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if text is None or b"\0" in data[:8192]:
            if not BINARY_OK.match(rel):
                err(rel, "binary file outside sources/papers and docs assets; pin it in registry/sources.yaml or keep it out")
            continue
        for n, line in enumerate(text.split("\n"), start=1):
            if names and names.search(line):
                err(f"{rel}:{n}", "contains one of the owner's private terms (a personal name); replace it with 'True Line AI' or 'the owner'")
            for label, pat in PRIVATE_TEXT:
                for m in pat.finditer(line):
                    if label == "personal email" and EMAIL_OK.match(m.group(0)):
                        continue
                    err(f"{rel}:{n}", f"possible {label}; personal data does not belong in this repository")


def main():
    if "--privacy" in sys.argv[1:]:
        check_privacy()
        for e in errors:
            print("error:", e)
        print(f"privacy: {len(errors)} errors" + ("" if private_terms() else " (no private-terms list found; names not checked)"))
        return 1 if errors else 0
    nav = set(nav_pages(yaml.load((ROOT / "mkdocs.yml").read_text(), Loader=yaml.BaseLoader)["nav"]))
    idx = build_index()
    docs = sorted(DOCS.rglob("*.md"))
    for path in docs:
        check_document(path, idx, nav)
    for page in nav:
        if not (DOCS / page).exists():
            err("mkdocs.yml", f"nav entry {page} does not exist")
    check_registries(idx)
    check_generated()
    check_privacy()
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    print(f"\n{len(docs)} documents, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
