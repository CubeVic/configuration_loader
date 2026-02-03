---
phase: 01-fix-critical-bugs
plan: 02
subsystem: parsers
tags: [mypy, typing, Path, Dict, type-hints]

# Dependency graph
requires:
  - phase: 01-01
    provides: Parser error handling fixes (ConfigParserError now raised)
provides:
  - Consistent parser type signatures matching BaseParser ABC
  - Correct ConfigValidationError.errors type for Pydantic compatibility
affects: [02-type-system, core]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Parser signatures use Path parameter and Dict[str, Any] return type"
    - "Exception error attributes use List[Dict[str, Any]] for Pydantic compatibility"

key-files:
  created: []
  modified:
    - configloader/parsers/json_parser.py
    - configloader/parsers/yaml_parser.py
    - configloader/parsers/toml_parser.py
    - configloader/exceptions.py

key-decisions:
  - "Renamed parameter from config_file_path to file_path for consistency with base class"

patterns-established:
  - "All parser implementations must match BaseParser.load(self, path: Path) -> Dict[str, Any] signature"

issues-created: []

# Metrics
duration: 3min
completed: 2026-02-03
---

# Phase 01 Plan 02: Fix Type Signatures Summary

**Parser type signatures aligned with BaseParser ABC; ConfigValidationError.errors typed as List[Dict[str, Any]] for Pydantic compatibility**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-03T14:48:28Z
- **Completed:** 2026-02-03T14:51:01Z
- **Tasks:** 2/2
- **Files modified:** 4

## Accomplishments

- All three parsers (JSON, YAML, TOML) now use `Path` parameter type and `Dict[str, Any]` return type
- ConfigValidationError.errors correctly typed as `List[Dict[str, Any]]` to match Pydantic's `e.errors()` format
- Parameter renamed from `config_file_path` to `file_path` for consistency with base class
- mypy reports no errors for all modified files (ignoring missing stubs for yaml/toml - Phase 2 concern)

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix parser type signatures to use Path and Dict[str, Any]** - `12d3c82` (fix)
2. **Task 2: Fix ConfigValidationError.errors type hint** - `4672d36` (fix)

## Files Created/Modified

- `configloader/parsers/json_parser.py` - Updated signature to `load(self, file_path: Path) -> Dict[str, Any]`
- `configloader/parsers/yaml_parser.py` - Updated signature to `load(self, file_path: Path) -> Dict[str, Any]`
- `configloader/parsers/toml_parser.py` - Updated signature to `load(self, file_path: Path) -> Dict[str, Any]`
- `configloader/exceptions.py` - Changed errors type from `dict` to `Optional[List[Dict[str, Any]]]`

## Decisions Made

- Renamed parameter from `config_file_path` to `file_path` for consistency with base class naming convention

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Next Phase Readiness

- Type signatures now consistent across all parsers
- Exception types correct for Pydantic integration
- Ready for Plan 01-03 (path handling bug fix)
- Note: mypy still reports missing type stubs for yaml/toml - this is Phase 2 scope (Issue 2.1)

---
*Phase: 01-fix-critical-bugs*
*Completed: 2026-02-03*
