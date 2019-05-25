import json

from paths import *


def construct_list_of_books():
    """This function construct list of books from json files.
    By json files I means: file with books info, authors info and books texts"""

    with open(books_info_path, 'r') as file:
        books_data_raw = json.load(file)

    with open(authors_info_ready_path, 'r') as file:
        authors_data = json.load(file)

    with open(books_texts_path, 'r') as file:
        books_texts = json.load(file)

    books_list = []

    for i, book in enumerate(books_data_raw):
        title = book["title"]
        author = book["authors"][0]["name"]
        epoch = book["epochs"][0]["name"]
        kind = book["kinds"][0]["name"]
        genre = book["genres"][0]["name"]
        txt = books_texts[title]

        birth_year = authors_data[author]["birth_year"]
        death_year = authors_data[author]["death_year"]

        # done append when no text
        if txt is None:
            continue

        if birth_year is None and death_year is None:
            # print("There's no date for book", title)
            date = None
            continue  # dont append when no date
        elif birth_year is not None and death_year is not None:
            date = (birth_year + death_year) // 2
        elif birth_year is not None:
            date = birth_year + 25
        else:  # death_year is not None:
            date = death_year - 20

        books_list.append(Book(title, author, epoch, genre, kind, date, txt))

    return books_list


class Book:
    def __init__(self, title, author, epoch, genre, kind, date, text):
        self.title = title
        self.author = author
        self.epoch = epoch
        self.genre = genre
        self.kind = kind
        self.date = date
        self.text = text

    def __str__(self):
        result = ""
        result += "=" * 50 + "\n"
        result += self.title + "\n"
        result += self.author + "\n"
        result += self.epoch + "\n"
        result += self.genre + "\n"
        result += self.kind + "\n"
        result += str(self.date) + "\n"
        result += self.text[:100] + "\n"
        return result


def main():
    books = construct_list_of_books()
    for i in range(5):
        print(str(books[i]))


if __name__ == '__main__':
    main()
