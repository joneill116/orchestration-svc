# Orchestration Service Runbook

## Overview
This runbook covers basic operations, troubleshooting, and escalation for orchestration-svc.

## Health & Monitoring
- Service exposes only orchestration APIs; health endpoints are managed by a separate health-service.
- Check logs for correlation IDs to trace requests end-to-end.

## Common Operations
- **Deploy:** Use CI/CD pipeline; builds are immutable and reproducible.
- **Logs:** All logs are structured and machine-parsable.
- **Scaling:** Service is stateless and autoscaling-ready.

## Troubleshooting
- Check logs for errors and correlation IDs.
- Ensure all dependencies (adapters, domain, health-service) are reachable.

## Escalation
- Primary: @joneill116
- See CODEOWNERS for on-call rotation.

---

> Keep this runbook up to date as the service evolves.
