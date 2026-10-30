from testif import testif


class NVector:
    """Represent an N-dimensional vector using a list of numbers."""

    def __init__(self, *values: float) -> None:
        """Initialize a vector from a sequence or multiple numbers."""
        if len(values) == 1:
            self.elements = list(values[0])
        else:
            self.elements = list(values)

    def __len__(self) -> int:
        """Return the number of elements in the vector."""
        return len(self.elements)

    def __getitem__(self, index: int) -> float:
        """Return the element at the given index."""
        return self.elements[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Assign a value to the element at the given index."""
        self.elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string."""
        return str(self.elements)

    def __eq__(self, other: object) -> bool:
        """Return True if both vectors have equal elements."""
        if not isinstance(other, NVector):
            return False

        return self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Return True if the vectors are not equal."""
        return not self.__eq__(other)

    def __add__(self, other: object):
        """Add another vector or a number to this vector."""
        result = []

        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length.")

            for i in range(len(self)):
                result.append(self[i] + other[i])

        elif isinstance(other, (int, float)):
            for value in self.elements:
                result.append(value + other)

        else:
            return NotImplemented

        return NVector(result)

    def __radd__(self, other: object):
        """Add a number to this vector from the left."""
        return self.__add__(other)

    def __mul__(self, other: object):
        """Return the dot product or the sum of scalar products."""
        total = 0

        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length.")

            for i in range(len(self)):
                total += self[i] * other[i]

        elif isinstance(other, (int, float)):
            for value in self.elements:
                total += value * other

        else:
            return NotImplemented

        return total

    def __rmul__(self, other: object):
        """Multiply this vector by a number from the left."""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """Return a vector of length n containing only zeros."""
        if n < 0:
            raise ValueError("Vector length cannot be negative.")

        return cls([0] * n)


def main() -> None:
    """Test the NVector class methods."""
    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 1")
    print()

    v1 = NVector(3, 0, 1, -1)
    v2 = NVector([3, 0, 1, -1])
    v3 = NVector((1, 2, 3, 4))

    print("Vector 1:", v1)
    print("Vector 2:", v2)
    print("Vector 3:", v3)
    print()

    testif(v1 == v2, "Constructor with list")
    testif(v3 == NVector(1, 2, 3, 4), "Constructor with tuple")
    testif(len(v1) == 4, "Length")
    testif(v1[1] == 0, "Positive indexing")
    testif(v1[-2] == 1, "Negative indexing")

    v2[2] = 5
    testif(v2[2] == 5, "Indexed assignment")
    testif(v2[-1] == -1, "Negative indexing assignment")

    v2[-1] = 10
    testif(v2[-1] == 10, "Set negative index")

    testif(str(v1) == "[3, 0, 1, -1]", "String representation")
    testif(v1 != v2, "Not equal")
    testif(v1 == NVector(3, 0, 1, -1), "Equal")

    testif(
        v1 + v3 == NVector(4, 2, 4, 3),
        "Vector addition"
    )

    testif(
        v1 + 10 == NVector(13, 10, 11, 9),
        "Scalar addition"
    )

    testif(
        10 + v1 == NVector(13, 10, 11, 9),
        "Reflected addition"
    )

    testif(v1 * v3 == 2, "Vector multiplication")
    testif(v1 * 2 == 6, "Scalar multiplication")
    testif(2 * v1 == 6, "Reflected multiplication")

    testif(
        NVector.zeros(4) == NVector(0, 0, 0, 0),
        "Zeros class method"
    )

    original = [1, 2, 3]
    copied = NVector(original)
    original[0] = 10

    testif(copied[0] == 1, "Constructor copies the list")

    try:
        value = v1[10]
        testif(False, "Invalid index")
    except IndexError:
        testif(True, "Invalid index")

    try:
        result = v1 + NVector(1, 2)
        testif(False, "Different vector lengths")
    except ValueError:
        testif(True, "Different vector lengths")


if __name__ == "__main__":
    main()