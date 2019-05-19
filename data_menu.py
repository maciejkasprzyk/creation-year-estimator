import data_download
import data_scraping


def is_user_sure():
    print("Do you really want to start the download? it may take long time")
    answer = input(" [Y/n]: ")
    if answer == "Y":
        return True
    return False


def main():
    print("What do you want to do?")

    # download
    print("dl to download list of books")
    print("db to download books info")
    print("da to download authors info")
    print("dt to download books texts")
    # scrap
    print("sa to scrap authors birth and death dates")
    # print
    print("pb to print books info")
    print("pa to print authors descriptions")
    print("pd to print authors with dates")
    print("pt to print text samples")

    choice = input("Your choice: ").strip()

    # download
    if choice == "dl":
        if is_user_sure():
            data_download.save_book_list()
    elif choice == "db":
        how_many_books = int(input("How many books do you want to download? (type -1 for all): "))
        if is_user_sure():
            data_download.save_data_for_books(how_many_books)
    elif choice == "da":
        if is_user_sure():
            data_download.save_data_for_authors()
    elif choice == "dt":
        if is_user_sure():
            data_download.save_texts()
    # scrap
    elif choice == 'sa':
        data_scraping.scrap_authors_info()
    # print
    elif choice == 'pb':
        data_download.printout_books_info()
    elif choice == 'pa':
        data_download.printout_authors_info_raw()
    elif choice == 'pd':
        data_download.printout_authors_info_ready()
    elif choice == 'pt':
        data_download.printout_text_samples()
    else:
        print("incorrect choice")


if __name__ == '__main__':
    main()
