def main():
    # Part a
    result_a = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if a != b
        and a != c
        and a != d
        and b != c
        and b != d
        and c != d
        and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]

    print("Part a:")
    print(result_a)

    # Part b
    words = ["One", "SEVEN", "three", "two", "Ten"]

    result_b = [
        (word.lower(), len(word))
        for word in words
        if len(word) < 5
    ]

    print("\nPart b:")
    print(result_b)

    # Part c
    names = [
        "Christopher Ashton Kutcher",
        "Elizabeth Stamatina Fey"
    ]

    result_c = [
        name.split()[0] + " "
        + name.split()[1][0] + ". "
        + name.split()[2]
        for name in names
    ]

    print("\nPart c:")
    print(result_c)

    # Part d
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

    result_d = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]

    print("\nPart d:")
    print(result_d)

    # Part e
    s = ["one", "two", "three"]

    result_e = {
        word: len(word)
        for word in s
    }

    print("\nPart e:")
    print(result_e)

    # Part f
    text = "Hello world"

    result_f = {
        i: c
        for i, c in enumerate(text)
        if c.lower() in "aeiou"
    }

    print("\nPart f:")
    print(result_f)


if __name__ == "__main__":
    main()