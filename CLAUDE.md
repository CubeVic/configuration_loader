# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ConfigLoader is a Python library that provides flexible configuration loading from multiple sources (files, environment variables, CLI arguments) with support for TOML, YAML, and JSON formats. It uses an extensible architecture with optional Pydantic validation.

## Development Commands

### Setup
```bash
# Install dependencies using Poetry
poetry install

# Install with dev dependencies
poetry install --with dev
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=configloader

# Run a specific test file
pytest tests/test_unit_core.py

# Run a specific test
pytest tests/test_unit_core.py::test_function_name
```

### Code Quality
```bash
# Format code with black
black configloader tests

# Sort imports with isort
isort configloader tests

# Lint with ruff
ruff check configloader tests

# Type check with mypy
mypy configloader

# Run all linting and formatting
black configloader tests && isort configloader tests && ruff check configloader tests && mypy configloader
```

### Documentation
```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Architecture

### Core Components

**ConfigLoader** (`configloader/core.py`)
- Main orchestrator class that coordinates configuration loading
- Implements singleton pattern for config caching (`_config` attribute)
- Merges configs from multiple sources with update() priority (later sources override earlier)
- Optional Pydantic validation via `config_model` parameter

**Configuration Sources** (`configloader/sources.py`)
- All sources implement `ConfigSource` ABC with `load()` method
- Loading order (each overwrites previous): File → Environment → CLI → Custom sources
- `FileConfigSource`: Loads from TOML/YAML/JSON files using appropriate parser
- `EnvConfigSource`: Reads env vars with optional prefix (e.g., `MYAPP_` → `myapp`)
- `CLIConfigSource`: Converts argparse.Namespace to dict
- Custom sources can be added via `custom_sources` parameter

**Parsers** (`configloader/parsers/`)
- `BaseParser` ABC defines `load(file_path)` interface
- Format-specific parsers: `TOMLParser`, `YAMLParser`, `JSONParser`
- Parser selected automatically based on file extension in `ConfigLoader._get_parser()`

### Key Design Patterns

1. **Source Priority**: Configuration merging follows dict.update() semantics - sources loaded later override earlier values
2. **Lazy Loading**: Config loaded only when `load_config()` first called, then cached
3. **Optional Validation**: Pydantic validation only runs if `config_model` provided
4. **Extensibility**: Custom sources can be injected to support databases, remote APIs, etc.

> For detailed design decisions and architecture rationale, see [docs/DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md)

## Code Style

- Python 3.11+ required
- Line length: 88 characters (Black default)
- Type hints required for all function arguments and return values (enforced by mypy with `disallow_untyped_defs`)
- Google-style docstrings
- Follow PEP 8

## Important Notes

- When adding new parsers, implement `BaseParser` and register in `configloader/__init__.py`
- Custom sources must implement `ConfigSource.load()` returning `Dict[str, Any]`
- Validation is intentionally optional - library works without Pydantic models
- Config file path resolution: if `config_file_path=None`, defaults to `<repo_root>/<config_file_name>`

---

## Known Issues

### Critical (Must Fix)

| ID | Issue | Location | Impact |
|----|-------|----------|--------|
| 1.1 | Parsers silently return `{}` on parse errors instead of raising | `parsers/*.py` | Silent failures mask config problems |
| 1.2 | Parser type signatures use `str` instead of `Path` | `parsers/*.py` | mypy errors, inconsistent API |
| 1.3 | `_get_file()` path handling bug | `core.py:89` | Treats path as directory when it's a file |
| 1.4 | `ConfigValidationError.errors` type hint incorrect | `exceptions.py:11` | mypy error |
| 1.5 | 2 failing tests due to missing config fixtures | `tests/` | CI failures |

### Type System

| ID | Issue | Location | Impact |
|----|-------|----------|--------|
| 2.1 | Missing type stubs for PyYAML, toml | `pyproject.toml` | mypy errors |
| 2.2 | No `py.typed` marker file | `configloader/` | Library not typed for consumers |
| 2.3 | Parser parameter typed as `Any` | `sources.py:31` | Loses type safety |

### Project Configuration

| ID | Issue | Location | Impact |
|----|-------|----------|--------|
| 3.1 | pyproject.toml uses deprecated Poetry format | `pyproject.toml` | 11 deprecation warnings |
| 3.2 | No pre-commit hooks configured | Root | Manual quality checks |
| 3.3 | Junk files in root | `main.py`, `config.yaml` | Cluttered repository |

### Missing Features

| ID | Issue | Impact |
|----|-------|--------|
| 4.1 | No nested env var support (`APP_DB__HOST`) | Can't fully configure via env |
| 4.2 | No `reload()` method | Can't refresh config in long-running apps |
| 4.3 | CLI module incomplete | No validation commands |

---

## Roadmap Summary

Development is organized into 7 phases. Each phase can be worked on independently.

| Phase | Focus | Priority | Status |
|-------|-------|----------|--------|
| **1** | Fix Critical Bugs | CRITICAL | Not started |
| **2** | Type System Compliance | HIGH | Not started |
| **3** | Modernize Project Config | MEDIUM | Not started |
| **4** | Feature Flags System | MEDIUM | Not started |
| **5** | Core Enhancements | MEDIUM | Not started |
| **6** | CLI Implementation | LOW | Not started |
| **7** | Publish Readiness | LOW | Not started |

**Full roadmap with task-level details:** [.planning/ROADMAP.md](.planning/ROADMAP.md)

### Verification After Any Phase

```bash
# All phases should maintain these invariants
poetry run pytest                    # All tests pass
poetry run mypy configloader         # 0 errors (after Phase 2)
poetry check                         # No deprecation warnings (after Phase 3)
```
