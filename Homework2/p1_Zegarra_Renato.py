def line_number(input_file: str, output_file: str) -> None:
    """Write numbered lines from one text file to another."""
    try:
        infile = open(input_file, "r")
        outfile = open(output_file, "w")

        number = 1

        for line in infile:
            outfile.write("{}. {}".format(number, line))
            number += 1

        infile.close()
        outfile.close()

    except Exception:
        print("Error reading or writing the file.")
        raise


def parse_functions(filename: str) -> tuple:
    """Parse functions from a Python file and return their information."""
    try:
        infile = open(filename, "r")
        lines = infile.readlines()
        infile.close()

        functions = []

        for i in range(len(lines)):
            line = lines[i]

            if line.startswith("def "):
                function_line = i + 1

                left_paren = line.find("(")
                right_paren = line.find(")")

                function_name = line[4:left_paren]
                arguments = line[left_paren + 1:right_paren]

                if "#" in line:
                    function_code = line[:line.find("#")].rstrip() + "\n"
                else:
                    function_code = line

                j = i + 1

                while j < len(lines):
                    current_line = lines[j]

                    if current_line.strip() != "":
                        if not current_line.startswith(" ") \
                                and not current_line.startswith("\t"):
                            break

                    if current_line.strip() != "":
                        if not current_line.strip().startswith("#"):
                            if "#" in current_line:
                                current_line = (
                                    current_line[:current_line.find("#")]
                                    .rstrip() + "\n"
                                )

                            if current_line.strip() != "":
                                function_code += current_line

                    j += 1

                functions.append(
                    (
                        function_line,
                        function_name,
                        arguments,
                        function_code
                    )
                )

        functions.sort(key=lambda item: item[1])

        return tuple(functions)

    except Exception:
        print("Error reading or parsing the Python file.")
        raise


def main() -> None:
    """Test line_number and parse_functions on this Python file."""
    input_file = __file__
    output_file = __file__ + ".txt"

    line_number(input_file, output_file)

    print("Numbered file created:")
    print(output_file)

    functions = parse_functions(input_file)

    print("\nParsed functions:")
    print(functions)


if __name__ == "__main__":
    main()