class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_available = True  # خاصية Encapsulation للحالة

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"ISBN: {self.isbn} | {self.title} by {self.author} ({status})"