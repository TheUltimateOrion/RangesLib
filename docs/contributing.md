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
work.

## Quality checks

Run the unit suite:

```bash
./run_tests.sh
```

Run the same coverage threshold used by CI:

```bash
coverage run -m unittest discover -s tests
coverage report
```

Run linting, formatting validation, and static typing:

```bash
ruff check src tests
ruff format --check src
mypy src/rangeslib tests/typecheck/public_api.py
```

Build the documentation with warnings treated as errors:

```bash
./generate_docs.sh
```

Build the distributions:

```bash
python -m build
```

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
