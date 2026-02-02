# ConfigLoader Roadmap

> Detailed task-level breakdown for ConfigLoader development. Each issue is independently workable with clear acceptance criteria.

---

## Phase 1: Fix Critical Bugs

**Priority:** CRITICAL — Must fix before any feature work
**Dependencies:** None
**Estimated Issues:** 7

### Issue 1.1: Fix JSON Parser Silent Failure

**Files:** `configloader/parsers/json_parser.py:21-22`

**Problem:** Parser catches `JSONDecodeError` and returns empty dict `{}` instead of raising an error. This silently masks configuration problems.

**Current Code:**
```python
except json.JSONDecodeError:
    return {}
```

**Required Change:**
```python
except json.JSONDecodeError as e:
    raise ConfigParserError(f"Failed to parse JSON file {file_path}: {e}")
```

**Acceptance Criteria:**
- [ ] `ConfigParserError` is raised when JSON file has syntax errors
- [ ] Error message includes the file path and parse error details
- [ ] Import `ConfigParserError` from `configloader.exceptions`

**Verification:**
```bash
pytest tests/test_unit_parsers.py -v -k json
```

---

### Issue 1.2: Fix YAML Parser Silent Failure

**Files:** `configloader/parsers/yaml_parser.py:23-24`

**Problem:** Parser catches `YAMLError` and returns empty dict `{}` instead of raising an error.

**Current Code:**
```python
except yaml.YAMLError:
    return {}
```

**Required Change:**
```python
except yaml.YAMLError as e:
    raise ConfigParserError(f"Failed to parse YAML file {file_path}: {e}")
```

**Acceptance Criteria:**
- [ ] `ConfigParserError` is raised when YAML file has syntax errors
- [ ] Error message includes the file path and parse error details
- [ ] Import `ConfigParserError` from `configloader.exceptions`

**Verification:**
```bash
pytest tests/test_unit_parsers.py -v -k yaml
```

---

### Issue 1.3: Fix TOML Parser Silent Failure

**Files:** `configloader/parsers/toml_parser.py:21-22`

**Problem:** Parser catches `TomlDecodeError` and returns empty dict `{}` instead of raising an error.

**Current Code:**
```python
except toml.TomlDecodeError:
    return {}
```

**Required Change:**
```python
except toml.TomlDecodeError as e:
    raise ConfigParserError(f"Failed to parse TOML file {file_path}: {e}")
```

**Acceptance Criteria:**
- [ ] `ConfigParserError` is raised when TOML file has syntax errors
- [ ] Error message includes the file path and parse error details
- [ ] Import `ConfigParserError` from `configloader.exceptions`

**Verification:**
```bash
pytest tests/test_unit_parsers.py -v -k toml
```

---

### Issue 1.4: Fix Parser Type Signatures

**Files:**
- `configloader/parsers/base.py`
- `configloader/parsers/json_parser.py`
- `configloader/parsers/yaml_parser.py`
- `configloader/parsers/toml_parser.py`

**Problem:** Parser `load()` methods accept `str` but should accept `Path` for consistency with the rest of the codebase. Return type is `dict` but should be `Dict[str, Any]`.

**Required Changes:**

In `base.py`:
```python
from pathlib import Path
from typing import Dict, Any

@abstractmethod
def load(self, file_path: Path) -> Dict[str, Any]:
    pass
```

In each parser implementation:
```python
from pathlib import Path
from typing import Dict, Any

def load(self, file_path: Path) -> Dict[str, Any]:
    # Existing implementation works with Path
```

**Acceptance Criteria:**
- [ ] `BaseParser.load()` signature uses `Path` and `Dict[str, Any]`
- [ ] All three parser implementations match the base signature
- [ ] mypy reports no errors for parser module

**Verification:**
```bash
mypy configloader/parsers/
```

---

### Issue 1.5: Fix `_get_file()` Path Handling

**Files:** `configloader/core.py:89`

**Problem:** The `_get_file()` method has a bug where it treats a path as a directory when it's actually a file path. Needs investigation to determine exact fix.

**Investigation Required:**
1. Read `_get_file()` method implementation
2. Understand the expected behavior for both file paths and directory paths
3. Identify the bug and fix accordingly

**Acceptance Criteria:**
- [ ] `_get_file()` correctly handles when `config_file_path` is a full file path
- [ ] `_get_file()` correctly handles when `config_file_path` is a directory
- [ ] Existing tests still pass

