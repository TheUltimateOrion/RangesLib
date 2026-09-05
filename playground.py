from rangeslib import ranges, views


def is_even(value: int) -> bool:
    return value % 2 == 0


def times_ten(value: int) -> int:
    return value * 10


def main() -> None:
    cool_str: str = (
        "abcdefghijklmnopqrstuvwxyz"
        | views.take(5)
        | views.to("".join)
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
