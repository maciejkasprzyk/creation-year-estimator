import json

import requests
from paths import *
from paths import books_info_path, authors_info_raw_path, authors_info_ready_path


def save_book_list():
    """
    Gets full list of books stored on wolnelektury.pl and saves into txt file
    :return: -
    """
    book_list = "https://wolnelektury.pl/api/books/"

    response_book_list = requests.get(book_list)

    data_book_list = response_book_list.text
    parsed_book_list = json.loads(data_book_list)
    url_list = [book["href"] for book in parsed_book_list]

    with open(books_urls_list_path, 'w') as file:
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
    Gets data for given number of books listed in file: url_list.txt and saves it in books_info.json file.
    When given count < 0 then function loads all books available
    :return: -
    """
    with open(books_urls_list_path, 'r') as file:
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

    with open(books_info_path, 'w') as file:
        json.dump(books_data, file)


def save_data_for_authors():
    authors_info = {}

    with open(books_info_path, 'r') as file:
        data = json.load(file)

    for i, book_raw_data in enumerate(data):
        author_name = book_raw_data["authors"][0]["name"]

        if author_name not in authors_info:
            author_url = book_raw_data["authors"][0]["href"]

            response_author_info = requests.get(author_url)
            data_author_info_json = response_author_info.text
            parsed_author_info = json.loads(data_author_info_json)

            authors_info[author_name] = parsed_author_info

        print(f'{author_name}')
        print(f"processed {i + 1} of {len(data)} books")

    with open(authors_info_raw_path, 'w') as file:
        json.dump(authors_info, file)


def save_texts():
    with open(books_info_path, 'r') as file:
        books_data = json.load(file)

    books_texts = {}

    for i, book in enumerate(books_data):
        title = book["title"]
        txt_url = book["txt"]

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
        print(f"downloaded {i + 1} of {len(books_data)} books")
        books_texts[title] = book_pure_txt

    with open(books_texts_path, 'w') as file:
        json.dump(books_texts, file)


def printout_books_info():
    with open(books_info_path, 'r') as file:
        data = json.load(file)

    for book in data:
        # print(book)
        print("-" * 30)
        print("Title:\t", book["title"])
        print("Author:\t", book["authors"][0]["name"])

    print(f"Printed info for:")
    print(f"{len(data)} books")


def printout_authors_info_raw():
    with open(authors_info_raw_path, 'r') as file:
        data = json.load(file)

    for author_name, author_info in data.items():
        description = author_info['description']
        print("-" * 100)
        print(author_name)
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


def printout_authors_info_ready():
    with open(authors_info_ready_path, 'r') as file:
        data = json.load(file)

    for author_name, author_info in data.items():
        birth_year = author_info["birth_year"]
        death_year = author_info["death_year"]

        print("-" * 100)
        print(author_info)
        print(author_name, birth_year, death_year)

    print(f"Printed info for:")
    print(f"{len(data)} authors")


def printout_text_samples():
    with open(books_texts_path, 'r') as file:
        data = json.load(file)

    for title, content in data.items():
        print(title)
        if content is None:
            print("Brak tekstu")
        else:
            print(content[:50])

