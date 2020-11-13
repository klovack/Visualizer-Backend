""" A module to read the tours csv """

from os import path

from csv import DictReader


def get_tours_data():
    """ Return data read from tours.csv  """
    filepath = path.join(
        path.dirname(path.realpath(__file__)), 'tours.csv')

    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        list_of_rows = list(csv_reader)
        return list_of_rows


if __name__ == "__main__":
    tour_data = get_tours_data()
    print(tour_data[2])
