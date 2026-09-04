def caesar_cipher(text, shift):
    """
    Encrypts text using a Caesar cipher.
    Preserves spaces, punctuation, and letter casing.
    """
    result = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            else:
                alphabet = "abcdefghijklmnopqrstuvwxyz"

            index = alphabet.index(char)
            new_index = (index + shift) % 26
            result += alphabet[new_index]
        else:
            result += char

    return result


def caesar_decipher(ciphertext, shift):
    """
    Decrypts a Caesar cipher by shifting in the opposite direction.
    """
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """
    Counts the frequency of letters in the text.
    Ignores case and non-alphabetic characters.
    """
    frequency = {}

    for letter in "abcdefghijklmnopqrstuvwxyz":
        frequency[letter] = 0

    for char in text.lower():
        if char.isalpha():
            frequency[char] += 1

    return frequency


def display_frequency(freq):
    """Displays letter frequencies."""
    print("\nLetter Frequency:")
    for letter in sorted(freq.keys()):
        print(f"{letter}: {freq[letter]}")


def main():
    while True:
        print("\n===== Caesar Cipher Menu =====")
        print("1. Encrypt and Analyze Text")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("\nEnter a message: ")
            shift = int(input("Enter shift value: "))

            encrypted = caesar_cipher(message, shift)
            frequency = letter_frequency(message)
            decrypted = caesar_decipher(encrypted, shift)

            print("\nEncrypted Text:")
            print(encrypted)

            display_frequency(frequency)

            print("\nDecrypted Text:")
            print(decrypted)

        elif choice == "2":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()