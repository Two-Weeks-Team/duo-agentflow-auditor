#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

TRUSTED_DOMAINS = {
    "www.w3.org",
    "schemas.xmlsoap.org",
    "registry.npmjs.org",
    "pypi.org",
    "docs.gitlab.com",
    "api.github.com",
    "cdn.jsdelivr.net",
}

SEVERITY_WEIGHTS = {"danger": 50, "warning": 25}
CATEGORY_WEIGHTS = {
    "destructive": 15,
    "credential-exfil": 15,
    "prompt-injection": 10,
    "shell-exec": 10,
    "network": 5,
    "insecure-transport": 5,
    "hardcoded-cred": 10,
}

EXECUTABLE_EXTENSIONS = {".sh", ".py", ".js", ".ts", ".rb", ".go"}
EXCLUDED_PATH_SEGMENTS = {"vendor", "node_modules", "__pycache__", ".git"}
TEXT_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".rb",
    ".go",
    ".sh",
    ".yml",
    ".yaml",
    ".json",
    ".md",
    ".txt",
    ".toml",
    ".ini",
    ".cfg",
    ".env",
    ".sql",
}


def eprint(message):
    sys.stderr.write(message + "\n")


def load_json_file(path, default_value):
    target = Path(path)
    if not target.exists():
        eprint(f"warning: JSON file not found: {target}")
        return default_value
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed JSON in {target}: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"failed to read {target}: {exc}") from exc


def load_rules(path, severity):
    content = load_json_file(path, [])
    if not isinstance(content, list):
        raise ValueError(f"rules file must be a JSON array: {path}")
    rules = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if "regex" not in item or "pattern" not in item or "category" not in item:
            continue
        rule = dict(item)
        rule["severity"] = severity
        rules.append(rule)
    return rules


def run_git_command(args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def should_skip_path(path_obj):
    return any(part in EXCLUDED_PATH_SEGMENTS for part in path_obj.parts)


def get_changed_files():
    files = set()
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"],
    ]
    for cmd in commands:
        for candidate in run_git_command(cmd):
            path_obj = Path(candidate)
            if (
                not path_obj.exists()
                or not path_obj.is_file()
                or should_skip_path(path_obj)
            ):
                continue
            if path_obj.suffix in TEXT_FILE_EXTENSIONS or path_obj.name in {
                "Makefile",
                "Dockerfile",
                ".gitlab-ci.yml",
            }:
                files.add(str(path_obj))
    return sorted(files)


def normalize_severity(value):
    token = str(value or "").strip().lower()
    if token in {"high", "error", "critical", "danger"}:
        return "danger"
    if token in {"medium", "warning", "warn", "low", "info"}:
        return "warning"
    return "warning"


def normalize_category(raw):
    text = str(raw or "").lower()
    if "destructive" in text:
        return "destructive"
    if "credential-exfil" in text or "exfil" in text:
        return "credential-exfil"
    if "prompt" in text and "inject" in text:
        return "prompt-injection"
    if "shell" in text or "exec" in text or "subprocess" in text:
        return "shell-exec"
    if "insecure-transport" in text or "http" in text or "tls" in text:
        return "insecure-transport"
    if "hardcoded" in text or "secret" in text or "password" in text or "token" in text:
        return "hardcoded-cred"
    if "network" in text or "request" in text or "socket" in text or "url" in text:
        return "network"
    return "network"


def is_executable_context(file_path):
    path_obj = Path(file_path)
    if path_obj.suffix in EXECUTABLE_EXTENSIONS:
        return True
    return path_obj.name in {"Makefile", "Dockerfile", ".gitlab-ci.yml"}


def contains_untrusted_domain(snippet):
    domains = re.findall(r"https?://([A-Za-z0-9.-]+)", snippet or "")
    if not domains:
        return True
    for domain in domains:
        if any(
            domain == trusted or domain.endswith("." + trusted)
            for trusted in TRUSTED_DOMAINS
        ):
            continue
        return True
    return False


def compute_risk_score(severity, category, file_path, snippet):
    score = SEVERITY_WEIGHTS.get(severity, 25)
    score += CATEGORY_WEIGHTS.get(category, 0)
    executable = is_executable_context(file_path)
    if executable:
        score += 20
    if executable and contains_untrusted_domain(snippet):
        score += 15
    return score


def build_finding(
    file_path, line, severity, category, pattern, snippet, source, risk_modifier=0
):
    score = compute_risk_score(severity, category, file_path, snippet) + int(
        risk_modifier or 0
    )
    return {
        "file": file_path,
        "line": int(line or 1),
        "severity": severity,
        "category": category,
        "pattern": pattern,
        "snippet": (snippet or "").strip(),
        "risk_score": max(score, 0),
        "source": source,
    }


