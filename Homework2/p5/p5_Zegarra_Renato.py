import datetime
import sys


def read_observations(filename):
    """Read station,date,temperature lines and return data and errors.

    Keep dates as strings, such as '09:28:09 AM 04/20/2026'.
    Line numbers start at 1.
    """
    observations = {}
    errors = []
    seen = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.strip().split(",")

            if len(parts) != 3:
                errors.append((line_number, "Expected station,date,temperature."))
                continue

            station, date_text, temperature_text = [part.strip() for part in parts]

            if not station:
                errors.append((line_number, "Station name cannot be empty."))
                continue

            try:
                datetime.datetime.strptime(date_text, "%I:%M:%S %p %m/%d/%Y")
            except ValueError:
                errors.append((line_number, "Invalid date; use HH:MM:SS AM/PM MM/DD/YYYY."))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "Temperature must be a number."))
                continue

            if not -100.0 <= temperature <= 150.0:
                errors.append((line_number, "Temperature must be between -100.0 and 150.0."))
                continue

            # Only valid observations count when checking for duplicates.
            key = (station, date_text)
            if key in seen:
                errors.append((line_number, "Duplicate station/date combination."))
                continue

            seen.add(key)
            if station not in observations:
                observations[station] = []
            observations[station].append((date_text, temperature))

    # Convert dates only for sorting; the tuples still contain strings.
    for station in observations:
        observations[station].sort(
            key=lambda observation: datetime.datetime.strptime(
                observation[0], "%I:%M:%S %p %m/%d/%Y"
            )
        )

    return observations, errors


def station_statistics(observations):
    """Return each station's (minimum, maximum, mean) temperature.

    Stations with no observations are skipped.
    """
    statistics = {}

    for station in observations:
        temperatures = []
        for date, temperature in observations[station]:
            temperatures.append(temperature)

        if not temperatures:
            continue

        minimum = min(temperatures)
        maximum = max(temperatures)
        mean = sum(temperatures) / len(temperatures)
        statistics[station] = (minimum, maximum, mean)

    return statistics


def station_outliers(observations):
    """Return (date, temperature, mean) for stations whose latest reading exceeds the mean."""
    statistics = station_statistics(observations)

    # [-1] selects the latest observation; [2] selects the mean.
    return {
        station: (
            observations[station][-1][0],
            observations[station][-1][1],
            statistics[station][2],
        )
        for station in statistics
        if observations[station][-1][1] > statistics[station][2]
    }


def write_statistics(filename, statistics):
    """Write station,minimum,maximum,mean lines in lexicographic station order."""
    with open(filename, "w", encoding="utf-8") as file:
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            file.write(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def main():
    """Read command-line filenames and run the weather station analyzer."""
    # sys.argv[0] is the program name; the next two items are filenames.
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input_file output_file")
        return 1

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except OSError as error:
        print(f"Could not read input file: {error}")
        return 1

    for line_number, message in errors:
        print(f"Line {line_number}: {message}")

    statistics = station_statistics(observations)
    outliers = station_outliers(observations)

    print("Statistics (station, minimum, maximum, mean):")
    for station in sorted(statistics):
        minimum, maximum, mean = statistics[station]
        print(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}")

    print("Outliers (station, date, temperature, mean):")
    for station in sorted(outliers):
        date, temperature, mean = outliers[station]
        print(f"{station},{date},{temperature:.1f},{mean:.1f}")

    try:
        write_statistics(output_filename, statistics)
    except OSError as error:
        print(f"Could not write output file: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
