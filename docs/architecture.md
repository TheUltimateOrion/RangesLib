# Architecture

## Goals

`rangeslib` provides a small, typed, Pythonic range pipeline API inspired by
modern C++ ranges without attempting to reproduce C++ iterator and view
semantics exactly. The current design prioritizes:

- a small public facade,
- predictable eager results,
- compatibility with ordinary Python iterables,
- readable pipeline syntax,
- type information that survives common public operations,
- simple extension rules for maintainers.

Laziness, iterator/sentinel pairs, borrowed-range semantics, and C++
customization point objects are explicitly outside the current architecture.
`views.all` fills the role closest to C++ `views::all` by eagerly materializing
an existing Python iterable into a reusable `Range`.

## Package layout

```text
src/rangeslib/
├── __init__.py       Public package surface: Range, ranges, views
├── ranges.py         Lowercase generator facade
├── views.py          Lowercase adaptor facade and public typing protocols
├── _core.py          Range, RangeAdaptor, and RangeGenerator
├── _generators.py    Private source implementations
├── _adaptors.py      Private transformation implementations
└── py.typed           PEP 561 marker for downstream type checkers
```

The `src` layout prevents accidental imports from the repository root. Modules
beginning with `_` are implementation details. Application code should depend
only on `Range`, `ranges`, and `views`.

## Dependency direction

```text
__init__.py
   ├── ranges.py ───────> _generators.py ──┐
   └── views.py ────────> _adaptors.py ────┼──> _core.py
                                           └──> Range / base contracts
```

Private implementation modules do not depend on the public facade modules.
That direction keeps the facade replaceable and avoids circular imports.

## Public API boundary

The package root intentionally exports only:

```python
from rangeslib import Range, ranges, views
```

`ranges` exposes source factories and `views` exposes adaptor factories. The
private implementation classes are tested directly where useful, but they are
not part of the compatibility contract. Adding a new public source or adaptor
means adding it to the appropriate lowercase facade and that facade's
`__all__`, not exporting the implementation class from `rangeslib.__init__`.

## Data flow and pipeline dispatch

The conceptual data flow is:

```text
range source -> Range[T]
Iterable[T] -> adaptor -> Range[U]
Range[T] | adaptor -> Range[U]
ordinary Iterable[T] | adaptor -> Range[U]
Iterable[T] -> views.to(factory) -> factory-defined result
```

`RangeAdaptor.__ror__` enables built-in iterables such as `list`, `str`, and
built-in `range` to start a pipeline. `Range.__or__` invokes the callable on
the right side and preserves the result type supplied by that callable.

For example:

```python
from rangeslib import ranges, views

result = ranges.iota(1, 5) | views.transform(str) | views.to(tuple)
```

The dispatch sequence is:

1. `ranges.iota` constructs `Range[int]`.
2. `Range.__or__` calls the transform adaptor.
3. `Transform` materializes `Range[str]`.
4. `Range.__or__` calls `To`.
5. `To` delegates to `tuple` and returns `tuple[str, ...]`.

## Range invariants

`Range[T]` is a mutable `collections.UserList` subclass with positional
construction:

```python
Range(1, 2, 3)  # three integer elements
Range([1, 2, 3])  # one list element
```

The positional constructor is an intentional API choice. Because `UserList`
reconstructs subclasses internally for several operations, `Range` explicitly
implements those reconstruction operations so the positional constructor does
not turn results into nested single elements.

The following operations preserve `Range` and element order:

- slicing, including stepped and reverse slices,
- left and right concatenation with compatible iterables,
- multiplication and reverse multiplication,
- shallow copying.

`Range.copy()` and `copy.copy(range_value)` copy the outer container but do not
deep-copy contained objects.

## Eager execution and iterator consumption

Most adaptors return a fully materialized `Range`. `views.to` is the exception:
it delegates result construction and consumption behavior to the supplied
callable.

Eager output does not require every adaptor to consume its input in the same
way. The important contracts are:

| Category | Examples | One-shot iterator behavior |
| --- | --- | --- |
| Bounded prefix | positive `take`, `counted` | consumes only the selected prefix |
| Early stopping | `takewhile` | stops at first failing value; that failing value has been consumed |
| Full materialization | `reverse`, `filter`, `transform`, `drop`, `chunk`, `slide`, `split` | consumes the finite input before returning |
| Shortest-input combination | `zip`, `zip_transform` | stops when one participating iterable ends |
| Target-defined | `to` | depends on the target callable |

Negative `take` deliberately follows Python slice-stop semantics, equivalent to
`list(iterable)[:count]`, so the complete input must be known first. `drop`
likewise materializes the full input because its semantics are implemented as a
Python slice.

### Infinite iterables

