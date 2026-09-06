# Roadmap

The eager `Range` design now has the major C++-inspired adaptor families the
project set out to explore. New work should usually start as an issue or design
note instead of immediately adding more adaptors.

## Near-term polish

- Keep README examples short and executable.
- Keep `docs/usage.md`, API docstrings, and type assertions synchronized.
- Add migration notes only when user code needs to change.
- Watch CI and GitHub Pages releases after each version bump.

## Good future issues

- Lazy view architecture: decide whether a future release should add lazy views
  alongside eager `Range` results.
- Typed adaptor composition: improve static inference for reusable pipelines
  such as `views.filter(predicate) | views.take(3)`.
- Performance profiling: use `scripts/benchmark.py` to compare split, slide,
  join, and repeated materialization changes.
- PyPI publishing: add trusted publishing once the public API has settled.
- C++ compatibility notes: document every intentionally different behavior as it
  is discovered.

## Not immediate priorities

- Adding every remaining C++ range customization point.
- Publishing to PyPI before the docs and release automation have had a few
  successful cycles.
- Expanding the package root namespace beyond `Range`, `ranges`, and `views`.

## Release direction

`0.5.x` should focus on documentation, correctness, and polish. A future `0.6.0`
would be a reasonable place for publishing automation or a larger architecture
experiment.
