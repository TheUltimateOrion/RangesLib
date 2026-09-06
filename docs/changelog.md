# Changelog

The project follows semantic-versioning conventions where practical during the
`0.x` development series. Public changes are recorded here; private modules may
change independently.

## 0.8.1 - 2026-09-06

### Fixed

- Added a less precise fallback type for `views.zip` and
  `views.cartesian_product` calls with more than two companion iterables,
  matching their existing runtime support.

## 0.8.0 - 2026-09-06

### Changed

- Improved public typing for `views.zip` and `views.cartesian_product` with
  zero, one, and two companion iterables. Larger runtime arities remain
  supported but are typed less precisely.

## 0.7.0 - 2026-09-06

### Changed

- `Range.__str__()` now matches normal list formatting, including quoted string
  elements.

## 0.6.1 - 2026-09-06

### Added

- `views.to(str)` for concatenating string elements without requiring an
  explicit `"".join` factory.

### Fixed

- Corrected the historical `0.2.0` changelog entry so it no longer repeats
  changes from `0.5.0`.

## 0.6.0 - 2026-09-05

### Added

- Automated PyPI publishing through GitHub Releases and PyPI Trusted
  Publishing.
- Publishing documentation covering the release flow, trusted publisher fields,
  and GitHub environment behavior.
- Manual PyPI publishing workflow dispatch for existing releases.

## 0.5.1 - 2026-09-05

### Added

- C++ ranges comparison notes documenting where `rangeslib` follows C++ naming
  and where Python's eager iterable model intentionally differs.
- Roadmap notes for collecting future work as issues instead of adding more
  adaptors immediately.

### Changed

- Reworked the README into a shorter tutorial-style introduction focused on
  the core mental model: `ranges` creates, `views` transforms, and `views.to`
  converts.
- Tightened usage documentation examples so the README stays concise and the
  usage guide carries the fuller API catalog.

## 0.5.0 - 2026-09-05

### Added

- Reusable adaptor composition, allowing pipelines such as
  `views.filter(predicate) | views.take(3)` to be reused with multiple inputs.
- `views.take_while` and `views.drop_while` aliases for C++-style naming.
- Scalar delimiters for `views.split` and `views.join_with`, while retaining
  iterable separator-pattern support.
- `scripts/benchmark.py` for local performance measurements of large eager
  pipelines.

### Changed

- `views.split` now validates an empty separator before consuming its input.
- Public typing now supports mixed-type two-range `zip` and `cartesian_product`,
  typed `keys` and `values`, and exact pairwise tuple output.

## 0.4.0 - 2026-09-05

### Added

- `views.all` for materializing existing Python iterables into reusable `Range`
  values, similar in purpose to C++ `views::all`.
- Coverage now reports 100% executable line and branch coverage.

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

- Established the initial range container, source generators, and adaptor set.
