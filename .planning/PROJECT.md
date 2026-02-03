# ConfigLoader

## What This Is

A Python configuration loading library that provides zero-friction integration for any project. Load configuration from multiple file formats (TOML, YAML, JSON), merge with environment variables and CLI arguments using a predictable priority (CLI > Env > File), and optionally validate against a Pydantic model.

## Core Value

Zero-friction integration — adding ConfigLoader to a project takes minimal effort and works immediately with sensible defaults.

## Requirements

### Validated

<!-- Shipped and confirmed working. -->

- [x] Multi-source config loading (File, Env, CLI) — existing
- [x] TOML, YAML, JSON parser support — existing
- [x] Optional Pydantic model validation — existing
- [x] Extensible source architecture (ABC-based) — existing
- [x] Lazy loading with singleton caching — existing
- [x] Dict.update() merge semantics (later overrides earlier) — existing

### Active

<!-- Current scope. Building toward these. -->

- [ ] Proper error handling (parsers raise errors, not silent `{}`)
- [ ] Type system compliance (mypy strict, py.typed marker)
- [ ] Modern project configuration (PEP 621, pre-commit)
- [ ] Nested environment variable support (`APP_DB__HOST`)
- [ ] Type coercion for env vars (string → bool/int/list)
- [ ] `reload()` method for long-running applications
- [ ] Clear error messages with guidance
- [ ] Structure hints validation (warn about unexpected keys, typo suggestions)
- [ ] Integration tests covering full pipeline
- [ ] PyPI publish verification

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Remote config sources (Vault, AWS Parameter Store, Consul) — adds complexity and dependencies; can be custom source
- GUI/Web interface — library only, not a configuration editor
- Feature flags system — over-engineering for a config loader; users can implement if needed
- CLI validation commands — deferred to future version; focus on library API for v1
- Hot reloading (automatic refresh) — `reload()` is manual; automatic watching adds complexity

## Context

**Existing codebase:** ConfigLoader is a working library with 16 Python files, ~1000 LOC. Core functionality exists but has bugs (silent parser failures, type issues) that prevent reliable use.

**Known issues from analysis:**
- Parsers silently return `{}` on parse errors (critical)
- Type signatures inconsistent (`str` vs `Path`)
- 2 failing tests due to missing fixtures
- pyproject.toml uses deprecated Poetry format (11 warnings)
- Missing `py.typed` marker and type stubs

**Research needed:**
- Best API pattern for "zero-friction" (one-liner vs explicit)
- How to control nested env vars / type coercion (always-on vs parameter)

## Constraints

- **Python version**: 3.11+ — use modern features, no legacy support
- **Dependencies**: Minimal — core deps (pyyaml, toml, pydantic) only; no heavy frameworks
- **Distribution**: PyPI publishable — must pass TestPyPI verification
- **Types**: Strict mypy compliance — library consumers expect type hints
- **Priority order**: CLI > Env > File — standard hierarchy, not configurable

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Skip feature flags (Phase 4) | Adds complexity without clear benefit for config loader | — Pending |
| Defer CLI commands (Phase 6) | Focus on library API for v1; CLI adds optional deps | — Pending |
| Add validation hints phase | User wants structure validation beyond syntax | — Pending |
| Research API pattern before implementing | Need to determine best UX for "zero-friction" goal | — Pending |

---
*Last updated: 2026-02-03 after initialization*
