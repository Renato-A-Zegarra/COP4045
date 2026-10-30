class ParkingPermit:
    """Represent a university parking permit."""

    def __init__(self, owner: str, months: int, fees: dict) -> None:
        """Initialize the owner, number of months, and fee schedule."""
        self.owner = owner
        self.months = months
        self.fees = fees

    def cost(self) -> float:
        """Return the cost of the parking permit."""
        return 0.0

    def __str__(self) -> str:
        """Return a string describing the permit."""
        return "Owner: {}, Months: {}".format(self.owner, self.months)

    def __repr__(self) -> str:
        """Return the string representation of the permit."""
        return self.__str__()


class StudentPermit(ParkingPermit):
    """Represent a student parking permit."""

    def __init__(self, owner: str, months: int, fees: dict,
                 vehicles: int) -> None:
        """Initialize a student permit and its registered vehicles."""
        super().__init__(owner, months, fees)
        self.vehicles = vehicles

    def cost(self) -> float:
        """Calculate the student permit cost using the fee schedule."""
        monthly_cost = self.fees["student_monthly"] * self.months

        extra_vehicles = self.vehicles - 1
        if extra_vehicles < 0:
            extra_vehicles = 0

        extra_cost = extra_vehicles * self.fees["extra_vehicle"]
        return monthly_cost + extra_cost

    def __str__(self) -> str:
        """Return the student permit information."""
        return "Student Permit - {}, Vehicles: {}, Cost: ${:.2f}".format(
            super().__str__(), self.vehicles, self.cost()
        )

    def __repr__(self) -> str:
        """Return the student permit representation."""
        return self.__str__()


class FacultyPermit(ParkingPermit):
    """Represent a faculty parking permit."""

    def __init__(self, owner: str, months: int, fees: dict,
                 garage: bool) -> None:
        """Initialize a faculty permit and garage access."""
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Calculate the faculty permit cost using the fee schedule."""
        total = self.fees["faculty_monthly"] * self.months

        if self.garage:
            total += self.fees["garage_monthly"] * self.months

        return total

    def __str__(self) -> str:
        """Return the faculty permit information."""
        return "Faculty Permit - {}, Garage: {}, Cost: ${:.2f}".format(
            super().__str__(), self.garage, self.cost()
        )

    def __repr__(self) -> str:
        """Return the faculty permit representation."""
        return self.__str__()


def summarize_list(permits: list) -> float:
    """Print each permit owner and cost, then return total revenue."""
    total = 0.0

    for permit in permits:
        print("{} - ${:.2f}".format(permit.owner, permit.cost()))
        total += permit.cost()

    return total


def main() -> None:
    """Create permits and demonstrate the classes and calculations."""
    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 2")
    print()

    fees = {
        "student_monthly": 25.0,
        "extra_vehicle": 10.0,
        "faculty_monthly": 40.0,
        "garage_monthly": 15.0
    }

    student1 = StudentPermit("Renato Zegarra", 4, fees, 2)
    student2 = StudentPermit("Maria Lopez", 3, fees, 1)
    faculty1 = FacultyPermit("John Smith", 6, fees, True)
    faculty2 = FacultyPermit("Sarah Brown", 2, fees, False)

    print("Parking Permit Objects:")
    print(student1)
    print(student2)
    print(faculty1)
    print(faculty2)
    print()

    print("Permit Representations:")
    print(repr(student1))
    print(repr(faculty1))
    print()

    permits = [student1, student2, faculty1, faculty2]

    print("Permit Summary:")
    total_revenue = summarize_list(permits)

    print()
    print("Total Revenue: ${:.2f}".format(total_revenue))


if __name__ == "__main__":
    main()
