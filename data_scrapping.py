import requests
import json
from date_parser_pl import *


# TODO automate looking for all books at once -> https://wolnelektury.pl/api/books/

url = "https://wolnelektury.pl/api/books/studnia-i-wahadlo/"
# url = "https://wolnelektury.pl/api/books/pan-tadeusz/"
# url = "https://wolnelektury.pl/api/books/a-co-wam-spiewac/"     # TODO lyric need to be treated differently to epic

# ================== info scrapping =====================

response_book_info = requests.get(url)
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
    year_end_position = re.search(r"\b[1-2][0-9]{3}\b", birth_date_raw).end()
    birth_date_str = birth_date_raw[:year_end_position]

    birth_date = date_parse(birth_date_str)

else:
    pass                            # TODO find birth data on wikipedia


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
    year_end_position = re.search(r"\b[1-2][0-9]{3}\b", death_date_raw).end()
    death_date_str = death_date_raw[:year_end_position]

    death_date = date_parse(death_date_str)

else:
    pass                            # TODO find death data on wikipedia


# ================== txt scrapping =====================

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
ISBN_length = 4 + 1 + 13 + 4 + 1

if header_last_position != -1:
    book_pure_txt = book_without_footer[header_last_position + ISBN_length:].strip()
else:
    book_pure_txt = book_without_footer.strip()


# ================== output ===========================

print("Title:\t", title)
print("Kind:\t", kind)
print("Epoch:\t", epoch)
print("Author:\t", author)
print("Born:\t", birth_date)
print("Died:\t", death_date)
print("Txt fragment:\n\n", book_pure_txt[:800])


