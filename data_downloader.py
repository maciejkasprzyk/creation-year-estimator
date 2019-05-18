import json
import re
import time

import requests


def save_book_list():
    """
    Gets full list of books stored on wolnelektury.pl and saves into txt file
    :return: -
    """
    book_list = "https://wolnelektury.pl/api/books/"

    response_book_list = requests.get(book_list)

    # get json with general info about all books
    data_book_list = response_book_list.text
    # parse json to python object
    parsed_book_list = json.loads(data_book_list)
    # all we need is book href
    url_list = [book["href"] for book in parsed_book_list]

    with open('url_list.txt', 'w') as file:
        for url in url_list:
            file.write("%s\n" % url)


def get_info_for_book(book_url):
    """
    Function get data for given book from wolnelektury.pl
    :param book_url: Link to certain book via API on website: wolnelektury.pl
    :return: scrapped data in dictionary structure
    """

    response_book_info = requests.get(book_url)
    data_book_info = response_book_info.text
    parsed_book_info = json.loads(data_book_info)

    return parsed_book_info


def save_data_for_books(book_count=-1):
    """
    Gets data for given number of books listed in file: url_list.txt and saves it in books_info_raw.json file.
    When given count < 0 then function loads all books available
    Function does not load data for books without txt
    :return: -
    """
    with open('url_list.txt', 'r') as file:
        book_list = file.readlines()

    books_data = []

    if book_count == 0:
        return
    elif book_count < 0:
        book_count = len(book_list)

    for i, url in enumerate(book_list):

        if not i < book_count:
            break
        book_data = get_info_for_book(url)
        books_data.append(book_data)
        print(f'{book_data["title"]}')
        print(f"downloaded {i + 1} of {book_count} books")

    with open('books_info_raw.json', 'w') as file:
        json.dump(books_data, file)


def printout_books_info_raw():
    """
        Prints saved data from books_info_raw.json file
        :return: -
        """

    with open('books_info_raw.json', 'r') as file:
        data = json.load(file)

    for book in data:
        # print(book)
        print("-" * 30)
        print("Title:\t", book["title"])
        print("Author:\t", book["authors"][0]["name"])


def save_data_for_authors():
    authors_info = {}

    with open('books_info_raw.json', 'r') as file:
        data = json.load(file)

    for i, book_raw_data in enumerate(data):
        author_name = book_raw_data["authors"][0]["name"]

        if author_name not in authors_info:
            author_url = book_raw_data["authors"][0]["href"]

            response_author_info = requests.get(author_url)
            data_author_info_json = response_author_info.text
            parsed_author_info = json.loads(data_author_info_json)

            author_description = parsed_author_info["description"]

            authors_info[author_name] = author_description

        print(f'{author_name}')
        print(f"processed {i + 1} of {len(data)} books")

    with open('authors_raw_info.json', 'w') as file:
        json.dump(authors_info, file)


def printout_authors_info_raw():
    """
        Prints saved data from books_info_raw.json file
        :return: -
        """

    with open('authors_raw_info.json', 'r') as file:
        data = json.load(file)

    for author, description in data.items():
        print("-" * 100)
        print(author)
        description_without_blank_lines = "".join([s for s in description.strip().splitlines(True) if s.strip()])
        description_lines = description_without_blank_lines.splitlines()
        if 0 < len(description_lines):
            print(description_lines[0])
        if 1 < len(description_lines):
            print(description_lines[1])
        if 2 < len(description_lines):
            print(description_lines[2])

    print(f"Printed info for:")
    print(f"{len(data)} authors")


def scrap_authors_info_to_txt_file():
    with open('authors_raw_info.json', 'r') as file:
        data = json.load(file)

    # i = 0
    authors_dates = []
    for author, description in data.items():
        birth_year = None
        death_year = None
        by = None
        dy = None
        pne = None

        description_without_blank_lines = "".join([s for s in description.strip().splitlines(True) if s.strip()])
        description_lines = description_without_blank_lines.splitlines()
        # look for birth year
        if 0 < len(description_lines):
            by = re.search(r"[Uu]r.*?(\d{3,})", description_lines[0])
        if by is not None:
            birth_year = int(by.group(1))
        # look for death year
        if 1 < len(description_lines):
            dy = re.search(r"[Zz]m.*?(\d{3,})", description_lines[1])
        if dy is not None:
            death_year = int(dy.group(1))

        if 0 < len(description_lines):
            pne = re.search(r"p[.]n[.]e", description_lines[0])

        # print("-" * 30)
        # print(i, author)
        # if 0 < len(description_lines):
        #     print(description_lines[0])
        # if 1 < len(description_lines):
        #     print(description_lines[1])
        if birth_year is not None:
            if pne is not None:
                birth_year = -birth_year
            # print(birth_year)
        if death_year is not None:
            if pne is not None:
                death_year = -death_year
            # print(death_year)
        # i += 1
        authors_dates.append((author, birth_year, death_year))

        with open('authors_dates.txt', 'w') as file:
            for author, birth, death in authors_dates:
                author = author.replace(" ", "_")
                s = author + " " + str(birth) + " " + str(death) + "\n"
                file.write(s)


