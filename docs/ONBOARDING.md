# Onboarding Guide

Welcome to orchestration-svc! This guide will help you get started as a contributor or maintainer.

## 1. Clone the Repo
```sh
git clone https://github.com/joneill116/orchestration-svc.git
cd orchestration-svc
```

## 2. Install Dependencies
```sh
poetry install
```

## 3. Pre-commit Hooks
```sh
make pre-commit-install
```

## 4. Run Checks
```sh
make check
```

## 5. Run the Service
```sh
make run
```

## 6. Run Tests
```sh
make test
```

## 7. Review the Docs
- [README.md](../README.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [SECURITY.md](./SECURITY.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)

## 8. Open a Pull Request
- Ensure all checks pass before opening a PR.
- Follow the PR checklist in CONTRIBUTING.md.