**Verification:**
```bash
pytest tests/test_unit_core.py -v
```

---

### Issue 1.6: Fix `ConfigValidationError.errors` Type Hint

**Files:** `configloader/exceptions.py:11`

**Problem:** The `errors` attribute type hint is incorrect or missing, causing mypy errors.

**Investigation Required:**
1. Read current exception implementation
2. Determine appropriate type for `errors` (likely `List[Dict[str, Any]]` or similar)
3. Fix the type hint

**Acceptance Criteria:**
- [ ] `ConfigValidationError.errors` has correct type hint
- [ ] mypy reports no errors for exceptions module

**Verification:**
```bash
mypy configloader/exceptions.py
```

---

### Issue 1.7: Fix Failing Tests

**Files:** `tests/` directory

**Problem:** Two tests are failing: `test_custom_source` and `test_caching_mechanism`. They require proper config file fixtures.

**Investigation Required:**
1. Run failing tests to see exact error
2. Create missing config.toml fixture in tests/
3. Ensure tests use the correct paths

**Acceptance Criteria:**
- [ ] All 9 tests pass
- [ ] Tests are independent (can run in any order)
- [ ] Test fixtures are properly set up

**Verification:**
```bash
pytest tests/ -v
```

---

## Phase 2: Type System Compliance

**Priority:** HIGH — Required for publishable library
**Dependencies:** Phase 1 (Issues 1.4, 1.6)
**Estimated Issues:** 4

### Issue 2.1: Add Type Stub Dependencies

**Files:** `pyproject.toml`

**Problem:** Missing type stubs for PyYAML and toml libraries causes mypy errors.

**Required Change:**
```toml
[tool.poetry.group.dev.dependencies]
types-PyYAML = "^6.0"
types-toml = "^0.10"
```

**Acceptance Criteria:**
- [ ] `types-PyYAML` added to dev dependencies
- [ ] `types-toml` added to dev dependencies
- [ ] `poetry install` succeeds

**Verification:**
```bash
poetry install --with dev && mypy configloader
```

---

### Issue 2.2: Create `py.typed` Marker

**Files:** `configloader/py.typed` (new file)

**Problem:** Library doesn't advertise that it's typed, so consumers won't get type hints.

**Required Change:** Create empty file `configloader/py.typed`

**Acceptance Criteria:**
- [ ] `configloader/py.typed` exists (empty file)
- [ ] File is included in package (check MANIFEST.in if needed)

**Verification:**
```bash
ls configloader/py.typed
```

---

### Issue 2.3: Fix Parser Parameter Type in Sources

**Files:** `configloader/sources.py:31`

**Problem:** Parser parameter is typed as `Any` instead of `BaseParser`.

**Required Change:**
```python
from configloader.parsers.base import BaseParser

def __init__(self, file_path: Path, parser: BaseParser):
    ...
```

**Acceptance Criteria:**
- [ ] `FileConfigSource` parser parameter typed as `BaseParser`
- [ ] Import added for `BaseParser`
- [ ] mypy reports no errors

**Verification:**
```bash
mypy configloader/sources.py
```

---

### Issue 2.4: Verify Zero mypy Errors

**Files:** All in `configloader/`

**Problem:** Cumulative check that all type issues are resolved.

**Acceptance Criteria:**
- [ ] `mypy configloader` reports 0 errors
- [ ] No `# type: ignore` comments added (unless absolutely necessary with justification)

**Verification:**
```bash
mypy configloader --strict
```

---

## Phase 3: Modernize Project Configuration

**Priority:** MEDIUM — Improves maintainability
**Dependencies:** None (can run parallel to Phase 2)
**Estimated Issues:** 4

### Issue 3.1: Migrate pyproject.toml to PEP 621

**Files:** `pyproject.toml`

**Problem:** Currently uses deprecated Poetry-specific format, causing 11 deprecation warnings.

**Required Changes:**
- Move `[tool.poetry]` section to `[project]` section
- Update dependency format to PEP 621 style
- Keep Poetry as build backend but use standard metadata

**Acceptance Criteria:**
- [ ] `poetry check` shows no deprecation warnings
- [ ] `poetry install` still works
- [ ] Package metadata preserved

**Verification:**
```bash
poetry check && poetry install
```

---

### Issue 3.2: Add Pre-commit Hooks

**Files:** `.pre-commit-config.yaml` (new file)

**Problem:** No automated quality checks on commit.

