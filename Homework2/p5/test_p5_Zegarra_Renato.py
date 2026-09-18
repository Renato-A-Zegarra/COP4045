import tempfile
import unittest
from pathlib import Path

from p5.p5_Zegarra_Renato import (
    read_observations,
    station_statistics,
    station_outliers,
    write_statistics,
)


class TestWeatherStation(unittest.TestCase):
    def setUp(self):
        # Give each test its own folder and remove it after the test.
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.filename = Path(self.folder.name) / "weather.txt"
        self.earlier = "09:28:09 AM 04/20/2026"
        self.later = "09:28:09 AM 04/21/2026"

    def test_several_stations(self):
        self.filename.write_text(
            f"Miami,{self.earlier},80\n"
            f"Boston,{self.earlier},50\n"
            f"Denver,{self.earlier},40\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        self.assertEqual(observations, {
            "Miami": [(self.earlier, 80.0)],
            "Boston": [(self.earlier, 50.0)],
            "Denver": [(self.earlier, 40.0)],
        })
        self.assertEqual(errors, [])

    def test_negative_temperatures(self):
        self.filename.write_text(
            f"Denver,{self.earlier},-15.5\n"
            f"Denver,{self.later},-5.5\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        self.assertEqual(observations["Denver"], [
            (self.earlier, -15.5), (self.later, -5.5),
        ])
        self.assertEqual(errors, [])
        self.assertEqual(station_statistics(observations)["Denver"],
                         (-15.5, -5.5, -10.5))

    def test_duplicate_observations(self):
        self.filename.write_text(
            f"Miami,{self.earlier},80\n"
            f"Miami,{self.earlier},85\n"
            f"Boston,{self.earlier},50\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        self.assertEqual(observations, {
            "Miami": [(self.earlier, 80.0)],
            "Boston": [(self.earlier, 50.0)],
        })
        self.assertEqual(errors, [(2, "Duplicate station/date combination.")])

    def test_invalid_temperature_ranges(self):
        self.filename.write_text(
            f"TooCold,{self.earlier},-100.1\n"
            f"TooHot,{self.earlier},150.1\n"
            f"ColdLimit,{self.earlier},-100\n"
            f"HotLimit,{self.earlier},150\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        self.assertEqual(observations, {
            "ColdLimit": [(self.earlier, -100.0)],
            "HotLimit": [(self.earlier, 150.0)],
        })
        message = "Temperature must be between -100.0 and 150.0."
        self.assertEqual(errors, [(1, message), (2, message)])

    def test_calculated_statistics(self):
        observations = {
            "Miami": [(self.earlier, 10.0), (self.later, 21.0),
                      ("09:28:09 AM 04/22/2026", 30.0)],
            "Boston": [(self.earlier, 5.0)],
        }

        statistics = station_statistics(observations)

        self.assertEqual(statistics["Miami"][0], 10.0)
        self.assertEqual(statistics["Miami"][1], 30.0)
        # Approximate comparison is useful for a mean with repeating decimals.
        self.assertAlmostEqual(statistics["Miami"][2], 61.0 / 3)
        self.assertEqual(statistics["Boston"], (5.0, 5.0, 5.0))

    def test_observations_sorted_by_date(self):
        previous_year = "01:00:00 PM 12/31/2025"
        midnight = "12:00:00 AM 04/20/2026"
        noon = "12:00:00 PM 04/20/2026"
        self.filename.write_text(
            f"Miami,{noon},30\n"
            f"Miami,{self.earlier},20\n"
            f"Miami,{previous_year},5\n"
            f"Miami,{midnight},10\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        # The dates stay strings, but their order must be chronological.
        self.assertEqual(observations["Miami"], [
            (previous_year, 5.0), (midnight, 10.0),
            (self.earlier, 20.0), (noon, 30.0),
        ])
        self.assertEqual(errors, [])

    def test_sorted_output_and_one_decimal_place(self):
        statistics = {
            "Miami": (10, 30, 20.36),
            "Denver": (-15.5, -5.5, -10.5),
            "Boston": (0, 10, 5),
        }

        write_statistics(self.filename, statistics)

        self.assertEqual(self.filename.read_text(encoding="utf-8"),
                         "Boston,0.0,10.0,5.0\n"
                         "Denver,-15.5,-5.5,-10.5\n"
                         "Miami,10.0,30.0,20.4\n")

    def test_missing_file(self):
        # No file has been created at this path.
        with self.assertRaises(FileNotFoundError):
            read_observations(self.filename)

    def test_station_outliers(self):
        observations = {
            "Rising": [(self.earlier, 10.0), (self.later, 20.0)],
            "Falling": [(self.earlier, 20.0), (self.later, 10.0)],
            "Equal": [(self.earlier, 10.0), (self.later, 10.0)],
            "Single": [(self.earlier, 5.0)],
        }

        self.assertEqual(station_outliers(observations), {
            "Rising": (self.later, 20.0, 15.0),
        })

    def test_malformed_lines_and_invalid_values(self):
        self.filename.write_text(
            "missing fields\n"
            f"Miami,{self.earlier},warm\n"
            "Miami,09:28:09 AM 02/30/2026,20\n"
            f",{self.earlier},20\n"
            f"Miami,{self.earlier},80\n",
            encoding="utf-8",
        )

        observations, errors = read_observations(self.filename)

        self.assertEqual(observations, {"Miami": [(self.earlier, 80.0)]})
        self.assertEqual(errors, [
            (1, "Expected station,date,temperature."),
            (2, "Temperature must be a number."),
            (3, "Invalid date; use HH:MM:SS AM/PM MM/DD/YYYY."),
            (4, "Station name cannot be empty."),
        ])

    def test_empty_input(self):
        self.filename.write_text("", encoding="utf-8")

        self.assertEqual(read_observations(self.filename), ({}, []))
        self.assertEqual(station_statistics({}), {})
        self.assertEqual(station_outliers({}), {})
        write_statistics(self.filename, {})
        self.assertEqual(self.filename.read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