def parse_bandit(bandit_json):
    findings = []
    for item in bandit_json.get("results", []):
        file_path = item.get("filename", "")
        message = item.get("issue_text", "")
        test_name = item.get("test_name", "")
        findings.append(
            build_finding(
                file_path=file_path,
                line=item.get("line_number", 1),
                severity=normalize_severity(item.get("issue_severity", "warning")),
                category=normalize_category(f"{test_name} {message}"),
                pattern=item.get("test_id", test_name) or "bandit-rule",
                snippet=message,
                source="bandit",
            )
        )
    return findings


def parse_semgrep(semgrep_json):
    findings = []
    for item in semgrep_json.get("results", []):
        extra = item.get("extra", {}) or {}
        start = item.get("start", {}) or {}
        snippet = extra.get("lines") or extra.get("message", "")
        findings.append(
            build_finding(
                file_path=item.get("path", ""),
                line=start.get("line", 1),
                severity=normalize_severity(extra.get("severity", "warning")),
                category=normalize_category(
                    f"{item.get('check_id', '')} {extra.get('message', '')}"
                ),
                pattern=item.get("check_id", "semgrep-rule"),
                snippet=snippet,
                source="semgrep",
            )
        )
    return findings


def scan_custom_rules(changed_files, rules):
    findings = []
    for file_path in changed_files:
        path_obj = Path(file_path)
        try:
            content = path_obj.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for rule in rules:
            try:
                regex = re.compile(rule.get("regex", ""), re.MULTILINE)
            except re.error:
                continue
            for match in regex.finditer(content):
                line_no = content.count("\n", 0, match.start()) + 1
                matched_line = (
                    content.splitlines()[line_no - 1] if content.splitlines() else ""
                )
                findings.append(
                    build_finding(
                        file_path=file_path,
                        line=line_no,
                        severity=normalize_severity(rule.get("severity", "warning")),
                        category=normalize_category(rule.get("category", "network")),
                        pattern=rule.get("pattern", "custom-rule"),
                        snippet=matched_line,
                        source="custom-rule",
                        risk_modifier=rule.get("risk_modifier", 0),
                    )
                )
    return findings


def deduplicate_findings(findings):
    deduped = {}
    for finding in findings:
        key = (
            finding["file"],
            finding["line"],
            finding["severity"],
            finding["category"],
            finding["pattern"],
            finding["snippet"][:160],
        )
        existing = deduped.get(key)
        if not existing or finding["risk_score"] > existing["risk_score"]:
            deduped[key] = finding
    return sorted(deduped.values(), key=lambda item: item["risk_score"], reverse=True)


def compute_metrics_and_grade(findings, scanned_files):
    max_risk = max((item["risk_score"] for item in findings), default=0)
    high_risk_count = sum(1 for item in findings if item["risk_score"] >= 70)
    if max_risk >= 90 or high_risk_count >= 3:
        grade = "DANGER"
    elif max_risk >= 70 or high_risk_count >= 1:
        grade = "WARNING"
    else:
        grade = "SAFE"

    severity_counts = {"danger": 0, "warning": 0}
    category_counts = {}
    source_counts = {}
    for finding in findings:
        severity_counts[finding["severity"]] = (
            severity_counts.get(finding["severity"], 0) + 1
        )
        category_counts[finding["category"]] = (
            category_counts.get(finding["category"], 0) + 1
        )
        source_counts[finding["source"]] = source_counts.get(finding["source"], 0) + 1

    metrics = {
        "total_findings": len(findings),
        "max_risk_score": max_risk,
        "high_risk_count": high_risk_count,
        "severity_counts": severity_counts,
        "category_counts": category_counts,
        "source_counts": source_counts,
        "scanned_file_count": len(scanned_files),
    }
    return metrics, grade


def main(argv):
    if len(argv) != 3:
        eprint("usage: merge_sast_results.py <bandit_json_path> <semgrep_json_path>")
        return 2

    try:
        bandit_json = load_json_file(argv[1], {"results": []})
        semgrep_json = load_json_file(argv[2], {"results": []})
        danger_rules = load_rules("rules/danger_rules.json", "danger")
        warning_rules = load_rules("rules/warning_rules.json", "warning")
    except ValueError as exc:
        eprint(f"error: {exc}")
        return 2

    changed_files = get_changed_files()
    findings = []
    findings.extend(
        parse_bandit(bandit_json if isinstance(bandit_json, dict) else {"results": []})
    )
    findings.extend(
        parse_semgrep(
            semgrep_json if isinstance(semgrep_json, dict) else {"results": []}
        )
    )
    findings.extend(scan_custom_rules(changed_files, danger_rules + warning_rules))
    findings = deduplicate_findings(findings)

    risk_metrics, grade = compute_metrics_and_grade(findings, changed_files)
    output = {
        "findings": findings,
        "risk_metrics": risk_metrics,
        "grade": grade,
        "scanned_files": changed_files,
        "sources": ["bandit", "semgrep", "custom-rules"],
    }
    sys.stdout.write(json.dumps(output, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
