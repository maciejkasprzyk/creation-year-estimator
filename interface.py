import pickle
from pprint import pprint

import sys

import paths


def main():
    file_name = sys.argv[1]

    try:
        with open(file_name, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("Nie ma takiego pliku lub niepoprawny plik")
        exit(-1)

    try:
        with open(paths.interface_gird_search_path, 'rb') as file:
            grid_search, x_test, y_test = pickle.load(file)
    except FileNotFoundError:
        print("Brak modelu do użycia na ścieżce: ", paths.interface_gird_search_path)
        exit(-1)

    classes = grid_search.classes_
    dec_func = grid_search.decision_function([text])[0]
    list = [(a, b) for a, b in zip(classes, dec_func)]
    pprint(list)
    # print(classes)
    # print(dec_func)

    predicted = grid_search.predict([text])
    print(predicted)


if __name__ == '__main__':
    main()
