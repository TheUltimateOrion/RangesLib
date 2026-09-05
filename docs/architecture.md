# Architecture

## Package layout

```text
src/rangeslib/
├── __init__.py       Public exports and the grouped `Ranges` namespace
├── _core.py          Range, RangeAdaptor, and RangeGenerator
├── _generators.py    Sources that construct Range values
└── _adaptors.py      Callable transformations over iterables
```

The `src` layout prevents accidental imports from the repository root and matches standard Python packaging practice.

## Data flow

```text
Iterable[T] -> RangeAdaptor -> Output

RangeGenerator -> Range[T]
Range[T] | RangeAdaptor[T, U] -> U
ordinary Iterable[T] | RangeAdaptor[T, U] -> U
```

`RangeAdaptor` is an abstract callable contract. Its `__ror__` method enables built-in types such as `str`, `list`, and `range` to participate in pipelines. `Range.__or__` supplies a precise type-checker signature for the library's primary container.

## Generators and adaptors

Generators are nominal source types: `Iota`, `Repeat`, and the other factories inherit from `RangeGenerator` and produce a `Range` directly.

Adaptors are transformations. Type-preserving adaptors use one element type, such as `Iterable[T] -> Range[T]`. `Transform` and `To` use separate input and output types because they change either the element type or the entire collection type.

## Eager execution

Every current adaptor returns an already-materialized `Range` except `To`, which returns the requested target type. This makes the API simple and repeatable, but differs from C++ ranges, where most views are lazy. Adaptors that consume a one-shot iterator therefore consume it during the call.

## C++ correspondence

Names and core behavior are inspired by C++20, C++23, and C++26 ranges where useful, but the API follows Python conventions:

- Python iterables replace iterator/sentinel pairs.
- `Range` replaces a general-purpose view object for now.
- `tuple` results replace C++ reference tuples.
- Python callables replace customization point objects.
- Invalid sizes and empty patterns raise `ValueError`.
