# Contributing to Duo AgentFlow Auditor

Thank you for your interest in contributing! This project is built for the **GitLab AI Hackathon 2026** and uses the GitLab Duo Agent Platform.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. Create a **feature branch** from `main`
4. Make your changes
5. **Push** and open a Pull Request (GitHub) or Merge Request (GitLab)

---

## What You Can Contribute

### Detection Rules

Add new patterns to `rules/danger_rules.json` or `rules/warning_rules.json`:

```json
{
  "category": "category-name",
  "pattern_name": "human-readable-name",
  "regex": "your-regex-pattern",
  "risk_modifier": 0
}
```

**Requirements:**
- Prefer low false positives over broad catches
- Include at least one positive and one negative test case in `examples/`
- Document the pattern with an example match

### Agent System Prompts

Improvements to agent prompts in `agents/*.md`:
- Better output formatting
- Fewer false positives/negatives
- Clearer fix suggestions
- More accurate risk scoring

### Documentation

- Fix typos or unclear instructions
- Add setup tips for specific environments
- Improve example files

---

## Rules

### Do

- Follow existing code style and markdown formatting
- Test your changes against the example files (`examples/vulnerable-mr/` and `examples/safe-mr/`)
- Keep the project **stdlib-only** (no external dependencies for Python scripts)
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages

### Don't

- Add external dependencies
- Modify existing test fixtures (add new ones instead)
- Change the Flow YAML schema version without discussion
- Touch the `hackathon/` or `references/` directories (historical artifacts)

---

## Commit Message Format

```
type(scope): description

Examples:
feat(rules): add SQL injection detection pattern
fix(reporter): correct risk heatmap bar calculation
docs(setup): add troubleshooting for tool permissions
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

---

## PR / MR Checklist

Before submitting:

- [ ] Changes work against example files
- [ ] New detection rules include test cases
- [ ] Documentation updated if behavior changed
- [ ] Commit messages follow conventional format
- [ ] No external dependencies added

---

## Questions?

Open an issue or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