The library is not a lazy ranges framework. Only operations that can terminate
without exhausting their input are appropriate for infinite iterables. For
example, positive `take` and `counted` can bound `itertools.count()`, while
`reverse`, `filter`, `transform`, `drop`, `stride`, and grouping operations do
not return when applied directly to an unbounded iterable.

Pipeline order therefore matters:

```python
import itertools
from rangeslib import views

finite = itertools.count() | views.take(5) | views.transform(str)
```

The bounded operation must appear before an adaptor that requires complete
materialization.

## Validation and edge-case policy

Validation is adaptor-specific rather than governed by a blanket "all negative
sizes are invalid" rule.

The public contract is:

- `counted(count)` requires `count >= 0`.
- `adjacent(width)`, `adjacent_transform(..., width)`, `chunk(size)`,
  `slide(width)`, and `stride(step)` require a positive integer.
- `split(separator)` rejects an empty separator when the adaptor is applied.
- `take(count)` and `drop(count)` intentionally accept negative values and use
  Python slicing semantics.
- `repeat(value, count)` and `indices(count)` follow built-in list/range behavior,
  so non-positive counts produce empty results.
- `join_with([])` is valid and is equivalent to flattening with no inserted
  values.

These behaviors are public compatibility contracts and must be covered by
public-facade tests.

## Typing architecture

The distribution contains `py.typed`, so type checkers may consume inline
annotations under PEP 561. The code uses Python 3.12 type-parameter syntax.

Factories whose input type is inferable from an argument, such as `filter`,
`transform`, `chunk_by`, `join_with`, and `split`, return their concrete typed
adaptor classes. Factories such as `reverse`, `take`, `counted`, `enumerate`,
`adjacent`, `chunk`, and `join` do not receive the pipeline element type as a
factory argument. Their public signatures therefore use private structural
protocols with generic call methods so the input type can be inferred when the
adaptor is actually called or piped.

Some projection and variadic callable operations necessarily use `Any` where a
single Python signature cannot express dynamic tuple indexing or arbitrary
callable arity precisely. Those uses should stay localized to the facade and
implementation that require them.

Static type checking is part of CI. `tests/typecheck/public_api.py` contains
representative `assert_type` checks for the public API.

## Error philosophy

The library raises ordinary Python exceptions rather than wrapping them in a
library-specific hierarchy. Configuration that is unambiguously invalid is
validated by the relevant adaptor. Errors produced by user callables,
indexing, target factories, or incompatible values propagate naturally.

A new adaptor should not silently normalize invalid configuration unless that
normalization directly mirrors a well-known Python operation and is documented
as part of the public contract.

## Extending the library

A new source should:

1. be implemented in `_generators.py`,
2. return `Range` directly,
3. be exposed as a lowercase factory in `ranges.py`,
4. have public-facade behavior tests,
5. document validation and edge cases.

A new adaptor should:

1. subclass `RangeAdaptor` in `_adaptors.py`,
2. document input shape, output shape, materialization, and validation,
3. be exposed through a lowercase factory in `views.py`,
4. preserve useful public typing through a concrete generic return type or a
   structural protocol,
5. have both implementation tests where useful and public-facade contract tests,
6. be added to the usage/API documentation.

Do not expand the package-root namespace simply to expose a new implementation
class.

## Compatibility policy

During the `0.x` series, public API changes may still occur. Nevertheless:

- changes to `Range`, `ranges`, or `views` should be documented in the
  changelog,
- breaking public changes should include migration guidance,
- private modules beginning with `_` may change without migration support,
- observable iterator-consumption behavior should be treated as part of the
  public contract when users can reasonably depend on it.

## Testing strategy

The test suite has three complementary layers:

1. implementation tests for private generator/adaptor mechanics,
2. public-facade tests that exercise the API applications actually import,
3. collection-contract tests for `Range` behavior inherited from `UserList`.

Coverage is enforced as a guardrail, not as a substitute for behavioral
contracts. CI also runs static typing, linting, documentation builds, package
builds, and an installed-wheel smoke test.

Developer automation lives in `scripts/`. `scripts/format.sh` is intentionally
a local-only mutating command, while `scripts/check_all.sh`,
`scripts/run_tests.sh`, `scripts/check_package.sh`, and
`scripts/generate_docs.sh` are invoked directly by GitHub Actions. Keeping
executable policy in repository scripts prevents local and CI commands from
drifting. Documentation deployment is triggered only after the complete CI
workflow succeeds on `main`, and it builds the exact commit SHA that passed CI.

## C++ correspondence

Names and broad behavior are inspired by C++20, C++23, and C++26 ranges where
useful, but Python conventions take priority:

- Python iterables replace iterator/sentinel pairs.
- `Range` is an eager list-backed result rather than a general-purpose lazy
  view.
- tuples replace C++ reference tuples.
- normal Python callables replace customization point objects.
- validation follows each Python-facing operation rather than attempting to
  duplicate C++ concepts or constraints.
