# Contributing to ML-POWERED-BUG-TRIAGE-SYSTEM

Thanks for your interest in contributing! This document explains how to report issues, propose changes, and submit code so we can keep the project healthy, readable, and easy to maintain.

---

## Table of contents

* [Code of Conduct](#code-of-conduct)
* [Ways to contribute](#ways-to-contribute)
* [Getting started (local dev environment)](#getting-started-local-dev-environment)
* [Branching & commit conventions](#branching--commit-conventions)
* [Running tests & linting](#running-tests--linting)
* [Working with data and models](#working-with-data-and-models)
* [Submitting a pull request (PR)](#submitting-a-pull-request-pr)
* [Issue templates and labels](#issue-templates-and-labels)
* [Review process & checklist](#review-process--checklist)
* [Acknowledgements & contacting maintainers](#acknowledgements--contacting-maintainers)

---

## Code of Conduct

Please read and follow our [CODE\_OF\_CONDUCT.md](./CODE_OF_CONDUCT.md) (if present). We want contributors to feel welcome — be respectful, constructive, and professional.

If a code of conduct file does not yet exist, treat the repository as a friendly open-source project: be inclusive, patient, and communicative.

---

## Ways to contribute

1. **File issues** — report bugs, unexpected behaviour, or propose features. Include steps to reproduce, expected vs actual behaviour, logs, screenshots, and environment details (OS, Python version, package versions).
2. **Fix bugs or add features** — work on code, tests, docs, or examples.
3. **Improve documentation** — README, tutorials, API docs, and inline code comments.
4. **Improve model evaluation / experiments** — add baselines, benchmarks, or clearer evaluation scripts.
5. **Suggest improvements to CI, packaging, or developer tooling**.

---

## Getting started (local dev environment)

> The instructions below are generic; adapt them if the repository has its own `README` or `CONTRIBUTING` section with different commands.

1. Fork the repo and clone your fork:

```bash
# replace <your-username>
git clone https://github.com/<your-username>/ML-POWERED-BUG-TRIAGE-SYSTEM.git
cd ML-POWERED-BUG-TRIAGE-SYSTEM
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Mac / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies (if `requirements.txt` or `pyproject.toml` exists):

```bash
pip install -r requirements.txt
# or
pip install -e .
```

4. Set up environment variables (if needed).

* If the project requires API keys, datasets, or credentials, **do not** check them into source control. Add a `.env.example` with the variables names and expected format.

5. Run a quick smoke test to ensure everything loads:

```bash
# typical examples; check repository for actual entry points
python -m src.main --help
```

---

## Branching & commit conventions

* Use descriptive branch names: `fix/<short-desc>`, `feat/<short-desc>`, `chore/<short-desc>`.
* Keep PRs focused and small — one logical change per PR.

**Commit message style** (recommended):

```
[type](scope): short summary

longer description (optional)

issue: #<issue-number>
```

Where `type` is one of: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, `perf`.

---

## Running tests & linting

If the repo includes tests, run them locally before opening a PR.

```bash
# run unit tests (example)
pytest

# run linter (example)
flake8
# or
pylint src
```

If the repository uses `pre-commit`, install and run hooks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Add or update tests for any bug fixes or new features.

---

## Working with data and models

* **Do not** commit large datasets, model checkpoints, or secrets to the repository. Use `.gitignore` to exclude them.
* Provide small sample data or scripts to download required datasets automatically (e.g. `scripts/download_sample_data.sh`) and document the process.
* If using external datasets, include proper attribution and licensing in `DATA_LICENSES.md` or the main `README`.
* For reproducibility, include the exact commands used to train/evaluate models and random seeds where possible.

---

## Submitting a pull request (PR)

1. Fork & clone the repository.
2. Create a new branch for your change.
3. Make small, focused commits with clear messages.
4. Run tests & linter locally.
5. Push your branch to your fork.
6. Open a PR to `main` (or the repository's default branch) and include the following in the PR description:

   * What the change does and why.
   * Any dependencies or migration steps.
   * How to test the change locally (commands).
   * Screenshots/logs if applicable.
   * Link to related issues (use `Fixes #<issue-number>` to auto-close issues).

**PR template checklist (suggested)**

* [ ] My code follows the repository style.
* [ ] I added or updated tests as necessary.
* [ ] I updated the documentation when applicable.
* [ ] I ran the unit tests locally and they pass.
* [ ] I ran linting and formatting tools.
* [ ] No large files or secrets are included.

---

## Issue templates and labels

Consider adding these labels (maintainer side): `bug`, `enhancement`, `documentation`, `question`, `good first issue`, `help wanted`.

When filing an issue, include:

* A descriptive title
* Steps to reproduce
* Expected vs actual behaviour
* Environment (OS, Python version, dependencies)
* Any error logs or traceback

---

## Review process & checklist

* Maintainers will review PRs and may request changes.
* Be responsive to review comments and keep conversation constructive.

**Reviewer checklist**

* Does the change make sense and follow project conventions?
* Are tests provided and passing?
* Is documentation updated?
* Are new dependencies necessary and justified?

---

## A note on security and responsible disclosure

If you discover a security vulnerability, please **do not** open a public issue. Contact the maintainers privately (email listed in the repo) and provide enough detail for us to reproduce and fix the issue. We will treat reports confidentially.

---

## Acknowledgements & contacting maintainers

Thanks for considering contributing!

If you need help getting started, leave an issue with the `good first issue` label request or reach out to the maintainers via the repository contact listed in the README.

---

*This CONTRIBUTING.md is a template. If you'd like, I can tailor it to include project-specific commands, test examples, and PR/issue templates and then provide ready-to-add `.github/ISSUE_TEMPLATE` and `.github/PULL_REQUEST_TEMPLATE` files.*
