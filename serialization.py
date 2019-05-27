import book as bk
import lemmatization as lm
import json
from svm import prepare_class_labels_vector


def preprocessing():
    books = bk.construct_list_of_books()
    books_count = books.__len__()

    texts = []
    for book in books:
        texts.append(book.text)

    # new_texts_list = texts

    new_texts = []
    for i, txt in enumerate(texts):
        tokenized = lm.tokenize(txt)
        lemmatized = lm.lemmatize(tokenized)
        new_txt = ""
        for word in lemmatized:
            new_txt += word + " "
        new_texts.append(new_txt)
        print(str(i) + " / " + str(books_count))

    return new_texts


def main():
    preprocessed_texts = preprocessing()
    with open('data/preprocessed_texts.json', 'w') as file:
        json.dump(preprocessed_texts, file)

    # with open('data/preprocessed_texts.json', 'r') as file:
    #     data = json.load(file)
    # print(data[1])

#     json.dump(preprocessed_texts, file)


if __name__ == '__main__':
    main()

