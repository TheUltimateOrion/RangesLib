from __future__ import annotations

from collections.abc import Callable
from time import perf_counter

from rangeslib import ranges, views

Sample = Callable[[], object]


def measure(name: str, sample: Sample, iterations: int = 5) -> None:
    durations: list[float] = []
    for _ in range(iterations):
        start = perf_counter()
        sample()
        durations.append(perf_counter() - start)

    best = min(durations)
    average = sum(durations) / len(durations)
    print(f"{name:<32} best={best:.6f}s avg={average:.6f}s")


def main() -> None:
    size = 100_000
    values = list(range(size))
    nested = [range(100) for _ in range(1_000)]
    split_values = [item for value in range(10_000) for item in (value, -1)]

    measure("views.all list", lambda: values | views.all())
    measure(
        "filter + take",
        lambda: values | views.filter(lambda value: value % 2 == 0) | views.take(1_000),
    )
    measure(
        "composed pipeline",
        lambda: (
            values | (views.filter(lambda value: value % 2 == 0) | views.take(1_000))
        ),
    )
    measure("join nested ranges", lambda: nested | views.join())
    measure("split scalar delimiter", lambda: split_values | views.split(-1))
    measure("chunk", lambda: values | views.chunk(128))
    measure("slide", lambda: ranges.iota(0, 10_000) | views.slide(8))


if __name__ == "__main__":
    main()
