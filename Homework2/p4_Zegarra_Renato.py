import csv


def read_rated(filename):
    """Read the top rated movies into a dictionary."""
    movies = {}

    infile = open(filename, "r", encoding="utf-8")
    reader = csv.reader(infile)
    next(reader)

    for row in reader:
        title = row[1]
        year = row[2]
        movies[(title, year)] = row[3]

    infile.close()

    return movies


def read_grossing(filename):
    """Read the top grossing movies into a dictionary."""
    movies = {}

    infile = open(filename, "r", encoding="utf-8")
    reader = csv.reader(infile)
    next(reader)

    for row in reader:
        title = row[1]
        year = row[2]
        money = int(row[3])

        movies[(title, year)] = money

    infile.close()

    return movies


def read_casts(filename):
    """Read movie directors and actors from the casts file."""
    movies = {}

    infile = open(filename, "r", encoding="utf-8")
    reader = csv.reader(infile)

    for row in reader:
        title = row[0]
        year = row[1]
        director = row[2]
        actors = row[3:]

        movies[(title, year)] = (director, actors)

    infile.close()

    return movies


def display_top_collaborations(rated, casts, limit=None):
    """Display directors and actors with the most collaborations."""
    collaborations = {}

    for movie in rated:
        if movie in casts:
            director = casts[movie][0]
            actors = casts[movie][1]

            for actor in actors:
                pair = (director, actor)

                if pair in collaborations:
                    collaborations[pair] += 1
                else:
                    collaborations[pair] = 1

    ranking = []

    for pair in collaborations:
        director = pair[0]
        actor = pair[1]
        count = collaborations[pair]

        ranking.append((count, director, actor))

    ranking.sort(reverse=True)

    if limit is not None:
        ranking = ranking[:limit]

    print("Top Director and Actor Collaborations:")

    for item in ranking:
        print(item[1], "-", item[2], "-", item[0])


def display_top_actors(grossing, casts, limit=None):
    """Display actors ranked by total box office money."""
    totals = {}

    for movie in grossing:
        if movie in casts:
            money = grossing[movie]
            actors = casts[movie][1]

            for actor in actors:
                if actor in totals:
                    totals[actor] += money
                else:
                    totals[actor] = money

    ranking = []

    for actor in totals:
        ranking.append((totals[actor], actor))

    ranking.sort(reverse=True)

    if limit is not None:
        ranking = ranking[:limit]

    print("Top Actors by Box Office:")

    for item in ranking:
        print(item[1], "-", item[0])


def main():
    rated = read_rated("imdb-top-rated.csv")
    grossing = read_grossing("imdb-top-grossing.csv")
    casts = read_casts("imdb-top-casts.csv")

    display_top_collaborations(rated, casts, 10)

    print()

    display_top_actors(grossing, casts, 10)


if __name__ == "__main__":
    main()