# COP 4045 - Homework 3, Problem 6
# Renato Zegarra

import unittest


class Entry:
    """An entry with a name and an optional parent entry."""

    def __init__(self, name, parent=None):
        self.name = name
        self._parent = parent

    def parent(self):
        """Return this entry's parent, or None for the root."""
        return self._parent

    def size(self):
        """Return zero by default; subclasses can define their own size."""
        return 0

    def absolute_path(self):
        """Recursively build the path starting at the root folder."""
        if self._parent is None:
            return self.name
        return self._parent.absolute_path().rstrip("/") + "/" + self.name


class File(Entry):
    """A file entry that stores the number of bytes it uses."""

    def __init__(self, name: str, parent: Entry | None, bytes_used: int) -> None:
        """Initialize the file, raising ValueError if its size is negative."""
        if bytes_used < 0:
            raise ValueError("File size cannot be negative.")
        super().__init__(name, parent)
        self._bytes_used: int = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by this file."""
        return self._bytes_used


class Folder(Entry):
    """A folder containing files and other folders."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an empty folder with an optional parent."""
        super().__init__(name, parent)
        self._contents: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add an entry and set its parent to this folder."""
        self._contents.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return a tuple containing this folder's entries."""
        return tuple(self._contents)

    def size(self) -> int:
        """Return total bytes used, including files inside subfolders."""
        total = 0
        for entry in self._contents:
            total += entry.size()
        return total


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Recursively find files whose size is at least minimum_size bytes."""
    matches: list[File] = []
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            matches.append(entry)
    elif isinstance(entry, Folder):
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
    return matches


class TestProblem6(unittest.TestCase):
    """Test absolute paths and recursive file searches."""

    def setUp(self) -> None:
        """Create a small folder tree for each test."""
        self.root = Folder("/")
        self.documents = Folder("documents")
        self.homework = Folder("homework")
        self.root.add(self.documents)
        self.documents.add(self.homework)

        self.small = File("small.txt", None, 50)
        self.large = File("large.txt", None, 500)
        self.exact = File("exact.txt", None, 100)
        self.nested = File("nested.txt", None, 300)
        self.root.add(self.small)
        self.root.add(self.large)
        self.documents.add(self.exact)
        self.homework.add(self.nested)

    def test_root_absolute_path(self) -> None:
        """The root folder's path is its name."""
        self.assertEqual(self.root.absolute_path(), "/")

    def test_nested_file_absolute_path(self) -> None:
        """A nested file's path includes every parent folder."""
        self.assertEqual(
            self.nested.absolute_path(), "/documents/homework/nested.txt"
        )

    def test_find_large_files_in_subfolders(self) -> None:
        """Search finds matching files at multiple folder levels."""
        self.assertCountEqual(
            find_large_files(self.root, 200), [self.large, self.nested]
        )

    def test_find_files_equal_to_minimum(self) -> None:
        """Files exactly equal to the minimum size are included."""
        self.assertCountEqual(
            find_large_files(self.root, 100),
            [self.large, self.exact, self.nested],
        )

    def test_no_files_meet_minimum(self) -> None:
        """Search returns an empty list when all files are too small."""
        self.assertEqual(find_large_files(self.root, 1000), [])


def display_structure(entry: Entry, level: int = 0) -> None:
    """Print the folder tree with indentation for each level."""
    indent = "    " * level
    if isinstance(entry, Folder):
        print(f"{indent}[Folder] {entry.name}")
        for child in entry.children():
            display_structure(child, level + 1)
    else:
        print(f"{indent}{entry.name} ({entry.size()} bytes)")


def main() -> None:
    """Demonstrate folder sizes, absolute paths, and recursive searches."""
    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 6")

    root = Folder("/")
    documents = Folder("documents")
    homework = Folder("homework")
    root.add(documents)
    documents.add(homework)

    readme = File("readme.txt", None, 50)
    notes = File("notes.txt", None, 100)
    report = File("report.pdf", None, 500)
    program = File("problem6.py", None, 300)
    data = File("data.csv", None, 1000)
    root.add(readme)
    documents.add(notes)
    documents.add(report)
    homework.add(program)
    homework.add(data)

    print("\nFolder structure:")
    display_structure(root)

    print("\nTotal folder sizes:")
    for folder in (root, documents, homework):
        print(f"{folder.absolute_path()}: {folder.size()} bytes")

    print("\nAbsolute file paths:")
    for file in (readme, report, program):
        print(file.absolute_path())

    for minimum_size in (100, 500):
        print(f"\nFiles at least {minimum_size} bytes:")
        for file in find_large_files(root, minimum_size):
            print(f"{file.absolute_path()} ({file.size()} bytes)")


if __name__ == "__main__":
    main()
