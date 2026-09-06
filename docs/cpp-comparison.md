# C++ ranges comparison

`rangeslib` is inspired by modern C++ ranges, but it is designed for Python's
iterator and collection model. The goal is familiar naming and useful behavior,
not a direct port of C++ view machinery.

## Close conceptual matches

| C++ ranges idea | rangeslib API | Notes |
| --- | --- | --- |
| `views::all` | `iterable | views.all()` | Eagerly materializes a reusable `Range`. |
| `views::filter` | `views.filter(predicate)` | Keeps values for which the predicate is true. |
| `views::transform` | `views.transform(func)` | Maps each value through a callable. |
| `views::take` / `views::drop` | `views.take(count)` / `views.drop(count)` | Uses Python slice semantics, including negative counts. |
| `views::take_while` / `views::drop_while` | `views.take_while(predicate)` / `views.drop_while(predicate)` | Aliases also exist as `takewhile` and `dropwhile`. |
| `views::zip` | `views.zip(*others)` | Accepts any number of companion iterables and stops at the shortest input. |
| `views::cartesian_product` | `views.cartesian_product(other)` | Produces ordinary Python tuples. |
| `views::pairwise` | `views.pairwise()` | Produces `Range[tuple[T, T]]`. |
| `views::chunk` / `views::slide` | `views.chunk(size)` / `views.slide(width)` | Produces nested eager `Range` windows. |
| `views::join` / `views::join_with` | `views.join()` / `views.join_with(separator)` | Flattens one level. |
| `views::split` | `views.split(separator)` | Supports scalar delimiters and separator patterns. |

## Important differences

### Eager results

C++ views are usually lazy. `rangeslib` is currently eager: most operations
materialize and return a `Range` immediately. This keeps returned values simple
and reusable, but it means full-materialization operations should not be applied
directly to infinite iterables.

### Iterators and sentinels

C++ ranges expose iterator/sentinel concepts directly. Python exposes the
iterator protocol through `iter()` and `next()`, with `StopIteration` marking the
end. `rangeslib` follows Python here.

### References versus values

C++ views often yield references into underlying ranges. `rangeslib` stores the
values yielded by Python iteration. Mutating a mutable object contained in a
`Range` still mutates that object, but the `Range` itself is an eager container.

### Type system limits

Python type checkers can preserve many useful public types, including mixed
`zip`, `cartesian_product`, typed `keys` / `values`, and exact `pairwise` tuples.
They cannot express every C++ tuple-like constraint or variadic callable rule
with the same precision. `zip` and `cartesian_product` provide precise public
types for zero, one, and two companion iterables; larger runtime arities remain
supported but are typed less precisely.

### Naming

The public facade uses lowercase Python functions:

```python
from rangeslib import ranges, views
```

This preserves a C++-like vocabulary while staying natural for Python code.
