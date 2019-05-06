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
print(txt_url)

response_txt = requests.get(txt_url)
data_txt = response_txt.text

print(data_txt)
