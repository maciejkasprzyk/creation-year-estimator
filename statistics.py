import collections
import pickle

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

import book as bk
import paths


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Predicted label',
           xlabel='True label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def print_all_epochs():
    books = bk.construct_list_of_books()
    data = []

    for item in books:
        if not data.__contains__(item.epoch):
            data.append(item.epoch)
            print(item.epoch)


def print_confusion_matrix():
    with open(paths.stats_gird_search_path, "rb") as file:
        grid_search, x_test, y_test = pickle.load(file)

    y_pred = grid_search.predict(x_test)

    counter = collections.Counter(y_pred)
    from pprint import pprint
    pprint(counter)

    class_names = ["Starożytność lub średniowiecze", "Renesans", "Barok", "Oświecenie", "Romantyzm", "Pozytywizm",
                   "Modernizm", "Dwudziestolecie międzywojenne", "Współczesność", "nie dotyczy"]

    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plot_confusion_matrix(y_test, y_pred, classes=class_names,
                          title='Confusion matrix, without normalization')

    # Plot normalized confusion matrix
    plot_confusion_matrix(y_test, y_pred, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')

    plt.show()


def count_books_by_epochs():
    books = bk.construct_list_of_books()
    epochs = [book.label for book in books]
    counter = dict(sorted(collections.Counter(epochs).items()))

    objects = counter.keys()
    y_pos = range(len(counter))
    y = counter.values()

    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=90)
    plt.ylabel('Ilość tekstów')
    plt.title('Rozkład ilości danych na epoki')

    plt.show()

    from pprint import pprint
    pprint(counter)


def main():
    # print_all_epochs()

    # count_books_by_epochs()
    print_confusion_matrix()


if __name__ == '__main__':
    main()
