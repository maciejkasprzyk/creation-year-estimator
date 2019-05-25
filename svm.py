from pprint import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

import book as bk


def prepare_class_labels_vector(books):
    labels = []
    for book in books:
        year = book.date
        if year < 0:
            labels.append("PNE")
        elif year < 1000:
            labels.append("0-1000")
        elif year < 1500:
            labels.append("1000-1500")
        elif year < 1700:
            labels.append("1500-1700")
        else:
            labels.append(">1700")

    return labels


def main():
    print("constructing list of books...")
    books = bk.construct_list_of_books()[0:1000]

    texts_list = [book.text for book in books]
    labels = prepare_class_labels_vector(books)

    print("vectorizing...")
    vectorizer = CountVectorizer()
    # tokenize and build vocab

    pipeline = Pipeline([("vect", CountVectorizer()),
                         ("tfidf", TfidfTransformer()),
                         ("svm", SVC(kernel="rbf"))])

    parameters = {
        # 'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_features': (None, 5000, 10000, 50000),
        # 'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        # 'tfidf__use_idf': (True, False),
        # 'tfidf__norm': ('l1', 'l2'),

    }

    grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(texts_list, labels)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # summarize
    print("Vocabulary len:\n", len(vectorizer.vocabulary_))
    # print("Vocabulary:\n", vectorizer.vocabulary_)
    print("Features len:\n", len(vectorizer.get_feature_names()))
    # print("Feature names:\n", vectorizer.get_feature_names())

    # encode document


if __name__ == '__main__':
    main()
