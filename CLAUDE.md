# CLAUDE.md — Agency

This file provides context for AI assistants (Claude Code and others) working in this repository. Update it as the project evolves.

---

## Repository Status

This is a **newly initialized repository** with no committed code yet. The sections below establish conventions to follow as the project is built out. Update each section when the corresponding code is added.

---

## Project Overview

**Name:** Agency
**Purpose:** _TODO: Describe what this project does._
**Primary language(s):** _TODO: Fill in once established._
**Status:** Pre-development / initial setup

---

## Directory Structure

_Update this section once files exist._

```
Agency/
├── CLAUDE.md          # This file
├── README.md          # Project overview for humans
└── ...                # Add structure as it develops
```

---

## Development Setup

### Prerequisites

_List required tools, runtimes, and versions here as they are determined._

```bash
# Example placeholders — update with real commands
# node >= 20, python >= 3.11, go >= 1.22, etc.
```

### Initial Setup

```bash
# Clone and enter the repo
git clone <repo-url>
cd Agency

# Install dependencies (update with real commands)
# npm install   (Node/JS)
# pip install -r requirements.txt   (Python)
# go mod tidy   (Go)
# cargo build   (Rust)
```

### Environment Variables

Copy `.env.example` to `.env` and fill in values before running anything.

```bash
cp .env.example .env
```

_Document required env vars here as they are added._

---

## Running the Project

```bash
# Development server (update with real commands)
# npm run dev
# python -m uvicorn app.main:app --reload
# go run ./cmd/server
```

---

## Testing

```bash
# Run all tests (update with real commands)
# npm test
# pytest
# go test ./...
# cargo test
```

- Write tests for all new functionality.
- Tests live alongside source files or in a dedicated `tests/` directory — pick one and be consistent.
- Aim for meaningful coverage; avoid testing implementation details.

---

## Code Style & Conventions

### General

- Prefer clarity over cleverness.
- Keep functions small and focused on a single responsibility.
- Avoid premature abstraction — solve the current problem first.
- No commented-out code in commits; use git history instead.

### Naming

- Variables, functions, files: use the idiomatic casing for the language (camelCase for JS/TS, snake_case for Python/Rust/Go).
- Be descriptive: `fetchUserById` over `getUser`; `is_active` over `flag`.

### Error Handling

- Never silently swallow errors.
- Return/throw meaningful error messages with context.
- Validate at system boundaries (user input, external APIs); trust internal contracts.

### Comments

- Comment the **why**, not the **what**.
- Self-documenting code is preferred over excessive inline comments.

---

## Git Workflow

### Branches

- `main` — production-ready code; protected.
- Feature branches: `feature/<short-description>`
- Bug fixes: `fix/<short-description>`
- Claude Code branches: `claude/<task-id>` (auto-created by Claude Code sessions)

### Commits

- Use the **imperative mood** in commit messages: `Add user authentication`, not `Added` or `Adding`.
- Keep the subject line under 72 characters.
- Reference issue numbers when applicable: `Fix login redirect (#42)`.

### Pull Requests

- Each PR should address a single concern.
- Include a summary of what changed and why.
- Ensure tests pass and linting is clean before requesting review.

### Never

- Force-push to `main`.
- Commit secrets, credentials, or `.env` files.
- Skip pre-commit hooks with `--no-verify` without a documented reason.

---

## AI Assistant Guidelines (Claude Code)

### What to do

- Read existing code before modifying it.
- Match the style and patterns already in the codebase.
- Make the minimum change necessary to accomplish the task.
- Run tests after changes when a test command is available.
- Commit changes with clear messages and push to the designated branch.

### What to avoid

- Do not create unnecessary files or abstractions.
- Do not refactor code that wasn't part of the requested task.
- Do not add docstrings, comments, or type annotations to code that wasn't changed.
- Do not add error handling for scenarios that cannot occur.
- Do not use `--no-verify` or skip safety checks.
- Do not push to `main` directly.

### Branch policy

All Claude Code sessions must develop on and push to their designated `claude/` branch. Never push to `main` or another user's branch without explicit instruction.

---

## Security

- Never commit secrets, API keys, tokens, or passwords.
- Use environment variables for all sensitive configuration.
- Validate and sanitize all external input.
- Keep dependencies up to date; address known CVEs promptly.

---

## Updating This File

Update `CLAUDE.md` whenever:
- A new tool, framework, or language is added to the project.
- Development setup steps change.
- New conventions are adopted.
- Significant architectural decisions are made.

Keep it accurate — an outdated CLAUDE.md is worse than none.
