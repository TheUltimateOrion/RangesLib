# Usage

## Installation

`rangeslib` requires Python 3.12 or newer and has no runtime dependencies.
From a source checkout:

```bash
python -m pip install .
```

Contributor tooling is installed separately with:

```bash
python -m pip install -e ".[dev]"
```

## Public API

Application code should import the two public facade modules and, when needed,
the `Range` container:

```python
from rangeslib import Range, ranges, views
```

Modules beginning with `_` are private implementation details.

## `Range`

`Range` is an eager mutable sequence backed by `collections.UserList`.
Construction is positional:

```python
from rangeslib import Range

values = Range(1, 2, 3)
nested = Range([1, 2, 3])

assert list(values) == [1, 2, 3]
assert list(nested) == [[1, 2, 3]]
```

Normal reconstruction operations preserve the `Range` type:

```python
assert list(values[1:]) == [2, 3]
assert list(values + [4]) == [1, 2, 3, 4]
assert list([0] + values) == [0, 1, 2, 3]
assert list(values * 2) == [1, 2, 3, 1, 2, 3]
assert list(values.copy()) == [1, 2, 3]
```

`copy()` is shallow. Mutating the copied outer sequence does not mutate the
original sequence, but mutable elements are shared.

## Generators

The `ranges` module constructs eager `Range` values.

| Factory | Result | Edge behavior |
| --- | --- | --- |
| `ranges.empty()` | empty `Range[int]` | always empty |
| `ranges.single(value)` | one-element `Range[T]` | preserves the value type |
| `ranges.iota(start, end)` | integers in `[start, end)` | same direction rules as built-in `range`; `start >= end` is empty |
| `ranges.indices(count)` | integers in `[0, count)` | non-positive counts are empty |
| `ranges.repeat(value, count)` | `count` copies of `value` | non-positive counts are empty |

Examples:

```python
from rangeslib import ranges

assert list(ranges.empty()) == []
assert list(ranges.single("x")) == ["x"]
assert list(ranges.iota(2, 5)) == [2, 3, 4]
assert list(ranges.indices(3)) == [0, 1, 2]
assert list(ranges.repeat("x", 3)) == ["x", "x", "x"]
```

## Pipelines

Adaptors can be called directly:

```python
from rangeslib import views

result = views.take(2)([1, 2, 3])
assert list(result) == [1, 2]
```

or placed on the right side of `|`:

```python
from rangeslib import ranges, views

result = (
    ranges.iota(1, 7)
    | views.reverse()
    | views.filter(lambda value: value % 2 == 0)
    | views.transform(lambda value: value * 10)
    | views.take(2)
)

assert list(result) == [60, 40]
```

Ordinary iterables can start pipelines because adaptors implement reflected
`|` dispatch:

```python
text = "abcdef" | views.take(3) | views.to("".join)
assert text == "abc"
```

## Materialization and one-shot iterators

Most adaptors return a fully materialized `Range`. This makes returned results
repeatable but means many operations consume the complete finite input before
returning.

Two bounded-prefix operations intentionally stop early:

```python
source = iter([1, 2, 3, 4])
assert list(views.take(2)(source)) == [1, 2]
assert next(source) == 3

source = iter([1, 2, 3, 4])
assert list(views.counted(2)(source)) == [1, 2]
assert next(source) == 3
```

Positive `take` can therefore bound an infinite iterable:

```python
import itertools

assert list(views.take(3)(itertools.count(10))) == [10, 11, 12]
```

Negative `take` is different. It intentionally follows Python slice-stop
semantics, equivalent to `list(iterable)[:count]`, so it must consume the
entire input first.

`takewhile` stops when its predicate first returns false. On a one-shot
iterator, the first failing value has already been consumed when the adaptor
returns.

Do not apply full-materialization adaptors directly to infinite iterables.
Instead, bound the iterable first where the desired operation permits it.

## Value processing adaptors

### `views.reverse()`

- **Input:** `Iterable[T]`
- **Output:** `Range[T]`
- **Consumption:** complete finite input
- **Validation:** none

Returns all values in reverse order.

```python
assert list(views.reverse()([1, 2, 3])) == [3, 2, 1]
```

### `views.filter(predicate)`

