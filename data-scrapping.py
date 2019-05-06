import requests
import json
print()

url = "https://wolnelektury.pl/api/books/studnia-i-wahadlo/"


# ================== info scrapping =====================

response_book_info = requests.get(url)
data_book_info = response_book_info.text
parsed_book_info = json.loads(data_book_info)

# print(json.dumps(parsed_book_info, indent=4))

title = parsed_book_info["title"]
author = parsed_book_info["authors"][0]["name"]
author_url = parsed_book_info["authors"][0]["href"]
epoch = parsed_book_info["epochs"][0]["name"]
txt_url = parsed_book_info["txt"]

print("Title:\t", title)
print("Author:\t", author)
print("Epoch:\t", epoch)


# ================== author info scrapping =============

response_author_info = requests.get(author_url)
data_author_info = response_author_info.text
parsed_author_info = json.loads(data_author_info)

author_description_ugly = parsed_author_info["description"]

born_date_sign = "Ur."
date_start_sign = "<dd>"
date_end_sign = "<br>"
born_date_area_start_position = author_description_ugly.find(born_date_sign)

if born_date_area_start_position != -1:

    born_date_start_position = \
        author_description_ugly[born_date_area_start_position:].find(date_start_sign) \
        + born_date_area_start_position \
        + len(date_start_sign) \
        + 1

    born_date_length = author_description_ugly[born_date_start_position:].find(date_end_sign)
    born_date = author_description_ugly[born_date_start_position:born_date_start_position + born_date_length]

else:
    pass                            # TODO find born data on wikipedia

print("Born:\t", born_date)         # TODO extract pure date only


death_date_sign = "Zm."
death_date_area_start_position = author_description_ugly.find(death_date_sign)

if death_date_area_start_position != -1:

    death_date_start_position = \
        author_description_ugly[death_date_area_start_position:].find(date_start_sign) \
        + death_date_area_start_position \
        + len(date_start_sign) \
        + 1

    death_date_end_length = author_description_ugly[death_date_start_position:].find(date_end_sign)
    death_date = author_description_ugly[death_date_start_position:death_date_start_position + death_date_end_length]

else:
    pass                            # TODO find death data on wikipedia

print("Died:\t", death_date)        # TODO extract pure date only


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
    book_pure_txt = book_without_footer[header_last_position + ISBN_length:]
else:
    book_pure_txt = book_without_footer

print("Txt fragment:\t", book_pure_txt[:600])

