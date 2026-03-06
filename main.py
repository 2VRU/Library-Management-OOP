from book import Book
from user import Student, Teacher
from library import Library

def main():
    my_library = Library()
    # إضافة كتب افتراضية
    my_library.add_book(Book("101", "Python Basics", "Guido"))
    my_library.add_book(Book("102", "OOP Principles", "Robert"))

    user = Student(1, "Abdou")

    while True:
        print("\n--- Library System ---")
        print("1. Show Books\n2. Add Book\n3. Borrow Book\n4. Exit")
        choice = input("Select: ")

        if choice == "1":
            my_library.show_all_books()
        elif choice == "2":
            isbn = input("ISBN: ")
            title = input("Title: ")
            author = input("Author: ")
            my_library.add_book(Book(isbn, title, author))
        elif choice == "3":
            isbn = input("Enter ISBN to borrow: ")
            my_library.borrow_book(user, isbn)
        elif choice == "4":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()