- **Input:** `Iterable[T]`
- **Output:** `Range[T]`
- **Consumption:** complete finite input
- **Validation:** exceptions from `predicate` propagate

Keeps values for which `predicate(value)` is true.

```python
assert list(views.filter(lambda x: x % 2 == 0)(range(6))) == [0, 2, 4]
```

### `views.transform(func)`

- **Input:** `Iterable[T]`
- **Output:** `Range[U]`
- **Consumption:** complete finite input
- **Validation:** exceptions from `func` propagate

Maps each value through `func`.

```python
assert list(views.transform(str)([1, 2])) == ["1", "2"]
```

### `views.take(count)`

- **Input:** `Iterable[T]`
- **Output:** `Range[T]`
- **Consumption:** bounded for `count >= 0`; complete input for `count < 0`
- **Validation:** negative counts are valid

Uses Python slice-stop semantics. Examples:

```python
assert list(views.take(2)([1, 2, 3, 4])) == [1, 2]
assert list(views.take(0)([1, 2, 3, 4])) == []
assert list(views.take(-1)([1, 2, 3, 4])) == [1, 2, 3]
```

### `views.drop(count)`

- **Input:** `Iterable[T]`
- **Output:** `Range[T]`
- **Consumption:** complete finite input
- **Validation:** negative counts are valid

Uses Python slice-start semantics:

```python
assert list(views.drop(2)([1, 2, 3, 4])) == [3, 4]
assert list(views.drop(-1)([1, 2, 3, 4])) == [4]
```

### `views.takewhile(predicate)`

Returns the initial prefix while `predicate` is true. It stops at and consumes
the first failing value from a one-shot iterator.

```python
assert list(views.takewhile(lambda x: x < 3)([1, 2, 3, 2])) == [1, 2]
```

### `views.dropwhile(predicate)`

Drops the initial prefix while `predicate` is true, then materializes the
remaining values.

```python
assert list(views.dropwhile(lambda x: x < 3)([1, 2, 3, 2])) == [3, 2]
```

### `views.counted(count)`

Consumes at most `count` values from the input's current iterator position and
leaves later values unconsumed. `count` must be non-negative.

```python
source = iter([1, 2, 3])
assert list(views.counted(2)(source)) == [1, 2]
assert next(source) == 3
```

`views.counted(-1)` raises `ValueError`.

## Projection and indexing adaptors

### `views.elements(index)`

Projects `value[index]` from every tuple-like or integer-indexable input value.
Indexing errors propagate normally.

```python
pairs = [("a", 1), ("b", 2)]
assert list(views.elements(0)(pairs)) == ["a", "b"]
```

### `views.keys()` and `views.values()`

Convenience projections for indexes `0` and `1`:

```python
pairs = [("a", 1), ("b", 2)]
assert list(views.keys()(pairs)) == ["a", "b"]
assert list(views.values()(pairs)) == [1, 2]
```

### `views.enumerate(start=0)`

Pairs values with sequential integer indexes and returns
`Range[tuple[int, T]]`.

```python
assert list(views.enumerate(5)(["a", "b"])) == [(5, "a"), (6, "b")]
```

## Combining iterables

### `views.concat(*iterables)`

Appends each configured iterable after the piped input and materializes the
combined result.

```python
assert list(views.concat([3], [4, 5])([1, 2])) == [1, 2, 3, 4, 5]
```

### `views.zip(*iterables)`

Zips the pipeline input with configured iterables and stops at the shortest
participating iterable.

```python
assert list(views.zip([10, 20])([1, 2, 3])) == [(1, 10), (2, 20)]
```

### `views.zip_transform(func, *iterables)`

Zips corresponding values and calls `func(*values)` for each group.

```python
result = views.zip_transform(lambda a, b: a + b, [10, 20])([1, 2, 3])
assert list(result) == [11, 22]
```

### `views.cartesian_product(*iterables)`

Returns tuples from the Cartesian product of the pipeline input and configured
iterables. Inputs and results are materialized, so use finite iterables.

```python
result = views.cartesian_product([10, 20])([1, 2])
assert list(result) == [(1, 10), (1, 20), (2, 10), (2, 20)]
```

## Windows and grouping

### `views.adjacent(width=2)`

