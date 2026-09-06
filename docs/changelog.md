# Changelog

The project follows semantic-versioning conventions where practical during the
`0.x` development series. Public changes are recorded here; private modules may
change independently.

## 0.4.0 - 2026-09-05

### Added

- `views.all` for materializing existing Python iterables into reusable `Range`
  values, similar in purpose to C++ `views::all`.

## 0.3.3 - 2026-09-05

### Added

- Automated GitHub releases when `[project].version` changes on `main` after
  source quality, documentation, package, and wheel-install checks pass.
- GitHub issue and pull request templates, plus local pre-commit hooks for
  Ruff, mypy, and Pyright.

### Changed

- Moved developer commands into `scripts/` and updated CI, documentation, and
  source-distribution packaging to use the new paths.

## 0.3.2 - 2026-09-05

### Added

- Ruff, mypy, and Pyright as required, independently configured validation
  categories in the local quality gate and CI.
- `scripts/typecheck.sh` for running mypy and Pyright without the full test, coverage,
  package, and documentation checks.

### Changed

- The CI quality job now explicitly reports its Ruff, mypy, and Pyright gate.
- `scripts/check.sh` forwards its selected `PYTHON` interpreter to
  `scripts/typecheck.sh`.

## 0.3.1

### Fixed

- Corrected `Range` slicing, concatenation, multiplication, and copying so
  `UserList` reconstruction does not create nested single-element ranges.
- Made non-negative `take` consume only the requested prefix, allowing it to
  bound one-shot and infinite iterators.
- Corrected stale contributor guidance that told contributors to export private
  adaptor classes from the package root.
- Corrected API reference section markup and removed contradictory validation
  wording from the architecture contract.

### Changed

- `ranges.single` is now generically typed and preserves the input value type.
- Public typing for several no-input-type adaptor factories now uses structural
  protocols so pipeline element types can be inferred at call/pipe time.
- Development helper scripts use the active Python environment rather than
  assuming a repository-local `.venv`.
- CI now invokes repository validation scripts directly, and GitHub Pages
  deployment waits for a successful CI run on `main` before building the exact
  validated commit.
- Documentation now distinguishes end-user installation from contributor setup
  and documents materialization, iterator consumption, validation, extension,
  and compatibility contracts.

### Added

- `py.typed` marker for PEP 561 inline typing.
- Public-facade and `Range` collection-contract regression tests.
- Static public API type assertions.
- Coverage, linting, formatting, typing, package-build, wheel-install, and
  documentation quality gates in CI.
- `format.sh`, `check.sh`, and `check_package.sh` developer commands so local
  formatting, quality validation, and distribution validation use the same
  executable policy as CI.
- Project metadata, repository/documentation links, migration notes, and this
  changelog.

## 0.3.0

- Introduced the lowercase `ranges` and `views` facade.
- Reduced the package-root public namespace to `Range`, `ranges`, and `views`.
- Documented eager execution and ordinary-iterable pipeline support.

## 0.2.0

- Added project documentation and GitHub Pages automation.

## 0.1.0

- Established the initial range container, source generators, and adaptor set.
