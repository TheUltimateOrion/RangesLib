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
- C++ compatibility notes: document every intentionally different behavior as it
  is discovered.

## Not immediate priorities

- Adding every remaining C++ range customization point.
- Expanding the package root namespace beyond `Range`, `ranges`, and `views`.

## Release direction

`0.6.x` should focus on publishing automation, release confidence, and polish. A
future minor release would be a reasonable place for a larger architecture
experiment such as lazy views.
