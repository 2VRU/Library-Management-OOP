class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"✔️ Added: {book.title}")

    def show_all_books(self):
        if not self.books:
            print("⚠️ Library is empty.")
        else:
            for book in self.books:
                print(book)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def borrow_book(self, user, isbn):
        book = self.find_book(isbn)
        if book and book.is_available:
            if len(user.borrowed_books) < user.limit:
                book.is_available = False
                user.borrowed_books.append(book)
                print(f"✅ {user.name} borrowed '{book.title}'")
            else:
                print(f"❌ {user.name} reached the limit!")
        else:
            print("❌ Book unavailable or not found.")