**Required Configuration:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-PyYAML
          - types-toml
        args: [--config-file=pyproject.toml]
```

**Acceptance Criteria:**
- [ ] `.pre-commit-config.yaml` exists with black, isort, ruff, mypy
- [ ] `pre-commit install` succeeds
- [ ] `pre-commit run --all-files` passes

**Verification:**
```bash
pre-commit run --all-files
```

---

### Issue 3.3: Complete Truncated README Example

**Files:** `README.md:170` (approximate line)

**Problem:** JSON example in README is truncated/incomplete.

**Investigation Required:**
1. Find the truncated JSON example
2. Complete the example with proper closing braces

**Acceptance Criteria:**
- [ ] All code examples in README are complete and valid
- [ ] Examples can be copy-pasted and run

**Verification:**
```bash
# Manual review of README.md
```

---

### Issue 3.4: Clean Up Root Directory

**Files:**
- `main.py` (delete)
- `config.yaml` (move to tests/ or delete)

**Problem:** Junk files cluttering the repository root.

**Acceptance Criteria:**
- [ ] `main.py` removed from root
- [ ] `config.yaml` moved to `tests/fixtures/` or removed
- [ ] No development artifacts in root

**Verification:**
```bash
ls -la | grep -E "(main.py|config.yaml)"
# Should return nothing
```

---

## Phase 4: Feature Flags System

**Priority:** MEDIUM — Enables safe experimentation
**Dependencies:** Phase 1
**Estimated Issues:** 4

### Issue 4.1: Create FeatureFlag Class

**Files:** `configloader/features.py` (new file)

**Problem:** No way to safely experiment with new features.

**Required Implementation:**
```python
from dataclasses import dataclass
import os

@dataclass
class FeatureFlag:
    """A feature flag with environment variable override."""
    name: str
    default: bool
    env_var: str | None = None

    @property
    def enabled(self) -> bool:
        if self.env_var:
            env_value = os.environ.get(self.env_var, "").lower()
            if env_value in ("true", "1", "yes"):
                return True
            if env_value in ("false", "0", "no"):
                return False
        return self.default
```

**Acceptance Criteria:**
- [ ] `FeatureFlag` class created with name, default, env_var attributes
- [ ] `enabled` property respects environment variable override
- [ ] Environment override works for true/false values

**Verification:**
```bash
pytest tests/test_features.py -v -k "test_feature_flag"
```

---

### Issue 4.2: Create FeatureFlags Container

**Files:** `configloader/features.py`

**Problem:** Need a central registry of feature flags.

**Required Implementation:**
```python
class FeatureFlags:
    """Container for all feature flags."""

    # Add flags here as the library evolves
    NESTED_ENV_VARS = FeatureFlag(
        name="nested_env_vars",
        default=False,
        env_var="CONFIGLOADER_NESTED_ENV_VARS"
    )

    TYPE_COERCION = FeatureFlag(
        name="type_coercion",
        default=False,
        env_var="CONFIGLOADER_TYPE_COERCION"
    )
```

**Acceptance Criteria:**
- [ ] `FeatureFlags` class with initial flags defined
- [ ] Flags are class attributes for easy access
- [ ] Environment variable naming convention is consistent

**Verification:**
```bash
pytest tests/test_features.py -v
```

---

### Issue 4.3: Export FeatureFlags

**Files:** `configloader/__init__.py`

**Problem:** FeatureFlags needs to be accessible from package root.

**Required Change:**
```python
from configloader.features import FeatureFlags

__all__ = [..., "FeatureFlags"]
```

**Acceptance Criteria:**
- [ ] `from configloader import FeatureFlags` works
- [ ] Added to `__all__` list

**Verification:**
```bash
python -c "from configloader import FeatureFlags; print(FeatureFlags.NESTED_ENV_VARS.enabled)"
```

---

### Issue 4.4: Add Feature Flag Tests

**Files:** `tests/test_features.py` (new file)

**Problem:** Need tests for feature flag functionality.

**Required Tests:**
- Test default value is returned when env var not set
- Test env var override for "true" values
- Test env var override for "false" values
- Test flag without env_var uses default only

**Acceptance Criteria:**
- [ ] Test file created with comprehensive tests
- [ ] All tests pass
- [ ] Tests use proper fixtures and cleanup

**Verification:**
```bash
pytest tests/test_features.py -v
```

---

## Phase 5: Core Enhancements

**Priority:** MEDIUM — Improves usability
**Dependencies:** Phase 1, Phase 4 (feature flags)
**Estimated Issues:** 4

### Issue 5.1: Add Nested Environment Variable Support

**Files:** `configloader/sources.py:54` (EnvConfigSource)

**Problem:** Can't represent nested config via environment variables.

**Required Implementation:**
```python
# In EnvConfigSource.load()
def _parse_nested_key(self, key: str) -> list[str]:
    """Parse key with __ separator into nested path."""
    return key.split("__")

