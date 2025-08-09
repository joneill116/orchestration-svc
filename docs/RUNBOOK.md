# Runbook

## Service Overview
- Minimal orchestration service core.
- All business logic and integrations are externalized.

## Common Operations
- **Start service:** `make run`
- **Run tests:** `make test`
- **Check security:** `make pip-audit`
- **Generate SBOM:** `make sbom`

## Troubleshooting
- **Type errors:** Run `make typecheck` and fix all reported issues.
- **Lint errors:** Run `make lint` and `make format`.
- **Test failures:** Run `make test` and review coverage.
- **Dependency issues:** Run `poetry install` and `make pip-audit`.

## Escalation
- For production issues, see [SECURITY.md](./SECURITY.md).
- For CI failures, see GitHub Actions logs.
