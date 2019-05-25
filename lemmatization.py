from book import *
import morfeusz2

morf = morfeusz2.Morfeusz()


def lemmatize(word_vector):
    """
    Function transforms polish words to its basic form (lemma).
    Based on morfeusz2 project.
    NOTE: Pseudo-heuristic applied for choosing the best suited lemma.
    :param word_vector: Array of words to be transformed.
    :return: Array of lemmas made out of word_vector.
    """
    lemmatized_words = []

    for word in word_vector:
        analysis = morf.analyse(word)
        lemmatized_words.append(analysis[0][2][1])    # pseudo-heuristic applied for choosing right lemma

    return lemmatized_words


def tokenize(txt):
    """
    Returns a vector of words out of raw text.
    Simple, hand made version.
    :param txt: Raw text.
    :return: Vector of words.
    """
    words_vector = []
    word = ""
    separator = [u' ', u'\n']
    special_characters_to_pass = [
        u'\r',
        u'\t',
        u'0',
        u'1',
        u'2',
        u'3',
        u'4',
        u'5',
        u'6',
        u'7',
        u'8',
        u'9',
        u'—',
        u'-',
        u'.',
        u'…',
        u',',
        u';',
        u'!',
        u'"',
        u'„',
        u'”',
        u'(',
        u')'
    ]

    for letter in txt:

        if letter in special_characters_to_pass:
            # do not append nor make a new word when \t or \r
            pass

        elif letter in separator:
            if word.__len__() > 0:
                words_vector.append(word)
            word = ""

        else:
            word += letter

    words_vector.append(word)

    return words_vector


def main():
    books = construct_list_of_books()
    txt = books[77].text
    words_vector = tokenize(txt)
    lemmatized = lemmatize(words_vector)

    lemmatized_count = 0
    words_count = 100
    if words_count > words_vector.__len__():
        words_count = words_vector.__len__()

    for i in range(words_count):
        if words_vector[i] != lemmatized[i]:
            print(words_vector[i] + " > " + lemmatized[i])
            lemmatized_count += 1

    lemmatized_percent = 100 * lemmatized_count / words_count
    print("Lemmatized: " + str(lemmatized_percent) + "%")


if __name__ == '__main__':
    main()
