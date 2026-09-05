from rangeslib import Filter, Iota, Take, To, Transform


def is_even(value: int) -> bool:
    return value % 2 == 0


def times_ten(value: int) -> int:
    return value * 10


def main() -> None:
    result: list[int] = (
        Iota(1, 11)
        | Filter(is_even)
        | Transform(times_ten)
        | Take(3)
        | To[int, list[int]](list)
    )

    print(result)


if __name__ == "__main__":
    main()
