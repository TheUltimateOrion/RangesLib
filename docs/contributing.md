# Contributing

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Tests

Run all tests with:

```bash
./run_tests.sh
```

The same suite runs on every push through GitHub Actions for Python 3.12, 3.13, and 3.14.

## API documentation

Install the optional documentation tools and generate HTML reference pages:

```bash
python -m pip install -r requirements.txt
./generate_docs.sh
```

The generator imports the local `rangeslib` package and writes HTML output to `docs/_build/html/`.

## Adding an adaptor

1. Implement it in `_adaptors.py` as a `RangeAdaptor` subclass.
2. Document its input shape, output shape, and eager behavior.
3. Export it from `rangeslib.__init__` and `__all__`.
4. Add behavior and namespace tests.
5. Update `README.md` or the relevant guide.
