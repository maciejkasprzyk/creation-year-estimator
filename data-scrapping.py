import requests
import json
print()

url = "https://wolnelektury.pl/api/books/studnia-i-wahadlo/"

response_book = requests.get(url)
data_book = response_book.text
parsed_book = json.loads(data_book)

# print(json.dumps(parsed, indent=4))

title = parsed_book["title"]
author = parsed_book["authors"][0]["name"]
epoch = parsed_book["epochs"][0]["name"]
txt_url = parsed_book["txt"]

print(title)
print(author)
print(epoch)
# print(txt_url)

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

print(book_pure_txt)

