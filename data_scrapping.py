import requests
import json
import time
from date_parser_pl import *


# url = "https://wolnelektury.pl/api/books/studnia-i-wahadlo/"
# url = "https://wolnelektury.pl/api/books/pan-tadeusz/"
# url = "https://wolnelektury.pl/api/books/a-co-wam-spiewac/"     # TODO lyric need to be treated differently than epic


def get_data_for_book_url(book_url):
    """
    Function get data for given book from wolnelektury.pl
    :param book_url: Link to certain book via API on website: wolnelektury.pl
    :return: scrapped data in dictionary structure
    """

    # ================== info scrapping =====================

    response_book_info = requests.get(book_url)
    data_book_info = response_book_info.text
    parsed_book_info = json.loads(data_book_info)

    # print(json.dumps(parsed_book_info, indent=4))

    title = parsed_book_info["title"]
    author = parsed_book_info["authors"][0]["name"]
    epoch = parsed_book_info["epochs"][0]["name"]
    kind = parsed_book_info["kinds"][0]["name"]
    author_url = parsed_book_info["authors"][0]["href"]
    txt_url = parsed_book_info["txt"]

    # ================== author info scrapping =============

    is_date_found = True

    if author_url is not None and author_url != '':

        response_author_info = requests.get(author_url)
        data_author_info = response_author_info.text
        parsed_author_info = json.loads(data_author_info)

        author_description_ugly = parsed_author_info["description"]

        birth_date_sign = "Ur."
        date_start_sign = "<dd>"
        date_end_sign = "<br>"
        birth_date_area_start_position = author_description_ugly.find(birth_date_sign)

        if birth_date_area_start_position != -1:

            # find birth date in author's description
            birth_date_start_position = \
                author_description_ugly[birth_date_area_start_position:].find(date_start_sign) \
                + birth_date_area_start_position \
                + len(date_start_sign) \
                + 1

            birth_date_length = author_description_ugly[birth_date_start_position:].find(date_end_sign)
            birth_date_raw = author_description_ugly[birth_date_start_position:birth_date_start_position + birth_date_length]

            # exclude birth location
            year_end_position = re.search(r"\b[1-2]?[0-9]{3}\b", birth_date_raw).end()
            birth_date_str = birth_date_raw[:year_end_position]

            birth_date = date_parse(birth_date_str)

        else:
            is_date_found = False

        death_date_sign = "Zm."
        death_date_area_start_position = author_description_ugly.find(death_date_sign)

        if death_date_area_start_position != -1:

            death_date_start_position = \
                author_description_ugly[death_date_area_start_position:].find(date_start_sign) \
                + death_date_area_start_position \
                + len(date_start_sign) \
                + 1

            death_date_end_length = author_description_ugly[death_date_start_position:].find(date_end_sign)
            death_date_raw = author_description_ugly[
                                death_date_start_position: death_date_start_position + death_date_end_length
                             ]

            # exclude death location
            year_end_position = re.search(r"\b[1-2]?[0-9]{3}\b", death_date_raw).end()
            death_date_str = death_date_raw[:year_end_position]

            death_date = date_parse(death_date_str)

        else:
            is_date_found = False

    else:
        is_date_found = False

    if not is_date_found:
        birth_date = None  # TODO find birth data on wikipedia
        death_date = None  # TODO find death data on wikipedia

    # ================== txt scrapping =====================

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

    else:
        book_pure_txt = None

    # ================== output ===========================

    # print("Title:\t", title)
    # print("Kind:\t", kind)
    # print("Epoch:\t", epoch)
    # print("Author:\t", author)
    # print("Born:\t", birth_date)
    # print("Died:\t", death_date)
    # print("Txt fragment:\n\n", book_pure_txt[:800])

    if birth_date is not None:
        birth_date = birth_date.strftime('%d-%m-%Y')

    if death_date is not None:
        death_date = death_date.strftime('%d-%m-%Y')

    data_dictionary = {
        "title": title,
        "kind": kind,
        "epoch": epoch,
        "author": author,
        "birth_date": birth_date,
        "death_date": death_date,
        "txt": book_pure_txt
        }

    return data_dictionary


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

    with open('url_list.txt', 'w') as file:
        for url in url_list:
            file.write("%s\n" % url)


def save_data_for_books(book_count=-1):
    """
    Gets data for given number of books listed in file: url_list.txt and saves it in data.json file.
    When given count < 0 then function loads all books available
    Function does not load data for books without txt
    :return: -
    """

    with open('url_list.txt', 'r') as file:
        book_list = file.readlines()

    data = []
    do_for_all = False

    if book_count == 0:
        return
    elif book_count < 0:
        do_for_all = True

    for i, url in enumerate(book_list):
        if i >= book_count and not do_for_all:
            break
        book_data = get_data_for_book_url(url)

        # write only data with text provided
        if book_data["txt"] is not None:
            data.append(book_data)
        else:
            book_count += 1                                             # save one book more if omitted book without txt

    with open('data.json', 'w') as file:
        json.dump(data, file)


def read_saved_data():
    """
    Reads (printout) saved data from data.json file
    :return: -
    """

    with open('data.json', 'r') as file:
        data = json.load(file)

    for book in data:
        print("\n\n", "-"*30)
        print("Title:\t", book["title"])
        print("Kind:\t", book["kind"])
        print("Epoch:\t", book["epoch"])
        print("Author:\t", book["author"])
        print("Born:\t", book["birth_date"])
        print("Died:\t", book["death_date"])
        print("Txt fragment:\n\n", book["txt"][:500])


# start = time.time()
#
# save_data_for_books(20)     # now it loads only 20 books                # TODO do it for all books
#
# end = time.time()
# print("\n", end - start)


read_saved_data()
