from book import *
import csv


def main():
    books = construct_list_of_books()
    data = []

    for item in books:
        if not data.__contains__(item.epoch):
            data.append(item.epoch)
            print(item.epoch)




if __name__ == '__main__':
    main()
