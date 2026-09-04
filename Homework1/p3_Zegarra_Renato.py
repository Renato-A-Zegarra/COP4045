def find_dup_str(s, n):
    """Find the first duplicated substring of length n."""
    for i in range(len(s) - n + 1):
        first = s[i:i + n]

        for j in range(i + n, len(s) - n + 1):
            second = s[j:j + n]

            if first == second:
                return first

    return ""


def find_max_dup(s):
    """Find the longest duplicated substring."""
    max_length = len(s) // 2

    for n in range(max_length, 0, -1):
        result = find_dup_str(s, n)

        if result != "":
            return result

    return ""


def main():
    s = input("Enter a string: ")
    n = int(input("Enter substring length: "))

    result = find_dup_str(s, n)
    print("Duplicated substring:", result)

    longest = find_max_dup(s)
    print("Longest duplicated substring:", longest)


if __name__ == "__main__":
    main()