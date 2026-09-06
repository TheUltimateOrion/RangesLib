from collections.abc import Iterable

from rangeslib import ranges, views


def is_even(value: int) -> bool:
    return value % 2 == 0


def times_ten(value: int) -> int:
    return value * 10


def join_strings(values: Iterable[str]) -> str:
    return "".join(values)


def main() -> None:
    cool_str: str = (
        "abcdefghijklmnopqrstuvwxyz"
        | views.take(5)
        | views.to(list)
        | views.to(join_strings)
    )
    numbers = (
        ranges.iota(1, 11)
        | views.filter(is_even)
        | views.transform(times_ten)
        | views.take(3)
        | views.to(list)
    )
    print(cool_str)
    print(numbers)


if __name__ == "__main__":
    main()
