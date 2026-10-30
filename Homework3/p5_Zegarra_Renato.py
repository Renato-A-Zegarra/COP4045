import turtle
from testif import testif


# Part A

def leaf_branch(level: int, length: float) -> None:
    """Draw smaller leaf branches recursively."""
    if level == 0:
        return

    turtle.forward(length)

    turtle.left(40)
    leaf_branch(level - 1, length * 0.65)
    turtle.right(40)

    turtle.right(40)
    leaf_branch(level - 1, length * 0.65)
    turtle.left(40)

    turtle.backward(length)

def draw_leaf_straight(level: int, petiole_length: float) -> None:
    """Draw a vertical leaf using recursive branches."""
    turtle.reset()
    turtle.speed(0)
    turtle.delay(0)
    turtle.hideturtle()
    turtle.pensize(2)

    turtle.penup()
    turtle.goto(0, -300)
    turtle.setheading(90)
    turtle.pendown()

    turtle.forward(petiole_length)

    for i in range(level):
        length = 65 * (1 - i / (level + 1))

        turtle.left(55)
        leaf_branch(level - i, length)
        turtle.right(55)

        turtle.right(55)
        leaf_branch(level - i, length)
        turtle.left(55)

        turtle.forward(35)


# Part B

def strB(n: int, base: int = 10) -> str:
    """Convert a nonnegative integer to a given base recursively."""
    if n < 0:
        raise ValueError("The number must be nonnegative.")

    if base < 2 or base > 26:
        raise ValueError("The base must be between 2 and 26.")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if n < base:
        return digits[n]

    return strB(n // base, base) + digits[n % base]


def test_strB() -> None:
    """Test the recursive base conversion function."""
    testif(strB(15, 2) == "1111", "Base 2 conversion")
    testif(strB(255, 16) == "FF", "Base 16 conversion")
    testif(strB(100, 10) == "100", "Base 10 conversion")
    testif(strB(0, 8) == "0", "Convert zero")


# Part C

memo = {}


def Cnk_m(n: int, k: int) -> int:
    """Calculate n choose k recursively using memoization."""
    if n < 0 or k < 0 or k > n:
        raise ValueError("Invalid values for n and k.")

    if k == 0 or k == n:
        return 1

    if (n, k) in memo:
        return memo[(n, k)]

    result = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    memo[(n, k)] = result

    return result


def test_Cnk_m() -> None:
    """Test the memoized binomial coefficient function."""
    testif(Cnk_m(5, 2) == 10, "C(5, 2)")
    testif(Cnk_m(6, 3) == 20, "C(6, 3)")
    testif(Cnk_m(10, 0) == 1, "C(10, 0)")
    testif(Cnk_m(10, 5) == 252, "C(10, 5)")


def run_Cnk() -> None:
    """Display several binomial coefficient calculations."""
    print("C(5, 2) =", Cnk_m(5, 2))
    print("C(10, 5) =", Cnk_m(10, 5))
    print("C(20, 10) =", Cnk_m(20, 10))
    print("C(30, 15) =", Cnk_m(30, 15))


# Part D

def make_pairs(seq1: list, seq2: list,
               result: list = None) -> list:
    """Create matching pairs recursively using an accumulator."""
    if result is None:
        result = []

    if len(seq1) == 0 or len(seq2) == 0:
        return result

    result.append((seq1[0], seq2[0]))

    return make_pairs(seq1[1:], seq2[1:], result)


def test_make_pairs() -> None:
    """Test the recursive make_pairs function."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) ==
           [(1, 4), (2, 5), (3, 6)], "Equal lengths")

    testif(make_pairs([1, 2, 3], [4, 5]) ==
           [(1, 4), (2, 5)], "Second list shorter")

    testif(make_pairs([1, 2], [4, 5, 6]) ==
           [(1, 4), (2, 5)], "First list shorter")

    testif(make_pairs([], [4, 5, 6]) == [],
           "First list empty")

    testif(make_pairs([1, 2, 3], []) == [],
           "Second list empty")


def main() -> None:
    """Run the recursion tests and draw the leaf."""
    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 5")
    print()

    print("Part B: strB Tests")
    test_strB()

    print()
    print("Part C: Cnk_m Tests")
    test_Cnk_m()

    print()
    print("Part D: make_pairs Tests")
    test_make_pairs()

    print()
    print("Binomial Coefficient Examples:")
    run_Cnk()

    print()
    print("Drawing leaf with level 6 and petiole length 120.")

    draw_leaf_straight(6, 120)
    turtle.done()


if __name__ == "__main__":
    main()
