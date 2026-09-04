import unittest
from p5_Zegarra_Renato import (
    caesar_cipher,
    caesar_decipher,
    letter_frequency
)

class TestCaesarCipher(unittest.TestCase):

    def test_cipher_lowercase(self):
        self.assertEqual(caesar_cipher("abc", 3), "def")

    def test_cipher_uppercase(self):
        self.assertEqual(caesar_cipher("XYZ", 3), "ABC")

    def test_cipher_with_spaces(self):
        self.assertEqual(
            caesar_cipher("Hello World", 3),
            "Khoor Zruog"
        )

    def test_decipher(self):
        encrypted = caesar_cipher("Python", 5)
        self.assertEqual(
            caesar_decipher(encrypted, 5),
            "Python"
        )

    def test_frequency_simple(self):
        expected = {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}
        expected["a"] = 2
        expected["b"] = 2
        expected["c"] = 2

        self.assertEqual(
            letter_frequency("aabbcc"),
            expected
        )

    def test_frequency_ignore_symbols(self):
        freq = letter_frequency("Hello!!!")

        self.assertEqual(freq["h"], 1)
        self.assertEqual(freq["e"], 1)
        self.assertEqual(freq["l"], 2)
        self.assertEqual(freq["o"], 1)


if __name__ == "__main__":
    unittest.main()