def download_text_and_parse():
    with open('books_info_raw.json', 'r') as file:
        books_data_raw = json.load(file)

    with open('authors_dates_completed.txt', 'r') as file:
        lines = file.readlines()

    authors = {}

    for line in lines:
        words = line.split(" ")
        author_name = words[0]
        birth_date = words[1]
        death_date = words[2]
        authors[author_name] = (birth_date, death_date)

    books_data_final = []

    for i, book in enumerate(books_data_raw):
        title = book["title"]
        author = book["authors"][0]["name"]
        epoch = book["epochs"][0]["name"]
        kind = book["kinds"][0]["name"]
        txt_url = book["txt"]

        birth_date, death_date = authors[author.replace(" ", "_")]

        book_pure_txt = None
        if txt_url is not None and txt_url != '':
            response_txt = requests.get(txt_url)
            data_txt = response_txt.text
            footer_sign = "-----"
            footer_position = data_txt.find(footer_sign)

            if footer_position != -1:
                book_without_footer = data_txt[:footer_position]
            else:
                book_without_footer = data_txt
            header_sign = "ISBN"
            header_last_position = book_without_footer.find(header_sign)
            isbn_length = 4 + 1 + 13 + 4 + 1

            if header_last_position != -1:
                book_pure_txt = book_without_footer[header_last_position + isbn_length:].strip()
            else:
                book_pure_txt = book_without_footer.strip()

            print(title)
            print(f"downloaded {i + 1} of {len(books_data_raw)} books")

            book_dict = {
                "title": title,
                "kind": kind,
                "epoch": epoch,
                "author": author,
                "birth_date": birth_date,
                "death_date": death_date,
                "txt": book_pure_txt
            }
            books_data_final.append(book_dict)

    with open('data.json', 'w') as file:
        json.dump(books_data_final, file)

def read_saved_data():
    """
    Reads (printout) saved data from data.json file
    :return: -
    """

    with open('data.json', 'r') as file:
        data = json.load(file)

    counter = 0
    for book in data:
        print("\n\n", "-" * 30)
        print("Title:\t", book["title"])
        print("Kind:\t", book["kind"])
        print("Epoch:\t", book["epoch"])
        print("Author:\t", book["author"])
        print("Born:\t", book["birth_date"])
        print("Died:\t", book["death_date"])
        print("Txt fragment:\n", book["txt"][:100])
        if book["birth_date"] == "None" and book["death_date"] == "None":
            counter += 1
    print("Number of books without any year:", counter)


def main():
    print("What do you want to do?")
    print("l to download list of books")
    print("b to download books info")
    print("a to download authors info")
    print("sa to scrap authors birth and death dates")
    print(
        "t to download books texts and transform data into final format(it requires books and author info)")
    print("pa to print authors descriptions")
    print("read to read processed data")
    choice = input("Your choice: ").strip()

    if choice == "l":
        print("Do you really want to start the download?")
        answer = input(" [Y/n]: ")

        if answer == "Y":
            save_book_list()
    elif choice == "b":

        how_many_books = int(input("How many books do you want to download? (type -1 for all): "))

        print("Do you really want to start the download?")
        answer = input(" [Y/n]: ")

        if answer == "Y":
            start = time.time()
            save_data_for_books(how_many_books)
            end = time.time()
            print("\n", end - start)

        printout_books_info_raw()
    elif choice == "a":
        print("Do you really want to start the download?")
        answer = input(" [Y/n]: ")

        if answer == "Y":
            start = time.time()
            save_data_for_authors()
            end = time.time()
            print("\n", end - start)
    elif choice == "t":
        download_text_and_parse()
    elif choice == 'pa':
        printout_authors_info_raw()
    elif choice == 'sa':
        scrap_authors_info_to_txt_file()
    elif choice == 'print':
        read_saved_data()
    else:
        print("incorrect choice")


if __name__ == '__main__':
    main()