def _set_nested(self, config: Dict[str, Any], keys: list[str], value: str) -> None:
    """Set a value in a nested dict structure."""
    for key in keys[:-1]:
        config = config.setdefault(key.lower(), {})
    config[keys[-1].lower()] = value
```

**Example:**
```
MYAPP_DATABASE__HOST=localhost → {"database": {"host": "localhost"}}
```

**Acceptance Criteria:**
- [ ] `__` separator creates nested dicts
- [ ] Works with existing prefix functionality
- [ ] Feature flag controls whether this is enabled

**Verification:**
```bash
CONFIGLOADER_NESTED_ENV_VARS=true pytest tests/test_unit_sources.py -v -k "nested"
```

---

### Issue 5.2: Add `reload()` Method

**Files:** `configloader/core.py`

**Problem:** Can't refresh cached config in long-running applications.

**Required Implementation:**
```python
def reload(self) -> Dict[str, Any]:
    """Force reload configuration from all sources.

    Clears the cache and re-loads from all configured sources.
    Useful for long-running applications or tests.

    Returns:
        The freshly loaded configuration dict.
    """
    self._config = None
    return self.load_config()
```

**Acceptance Criteria:**
- [ ] `reload()` method clears cache and re-loads
- [ ] Returns the new config
- [ ] Test verifies cache is actually cleared

**Verification:**
```bash
pytest tests/test_unit_core.py -v -k "reload"
```

---

### Issue 5.3: Add Type Coercion for Environment Variables

**Files:** `configloader/sources.py`

**Problem:** Environment variables are always strings, but config often needs int/bool.

**Required Implementation:**
```python
def _coerce_type(self, value: str) -> str | int | bool | list:
    """Attempt to coerce string value to appropriate type."""
    # Boolean
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False

    # Integer
    try:
        return int(value)
    except ValueError:
        pass

    # JSON list/dict
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

    return value
```

**Acceptance Criteria:**
- [ ] "true"/"false" → bool
- [ ] "123" → int
- [ ] "[1,2,3]" → list
- [ ] Feature flag controls whether this is enabled

**Verification:**
```bash
CONFIGLOADER_TYPE_COERCION=true pytest tests/test_unit_sources.py -v -k "coercion"
```

---

### Issue 5.4: Improve Error Messages

**Files:** `configloader/core.py`

**Problem:** Error messages when no sources configured are unclear.

**Required Implementation:**
```python
def load_config(self) -> Dict[str, Any]:
    if self._config is not None:
        return self._config

    # Check if any sources are configured
    if not self._has_any_source():
        raise ConfigLoaderError(
            "No configuration sources provided. Expected at least one of:\n"
            f"  - Config file at: {self._get_expected_file_path()}\n"
            "  - Environment variables with prefix (use env_prefix='MYAPP_')\n"
            "  - CLI arguments (use cli_args=parser.parse_args())\n"
            "  - Custom sources (use custom_sources=[...])"
        )

    # ... rest of loading logic
```

**Acceptance Criteria:**
- [ ] Clear error message when no sources configured
- [ ] Error message shows expected file path
- [ ] Error message lists all possible source types

**Verification:**
```bash
pytest tests/test_unit_core.py -v -k "error"
```

---

## Phase 6: CLI Implementation

**Priority:** LOW — Nice to have
**Dependencies:** Phase 1, Phase 2
**Estimated Issues:** 3

### Issue 6.1: Add CLI Dependencies

**Files:** `pyproject.toml`

**Problem:** CLI module needs typer and rich but they're not installed.

**Required Change:**
```toml
[tool.poetry.extras]
cli = ["typer", "rich"]

