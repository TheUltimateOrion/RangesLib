# Contributing

## Local setup

Create and activate a virtual environment, then install the development extra:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The helper scripts use the active `python` on `PATH`. They do not require a
virtual environment named `.venv`, so alternate environment managers also
work. Set the `PYTHON` environment variable if you want the scripts to use a
specific interpreter, for example `PYTHON=python3.13 ./scripts/check.sh`.

## Formatting and quality workflow

Formatting and checking are intentionally separate operations.

### Apply formatting

Run:

```bash
./scripts/format.sh
```

This is a **mutating** developer command. It runs:

```text
ruff check . --fix
ruff format .
```

The repository root is used instead of a hard-coded `src tests` list, so Python
files such as `playground.py`, `docs/conf.py`, and static type-check fixtures
are formatted consistently too. Ruff still honors its configured and standard
exclusions.

Review the resulting diff before committing. CI never invokes `scripts/format.sh` and
never automatically commits formatting changes.

### Install pre-commit hooks

After installing the development tools, install the local hooks:

```bash
python -m pre_commit install
```

The hooks run Ruff, mypy, and Pyright before every commit. To run all hooks
manually, use:

```bash
python -m pre_commit run --all-files
```

### Validate the source tree

Run:

```bash
./scripts/check.sh
```

This is the same quality command used by the GitHub Actions quality job. It
performs, in order:

1. `ruff check .`
2. `ruff format --check .`
3. mypy over the package and public API type assertions
4. Pyright over the package and public API type assertions
5. the unit suite under branch coverage, including the configured coverage
   threshold

The script does not rewrite tracked source files. Coverage artifacts are
ignored by Git.

### Validate the complete release tree

Run:

```bash
./scripts/check_all.sh
```

This runs `scripts/check.sh`, then builds Sphinx documentation with warnings promoted
to errors. GitHub Actions uses this complete gate before deployment.

For a faster test-only pass, use:

```bash
./scripts/run_tests.sh
```

For the two static type checkers only, use:

```bash
./scripts/typecheck.sh
```

Ruff validates syntax, style, and code quality. Mypy and Pyright intentionally
both validate static types: Pyright matches the analysis engine used by
Pylance, while mypy provides an independent implementation.

### Validate distributions

Run:

```bash
./scripts/check_package.sh
```

This mirrors the package CI job. It builds the sdist and wheel, creates a
temporary isolated virtual environment, installs the built wheel, then verifies
basic public behavior and the packaged `py.typed` marker outside the checkout.

A good pre-push sequence is therefore:

```bash
./scripts/format.sh
./scripts/check_all.sh
./scripts/check_package.sh
```

## CI mapping

GitHub Actions deliberately delegates to repository scripts instead of
reimplementing their commands in YAML. This keeps local development and CI from
drifting apart.

| Local command | GitHub Actions use | Purpose |
| --- | --- | --- |
| `./scripts/format.sh` | Local only | Apply Ruff fixes and formatting |
| `./scripts/run_tests.sh` | Python 3.12/3.13/3.14 matrix | Runtime compatibility |
| `./scripts/check.sh` | Called by `./scripts/check_all.sh` | Ruff, mypy, Pyright, coverage |
| `./scripts/check_all.sh` | `Quality gates` job | Source quality plus strict docs |
| `./scripts/typecheck.sh` | Called by `./scripts/check.sh` | mypy and Pyright only |
| `./scripts/check_package.sh` | `Build and install package` job | Distribution and installed-wheel validation |
| `./scripts/generate_docs.sh` | Documentation deployment | Build the deployable Sphinx site |

A CI formatting failure should be fixed locally with `./scripts/format.sh`, reviewed,
committed, and pushed. The CI workflow must remain read-only with respect to
tracked source code.

## Releases

The `Release` workflow runs for pushes to `main` that modify `pyproject.toml`.
It compares `[project].version` with the previous commit. When the version has
changed, it runs `scripts/check_all.sh`, runs `scripts/check_package.sh`, then
creates the matching `v<version>` tag and GitHub release with generated notes.

Do not manually create a tag for a future version. Commit the version bump and
changelog entry together, then push `main`; the workflow handles the release.

Published GitHub Releases trigger the PyPI publishing workflow. See
[Publishing](publishing.md) for the required PyPI Trusted Publishing setup.

## Documentation deployment

GitHub Pages deployment is a separate CD workflow, but it is not independent of
CI. The deployment workflow listens for completion of the **Tests and quality**
workflow on `main` and runs only when that workflow concluded successfully.

The deployment workflow checks out `workflow_run.head_sha`, so it builds the
exact commit that passed CI rather than whatever commit happens to be at the tip
of `main` when the deployment runner starts.

## Test organization

- `tests/test_range.py` covers private implementation mechanics and core
  pipeline behavior.
- `tests/test_public_api.py` verifies the API exposed through `ranges` and
  `views`, including validation and iterator-consumption contracts.
- `tests/test_range_collection.py` protects `Range`'s list-like reconstruction
  behavior.
- `tests/typecheck/public_api.py` contains static type assertions and is run by
  mypy in CI.

Prefer public-facade regression tests for user-visible bugs even when a private
implementation test is also useful.

## Adding a source

1. Implement the source in `_generators.py` as a `RangeGenerator` subclass.
2. Add a lowercase factory to `ranges.py`.
3. Add the factory name to `ranges.__all__`.
4. Document its value domain, edge cases, and result type.
5. Add public-facade tests and, where useful, implementation tests.
6. Update the changelog for user-visible behavior.

## Adding an adaptor

1. Implement it in `_adaptors.py` as a `RangeAdaptor` subclass.
2. Document its input shape, output shape, eager behavior, iterator consumption,
   and validation rules.
3. Add a lowercase factory to `views.py` and `views.__all__`.
4. Preserve public typing. If the factory cannot infer the pipeline element type
   from its own arguments, use the existing structural-protocol pattern in
   `views.py` rather than returning an unbounded `Any` type by default.
5. Add behavior tests through the public facade. Add private-class tests when
   they cover implementation-specific mechanics.
6. Update `docs/usage.md`, API docstrings, and the changelog.

Do **not** export the implementation class from `rangeslib.__init__`. The root
namespace intentionally contains only `Range`, `ranges`, and `views`.

## Documentation changes

The documentation build runs with Sphinx warnings promoted to errors. Keep
examples executable and ensure the usage guide and architecture contract agree
with the implementation and tests.

Version information is read from `pyproject.toml` by `docs/conf.py`; do not
manually duplicate the version in Sphinx configuration.

## Pull requests and CI

CI runs on pushes and pull requests. It validates supported Python versions,
public behavior, coverage, linting, formatting, typing, documentation, package
building, and installation from the built wheel.

Before opening or updating a pull request, run the pre-push sequence above. If
CI reports `ruff format --check` failures, run `./scripts/format.sh` locally and commit
the resulting formatting changes rather than changing the CI workflow to
format code automatically.
