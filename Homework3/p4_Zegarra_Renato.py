from testif import testif


def ed_read(filename: str, from_pos: int = 0, to_pos: int = -1) -> str:
    """Read part of a text file.

    filename is the name of an existing file.
    from_pos is the starting position.
    to_pos is the ending position, which is not included.
    If to_pos is -1, read to the end of the file.
    Raise IndexError if a position is outside the file.
    Return the requested text.
    """
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    if from_pos < 0 or from_pos > len(text):
        raise IndexError("Starting position is outside the file.")

    if to_pos != -1:
        if to_pos < from_pos or to_pos > len(text):
            raise IndexError("Ending position is outside the file.")
        return text[from_pos:to_pos]

    return text[from_pos:]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Find all positions of a string in a file.

    filename must be an existing text file.
    search_str must not be empty.
    Return a list of starting positions where the string occurs.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty.")

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    positions = []
    start = 0

    while True:
        index = text.find(search_str, start)

        if index == -1:
            break

        positions.append(index)
        start = index + 1

    return positions


def ed_replace(filename: str, search_str: str,
               replace_with: str, occurrence: int = -1) -> int:
    """Replace one or all occurrences of a string in a file.

    filename must be an existing text file.
    search_str must not be empty.
    occurrence must be -1 or a nonnegative integer.
    -1 replaces all matches, otherwise replace the selected match.
    Return the number of replacements made.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty.")

    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or greater.")

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    positions = ed_find(filename, search_str)

    if occurrence == -1:
        count = len(positions)
        if count == 0:
            return 0

        new_text = text.replace(search_str, replace_with)

    else:
        if occurrence >= len(positions):
            return 0

        index = positions[occurrence]
        new_text = (text[:index] + replace_with +
                    text[index + len(search_str):])
        count = 1

    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_text)

    return count


def ed_append(filename: str, string: str) -> int:
    """Append text to a file, creating the file if necessary.

    filename is the file to modify.
    string is the text to append.
    Return the number of characters written.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(string)

    return len(string)


def test_ed_find() -> None:
    """Test the ed_find function using testif."""
    filename = "test_find.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    testif(ed_find(filename, "345") == [3, 13],
           "Find multiple occurrences")

    testif(ed_find(filename, "356") == [],
           "Find string not present")

    testif(ed_find(filename, "012") == [0, 10],
           "Find string at beginning")

    testif(ed_find(filename, "789") == [7, 17],
           "Find string near end")


def test_ed_replace() -> None:
    """Test the ed_replace function using testif."""
    filename = "test_replace.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    count = ed_replace(filename, "345", "ABCDE", 1)

    testif(count == 1, "Replace one occurrence")
    testif(ed_read(filename) == "0123456789012ABCDE6789",
           "Check single replacement")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    count = ed_replace(filename, "345", "ABCDE")

    testif(count == 2, "Replace all occurrences")
    testif(ed_read(filename) == "012ABCDE6789012ABCDE6789",
           "Check all replacements")

    count = ed_replace(filename, "XYZ", "ABC")

    testif(count == 0, "Replace string not found")

    count = ed_replace(filename, "ABCDE", "XYZ", 5)

    testif(count == 0, "Replace occurrence out of range")


def main() -> None:
    """Demonstrate the file editor functions and run the tests."""
    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 4")
    print()

    filename = "file1.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("")

    print("File Editor Demonstration:")

    print("Characters appended:",
          ed_append(filename, "0123456789"))

    print("Characters appended:",
          ed_append(filename, "0123456789"))

    print("Read positions 3 to 9:", ed_read(filename, 3, 9))
    print("Read from position 3:", ed_read(filename, 3))

    print("Find '345':", ed_find(filename, "345"))
    print("Find '356':", ed_find(filename, "356"))

    print("Replace second occurrence:",
          ed_replace(filename, "345", "ABCDE", 1))

    print("File after replacement:", ed_read(filename))

    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    print("Replace all occurrences:",
          ed_replace(filename, "345", "ABCDE"))

    print("File after replacing all:", ed_read(filename))

    print()
    print("Testing ed_find:")
    test_ed_find()

    print()
    print("Testing ed_replace:")
    test_ed_replace()


if __name__ == "__main__":
    main()
