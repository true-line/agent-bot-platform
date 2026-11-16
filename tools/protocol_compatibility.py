"""Offline structure/citation gate; conformance verifies immutable source bytes."""
import re
from pathlib import PurePosixPath

DECISION_PATH = "docs/04-decisions/PDR-0075-t14-supported-major-inventory-and-profile-evidence.md"


def validate_inventory(data, decision_status, repositories):
    """Return findings without treating an absent or proposed decision as accepted."""
    findings = []
    if not isinstance(data, dict) or set(data) != {
        "schema_version", "status", "decision", "decision_path", "protocols"
    }:
        return ["inventory fields are incomplete or unknown"]
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        findings.append("schema_version must be 1")
    if data["status"] != "Accepted" or data["decision"] != "PDR-0075" or data["decision_path"] != DECISION_PATH:
        findings.append("inventory must cite Accepted PDR-0075 at its canonical path")
    if decision_status != "Accepted":
        findings.append("cited decision is not Accepted")
    protocols = data["protocols"]
    if not isinstance(protocols, dict) or set(protocols) != {"hq", "wire"}:
        return findings + ["inventory must contain exactly hq and wire"]
    for family, record in protocols.items():
        if not isinstance(record, dict) or set(record) != {
            "current_major", "previous_supported_major", "first_supported_major", "evidence"
        }:
            findings.append(f"{family}: protocol fields are incomplete or unknown")
            continue
        first, current, previous = (record[k] for k in (
            "first_supported_major", "current_major", "previous_supported_major"
        ))
        if not (type(first) is int and type(current) is int
                and first == current == 1 and previous is None):
            findings.append(f"{family}: this accepted inventory permits only first/current major 1 and no previous major")
        evidence = record["evidence"]
        if not isinstance(evidence, list) or not evidence:
            findings.append(f"{family}: immutable source evidence is required")
            continue
        seen = set()
        for source in evidence:
            if not isinstance(source, dict) or set(source) != {"repository", "commit", "path", "sha256"}:
                findings.append(f"{family}: source evidence fields are incomplete or unknown")
                continue
            if not all(isinstance(v, str) for v in source.values()):
                findings.append(f"{family}: source evidence fields must be strings")
                continue
            path = PurePosixPath(source["path"])
            if source["repository"] not in repositories:
                findings.append(f"{family}: evidence repository is not in the platform catalog")
            if not re.fullmatch(r"[0-9a-f]{40}", source["commit"]) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
                findings.append(f"{family}: evidence needs a full commit and SHA-256")
            if not re.fullmatch(r"[A-Za-z0-9._/-]+", source["path"]) or path.is_absolute() or ".." in path.parts or str(path) != source["path"]:
                findings.append(f"{family}: evidence path must be a canonical repository-relative file")
            key = (source["repository"], source["commit"], source["path"])
            if key in seen:
                findings.append(f"{family}: duplicate source evidence")
            seen.add(key)
    return findings
