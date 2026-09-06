# Migration guide

## From 0.6.x to 0.7.0

`Range.__str__()` now uses normal list formatting. String elements are quoted,
matching the representation users get from a regular Python list:

```python
from rangeslib import Range

assert str(Range("a", "b")) == "['a', 'b']"
```

Code that relies on the previous unquoted display should use an explicit string
conversion or formatting expression when it needs output without quotes.

## From 0.3.0 to 0.3.1

0.3.1 is primarily a correctness, typing, documentation, and quality-gate
release. No existing public factory has been removed.

### `Range` collection operations

Slicing, concatenation, multiplication, and `Range.copy()` now return the
expected flat `Range` instead of nesting the reconstructed sequence as one
element.

```python
from rangeslib import Range

values = Range(1, 2, 3)

assert list(values[1:]) == [2, 3]
assert list(values + [4]) == [1, 2, 3, 4]
assert list(values * 2) == [1, 2, 3, 1, 2, 3]
assert list(values.copy()) == [1, 2, 3]
```

Code that accidentally depended on the 0.3.0 nested results should be updated
to use the corrected list-like behavior.

### `take` iterator consumption

For non-negative counts, `views.take(count)` now consumes only the requested
prefix. This makes it usable as a bound for one-shot and infinite iterators.
Returned values are unchanged for finite inputs.

Negative counts still follow `list(iterable)[:count]` semantics and therefore
materialize the complete input.

### `single` typing

`ranges.single` now preserves the type of any value instead of being annotated
as integer-only. Runtime behavior for integers is unchanged.

## From 0.2.x to 0.3.x

0.3 introduced the lowercase public facade. Application code should import:

```python
from rangeslib import Range, ranges, views
```

Use source factories such as `ranges.iota(...)` and adaptor factories such as
`views.filter(...)`. Implementation classes in modules beginning with `_` are
private and should not be used as an application-facing API.

The package-root namespace intentionally no longer re-exports implementation
classes such as `Iota`, `Take`, or `Filter`.
