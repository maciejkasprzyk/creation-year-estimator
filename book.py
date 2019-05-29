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
        if epoch == "nie dotyczy":
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

    @property
    def label(self):

        epoch = self.epoch

        if epoch == "Starożytność" or epoch == "Średniowiecze":
            return "Starożytność lub średniowiecze"
        # elif epoch == "Średniowiecze":
        #     labels.append("Średniowiecze")
        elif epoch == "Pozytywizm":
            return "Pozytywizm"
        elif epoch == "Romantyzm":
            return "Romantyzm"
        elif epoch == "Modernizm":
            return "Modernizm"
        elif epoch == "Współczesność":
            return "Współczesność"
        elif epoch == "Oświecenie" or epoch == "OÅ›wiecenie":
            return "Oświecenie"
        elif epoch == "Dwudziestolecie międzywojenne" or epoch == "Dwudziestolecie miÄ™dzywojenne":
            return "Dwudziestolecie międzywojenne"
        elif epoch == "Renesans":
            return "Renesans"
        elif epoch == "Barok":
            return "Barok"
        elif epoch == "nie dotyczy":
            return "nie dotyczy"
        else:
            return "other"

    @property
    def label_date(self):
        date = self.date
        if date <= 1500:
            return "<1500"
        elif 1500 < date <= 1600:
            return "(1500; 1600]"
        elif 1600 < date <= 1700:
            return "(1600; 1700]"
        elif 1700 < date <= 1800:
            return "(1700; 1800]"
        elif 1800 < date <= 1900:
            return "(1800; 1900]"
        elif 1900 < date <= 2020:
            return "(1900; 2020]"
        else:
            return "other"


def main():
    books = construct_list_of_books()
    for book in books:
        if book.label == 'nie dotyczy' or book.label == "other":
            print(book.epoch, book.title)


if __name__ == '__main__':
    main()