Returns overlapping tuple windows of exactly `width` values. `width` must be
positive. If the input is shorter than `width`, the result is empty.

```python
assert list(views.adjacent(3)([1, 2, 3, 4])) == [(1, 2, 3), (2, 3, 4)]
```

### `views.pairwise()`

Equivalent to `adjacent(2)`.

```python
assert list(views.pairwise()([1, 2, 3])) == [(1, 2), (2, 3)]
```

### `views.adjacent_transform(func, width=2)`

Calls `func(*window)` for each overlapping window. `width` must be positive.

```python
result = views.adjacent_transform(lambda a, b: a + b, 2)([1, 2, 3])
assert list(result) == [3, 5]
```

### `views.pairwise_transform(func)`

Calls a binary function for every adjacent pair.

```python
result = views.pairwise_transform(lambda a, b: a * b)([1, 2, 3])
assert list(result) == [2, 6]
```

### `views.chunk(size)`

Partitions input into non-overlapping `Range` chunks. `size` must be positive;
the final chunk may be shorter.

```python
result = views.chunk(2)([1, 2, 3, 4, 5])
assert [list(chunk) for chunk in result] == [[1, 2], [3, 4], [5]]
```

### `views.slide(width)`

Returns overlapping `Range` windows of exactly `width` values. `width` must be
positive.

```python
result = views.slide(3)([1, 2, 3, 4])
assert [list(window) for window in result] == [[1, 2, 3], [2, 3, 4]]
```

### `views.chunk_by(predicate)`

Starts a new chunk whenever `predicate(previous, current)` is false. Empty
input returns an empty `Range`.

```python
result = views.chunk_by(lambda a, b: b - a == 1)([1, 2, 4, 5, 8])
assert [list(chunk) for chunk in result] == [[1, 2], [4, 5], [8]]
```

### `views.stride(step)`

Selects every `step`-th value starting with the first. `step` must be positive.
Because the returned `Range` is eager, the finite input is consumed completely.

```python
assert list(views.stride(2)(range(6))) == [0, 2, 4]
```

## Nesting, splitting, and conversion

### `views.join()`

Flattens exactly one nesting level.

```python
assert list(views.join()([[1, 2], [3], [4, 5]])) == [1, 2, 3, 4, 5]
```

Strings and other iterable values are flattened according to normal Python
iteration rules.

### `views.join_with(separator)`

Flattens one nesting level and inserts the separator pattern between adjacent
sub-iterables. An empty separator is valid and behaves like `join()`.

```python
nested = [[1, 2], [3], [4, 5]]
assert list(views.join_with([0])(nested)) == [1, 2, 0, 3, 0, 4, 5]
```

### `views.split(separator)`

Splits whenever the complete separator pattern occurs. Empty leading, trailing,
or intermediate chunks are preserved. The input is materialized before
splitting.

```python
result = views.split([0, 0])([1, 2, 0, 0, 3, 0, 0])
assert [list(chunk) for chunk in result] == [[1, 2], [3], []]
```

An empty separator raises `ValueError` when the adaptor is applied.

### `views.to(target_type)`

Passes the current iterable to `target_type` and returns exactly what that
callable returns. This is commonly used to end a pipeline with a built-in
collection or a custom factory.

```python
assert views.to(tuple)([1, 2, 3]) == (1, 2, 3)
assert "abc" | views.to("".join) == "abc"
```

Unlike the other public adaptors, `to` does not promise a `Range` result and
does not impose its own materialization strategy beyond calling the target.

## Validation summary

| Operation | Invalid configuration |
| --- | --- |
| `counted` | `count < 0` |
| `adjacent` | `width < 1` |
| `adjacent_transform` | `width < 1` |
| `chunk` | `size < 1` |
| `slide` | `width < 1` |
| `stride` | `step < 1` |
| `split` | empty separator, checked when applied |

`take` and `drop` deliberately accept negative counts because they expose
Python slicing semantics. `join_with` deliberately accepts an empty separator.

## Type checking

The installed distribution includes a `py.typed` marker, so type checkers can
use the inline annotations. Public no-input-type factories such as `reverse`,
`take`, `enumerate`, `chunk`, and `join` preserve pipeline element types through
structural generic protocols.

Representative type expectations are checked in
`tests/typecheck/public_api.py` as part of CI.
