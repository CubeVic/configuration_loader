# Roadmap: ConfigLoader

## Overview

ConfigLoader evolves from a working-but-buggy configuration library to a production-ready, typed, publishable package. The journey starts with critical bug fixes (silent parser failures), builds type safety, modernizes project tooling, adds power-user features (nested env vars, reload), and culminates in PyPI publication.

## Domain Expertise

None

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Fix Critical Bugs** — Eliminate silent failures and fix type inconsistencies
- [ ] **Phase 2: Type System Compliance** — Achieve zero mypy errors with strict mode
- [ ] **Phase 3: Modernize Project Config** — PEP 621 migration, pre-commit hooks, cleanup
- [ ] **Phase 4: Feature Flags System** — Enable safe experimentation with new features
- [ ] **Phase 5: Core Enhancements** — Nested env vars, reload(), type coercion
- [ ] **Phase 6: CLI Implementation** — Validate and check commands with typer/rich
- [ ] **Phase 7: Publish Readiness** — Integration tests, CI verification, TestPyPI

## Phase Details

### Phase 1: Fix Critical Bugs
**Goal**: Parsers raise errors instead of silent `{}`, type signatures consistent, all tests pass
**Depends on**: Nothing (first phase)
**Research**: Unlikely (internal code investigation, established patterns)
**Plans**: 3 plans

Plans:
- [x] 01-01: Fix parser silent failures (JSON, YAML, TOML raise ConfigParserError)
- [ ] 01-02: Fix type signatures (Path instead of str, Dict[str, Any] return types)
- [ ] 01-03: Fix path handling and tests (_get_file() bug, missing fixtures, type hints)

### Phase 2: Type System Compliance
**Goal**: Library passes mypy --strict, consumers get type hints
**Depends on**: Phase 1
**Research**: Unlikely (standard typing patterns)
**Plans**: 2 plans

Plans:
- [ ] 02-01: Add type infrastructure (type stubs, py.typed marker)
- [ ] 02-02: Fix source types and verify (BaseParser type in sources, zero mypy errors)

### Phase 3: Modernize Project Config
**Goal**: No deprecation warnings, automated quality checks, clean repository
**Depends on**: None (can run parallel to Phase 2)
**Research**: Likely (PEP 621 migration)
**Research topics**: Poetry PEP 621 format, current pre-commit hook versions
**Plans**: 2 plans

Plans:
- [ ] 03-01: Migrate pyproject.toml to PEP 621
- [ ] 03-02: Add pre-commit hooks and clean up repository

### Phase 4: Feature Flags System
**Goal**: Infrastructure for safe feature experimentation via env vars
**Depends on**: Phase 1
**Research**: Unlikely (simple dataclass pattern)
**Plans**: 2 plans

Plans:
- [ ] 04-01: Implement FeatureFlag class and container
- [ ] 04-02: Add exports and comprehensive tests

### Phase 5: Core Enhancements
**Goal**: Nested env vars, config reload, type coercion, clear error messages
**Depends on**: Phase 1, Phase 4
**Research**: Unlikely (internal patterns, straightforward implementations)
**Plans**: 2 plans

Plans:
- [ ] 05-01: Add env var features (nested keys with __, type coercion)
- [ ] 05-02: Add reload() method and improve error messages

### Phase 6: CLI Implementation
**Goal**: Working configloader validate and check commands
**Depends on**: Phase 1, Phase 2
**Research**: Likely (typer CLI patterns)
**Research topics**: Typer command patterns, rich console output formatting
**Plans**: 2 plans

Plans:
- [ ] 06-01: Add CLI dependencies and implement validate command
- [ ] 06-02: Implement check command with format options

### Phase 7: Publish Readiness
**Goal**: Library verified end-to-end, CI green, TestPyPI successful
**Depends on**: Phases 1-6
**Research**: Likely (TestPyPI workflow)
**Research topics**: TestPyPI publishing with Poetry, CI workflow verification
**Plans**: 2 plans

Plans:
- [ ] 07-01: Create integration tests and verify CI pipeline
- [ ] 07-02: TestPyPI dry run and verification

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7
(Phase 3 can run parallel to Phase 2)

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Fix Critical Bugs | 1/3 | In progress | - |
| 2. Type System Compliance | 0/2 | Not started | - |
| 3. Modernize Project Config | 0/2 | Not started | - |
| 4. Feature Flags System | 0/2 | Not started | - |
| 5. Core Enhancements | 0/2 | Not started | - |
| 6. CLI Implementation | 0/2 | Not started | - |
| 7. Publish Readiness | 0/2 | Not started | - |

---

## Reference: Issue Mapping

For detailed acceptance criteria, see the original issue breakdown preserved below.

<details>
<summary>Phase 1 Issues (7 issues → 3 plans)</summary>

**Plan 01-01: Parser Silent Failures**
- Issue 1.1: Fix JSON parser (json_parser.py)
- Issue 1.2: Fix YAML parser (yaml_parser.py)
- Issue 1.3: Fix TOML parser (toml_parser.py)

**Plan 01-02: Type Signatures**
- Issue 1.4: Fix parser type signatures (str → Path, dict → Dict[str, Any])

**Plan 01-03: Path Handling and Tests**
- Issue 1.5: Fix _get_file() path handling
- Issue 1.6: Fix ConfigValidationError.errors type hint
- Issue 1.7: Fix failing tests (fixtures)

</details>

<details>
<summary>Phase 2 Issues (4 issues → 2 plans)</summary>

**Plan 02-01: Type Infrastructure**
- Issue 2.1: Add type stub dependencies (types-PyYAML, types-toml)
- Issue 2.2: Create py.typed marker

**Plan 02-02: Source Types and Verification**
- Issue 2.3: Fix parser parameter type in sources (Any → BaseParser)
- Issue 2.4: Verify zero mypy errors

</details>

<details>
<summary>Phase 3 Issues (4 issues → 2 plans)</summary>

**Plan 03-01: PEP 621 Migration**
- Issue 3.1: Migrate pyproject.toml to PEP 621

**Plan 03-02: Pre-commit and Cleanup**
- Issue 3.2: Add pre-commit hooks
- Issue 3.3: Complete truncated README example
- Issue 3.4: Clean up root directory

</details>

<details>
<summary>Phase 4 Issues (4 issues → 2 plans)</summary>

**Plan 04-01: Implementation**
- Issue 4.1: Create FeatureFlag class
- Issue 4.2: Create FeatureFlags container

**Plan 04-02: Exports and Tests**
- Issue 4.3: Export FeatureFlags from package
- Issue 4.4: Add feature flag tests

</details>

<details>
<summary>Phase 5 Issues (4 issues → 2 plans)</summary>

**Plan 05-01: Env Var Features**
- Issue 5.1: Add nested environment variable support
- Issue 5.3: Add type coercion for environment variables

**Plan 05-02: Reload and Errors**
- Issue 5.2: Add reload() method
- Issue 5.4: Improve error messages

</details>

<details>
<summary>Phase 6 Issues (3 issues → 2 plans)</summary>

**Plan 06-01: Dependencies and Validate**
- Issue 6.1: Add CLI dependencies (typer, rich)
- Issue 6.2: Implement validate command

**Plan 06-02: Check Command**
- Issue 6.3: Implement check command

</details>

<details>
<summary>Phase 7 Issues (3 issues → 2 plans)</summary>

**Plan 07-01: Integration and CI**
- Issue 7.1: Create integration tests
- Issue 7.2: Verify CI pipeline

**Plan 07-02: TestPyPI**
- Issue 7.3: TestPyPI dry run

</details>

---

**Last Updated:** 2026-02-03
