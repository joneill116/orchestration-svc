# Contributing Guide

Thank you for considering a contribution!

## PR Checklist
- [ ] All code is type-annotated and passes strict mypy
- [ ] All code is linted (ruff, flake8) and auto-formatted (ruff format)
- [ ] All tests pass and coverage is 100%
- [ ] No security vulnerabilities (pip-audit)
- [ ] SBOM is up to date (make sbom)
- [ ] Pre-commit hooks are installed and passing
- [ ] Documentation is updated (README, docs/)

## How to Contribute
1. Fork the repo and create a feature branch.
2. Run `make pre-commit-install` and `make check`.
3. Open a pull request and fill out the PR template.
4. Engage in code review and address feedback.

## Code Style
- Use type annotations everywhere.
- Keep code DRY and modular.
- Write intention-revealing tests.

## Reporting Issues
- Use GitHub Issues for bugs, feature requests, and questions.
- For security issues, see [SECURITY.md](./SECURITY.md).