[tool.poetry.dependencies]
typer = {version = "^0.9.0", optional = true}
rich = {version = "^13.0", optional = true}
```

**Acceptance Criteria:**
- [ ] typer and rich added as optional dependencies
- [ ] `poetry install --extras cli` works
- [ ] Base install doesn't require these dependencies

**Verification:**
```bash
poetry install --extras cli
```

---

### Issue 6.2: Implement Validate Command

**Files:** `configloader/cli/commands.py` or `configloader/cli/__init__.py`

**Problem:** No CLI command to validate config files.

**Required Implementation:**
```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def validate(
    file: Path = typer.Argument(..., help="Config file to validate"),
    schema: Optional[str] = typer.Option(None, help="Pydantic model path for schema validation")
):
    """Validate a configuration file."""
    # 1. Check file exists
    # 2. Parse file based on extension
    # 3. If schema provided, validate against it
    # 4. Report success or errors
```

**Acceptance Criteria:**
- [ ] `configloader validate config.yaml` checks file is valid
- [ ] `configloader validate config.yaml --schema app.config:AppConfig` validates against schema
- [ ] Clear error messages on failure
- [ ] Success message on valid config

**Verification:**
```bash
poetry run configloader validate tests/fixtures/config.toml
```

---

### Issue 6.3: Implement Check Command

**Files:** `configloader/cli/commands.py`

**Problem:** No way to see parsed config for debugging.

**Required Implementation:**
```python
@app.command()
def check(
    file: Path = typer.Argument(..., help="Config file to check"),
    format: str = typer.Option("yaml", help="Output format: yaml, json, toml")
):
    """Parse and display a configuration file."""
    # 1. Parse the file
    # 2. Pretty-print in requested format
```

**Acceptance Criteria:**
- [ ] `configloader check config.yaml` displays parsed config
- [ ] Supports yaml, json, toml output formats
- [ ] Uses rich for pretty printing

**Verification:**
```bash
poetry run configloader check tests/fixtures/config.toml --format json
```

---

## Phase 7: Publish Readiness

**Priority:** LOW — Final polish
**Dependencies:** Phases 1-6
**Estimated Issues:** 3

### Issue 7.1: Create Integration Test

**Files:** `tests/test_integration.py` (new file)

**Problem:** No end-to-end test that exercises the full library.

**Required Tests:**
- Load from file, env, and CLI simultaneously
- Verify merge priority is correct
- Verify Pydantic validation works
- Test error handling paths

**Acceptance Criteria:**
- [ ] Integration test file created
- [ ] Tests full loading flow with all source types
- [ ] Tests validation flow
- [ ] All tests pass

**Verification:**
```bash
pytest tests/test_integration.py -v
```

---

### Issue 7.2: Verify CI Pipeline

**Files:** `.github/workflows/`

**Problem:** CI pipeline may need updates after all changes.

**Checklist:**
- [ ] Tests run on multiple Python versions (3.11, 3.12)
- [ ] mypy check is included
- [ ] Coverage reporting works
- [ ] All jobs pass

**Verification:**
```bash
# Push to branch and check GitHub Actions
```

---

### Issue 7.3: TestPyPI Dry Run

**Files:** None (external process)

**Problem:** Need to verify package publishes correctly before real release.

**Steps:**
1. Bump version to test version (e.g., 0.1.0.dev1)
2. Build package: `poetry build`
3. Publish to TestPyPI: `poetry publish -r testpypi`
4. Install from TestPyPI and verify

**Acceptance Criteria:**
- [ ] Package builds successfully
- [ ] Package publishes to TestPyPI
- [ ] Package installs from TestPyPI
- [ ] Basic import works after install

**Verification:**
```bash
pip install --index-url https://test.pypi.org/simple/ configloader
python -c "from configloader import ConfigLoader; print('OK')"
```

---

## Dependency Graph

```
Phase 1 (Critical Bugs)
    ↓
Phase 2 (Type System) ←──┐
    ↓                    │
Phase 3 (Modernize) ─────┘ (can run in parallel)
    ↓
Phase 4 (Feature Flags)
    ↓
Phase 5 (Enhancements)
    ↓
Phase 6 (CLI)
    ↓
Phase 7 (Publish)
```

---

## Quick Reference

### Run All Quality Checks
```bash
black configloader tests && isort configloader tests && ruff check configloader tests && mypy configloader && pytest
```

### Check Specific Phase Progress
```bash
# Phase 1: Critical bugs fixed?
pytest tests/ -v

# Phase 2: Type system clean?
mypy configloader --strict

# Phase 3: No deprecation warnings?
poetry check

# Full verification
poetry run pytest && poetry run mypy configloader && poetry check
```

---

**Last Updated:** 2026-02-02
