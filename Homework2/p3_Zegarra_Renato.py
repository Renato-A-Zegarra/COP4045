import csv


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a new user to the social network."""
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception:
        print("Error adding user to the social network.")
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friend link between two users."""
    try:
        if user1 not in sn or user2 not in sn:
            return False

        if user1 == user2:
            return False

        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)

        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True

    except Exception:
        print("Error adding friend to the social network.")
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return friends of a user up to the given link distance."""
    try:
        if user1 not in sn or distance <= 0:
            return []

        friends = []
        current = [user1]
        visited = [user1]

        for i in range(distance):
            next_users = []

            for user in current:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.append(friend)
                        friends.append(friend)
                        next_users.append(friend)

            current = next_users

        return friends

    except Exception:
        print("Error finding friends in the social network.")
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save a social network dictionary to a CSV file."""
    try:
        outfile = open(filename, "w", newline="", encoding="utf-8")
        writer = csv.writer(outfile)

        for username in sn:
            fullname = sn[username][0]
            friends = sn[username][1]

            row = [username, fullname]

            for friend in friends:
                row.append(friend)

            writer.writerow(row)

        outfile.close()

    except Exception:
        print("Error saving the social network.")
        raise


def load_network(filename: str) -> dict:
    """Load a social network dictionary from a CSV file."""
    try:
        sn = {}

        infile = open(filename, "r", encoding="utf-8")
        reader = csv.reader(infile)

        for row in reader:
            username = row[0]
            fullname = row[1]
            friends = row[2:]

            sn[username] = (fullname, friends)

        infile.close()

        return sn

    except Exception:
        print("Error loading the social network.")
        raise


def main() -> None:
    """Test the social network functions."""
    try:
        sn = {}

        print("Adding users:")
        print(add_user(sn, "alice", "Alice Smith"))
        print(add_user(sn, "maria", "Maria Cortez"))
        print(add_user(sn, "joe", "Joseph Adams"))
        print(add_user(sn, "eve", "Evelyn Cooper"))
        print(add_user(sn, "david", "David Benson"))

        print("\nAdding alice again:")
        print(add_user(sn, "alice", "Alice Smith"))

        print("\nAdding friends:")
        print(add_friend(sn, "alice", "maria"))
        print(add_friend(sn, "maria", "joe"))
        print(add_friend(sn, "joe", "eve"))
        print(add_friend(sn, "maria", "david"))

        print("\nSocial network:")
        print(sn)

        print("\nAlice's friends at distance 1:")
        print(get_friends(sn, "alice", 1))

        print("\nAlice's friends at distance 2:")
        print(get_friends(sn, "alice", 2))

        print("\nAlice's friends at distance 3:")
        print(get_friends(sn, "alice", 3))

        print("\nWrong username:")
        print(get_friends(sn, "bob", 2))

        save_network("social_network.csv", sn)

        print("\nNetwork saved to social_network.csv")

        loaded_network = load_network("social_network.csv")

        print("\nLoaded network:")
        print(loaded_network)

    except Exception:
        print("An error occurred while testing the program.")
        raise


if __name__ == "__main__":
    main()