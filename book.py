from abc import ABC, abstractmethod


# ============================================================
#  ABSTRACTION — كلاص مجرد يمثل أي عنصر في المكتبة
# ============================================================
class LibraryItem(ABC):
    """Abstract base class for all items in the library."""

    def __init__(self, item_id: str, title: str):
        self._item_id = item_id      # Encapsulation: protected attribute
        self._title   = title

    @property
    def item_id(self):
        return self._item_id

    @property
    def title(self):
        return self._title

    @abstractmethod
    def get_info(self) -> str:
        """Every subclass MUST implement this."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    def __str__(self):
        return self.get_info()


# ============================================================
#  INHERITANCE + ENCAPSULATION — كلاص الكتاب
# ============================================================
class Book(LibraryItem):
    """Represents a regular book."""

    def __init__(self, isbn: str, title: str, author: str, year: int = 2024):
        super().__init__(isbn, title)
        self.__author    = author          # Encapsulation: private
        self.__year      = year
        self.__available = True

    # --- Getters / Setters (Encapsulation) ---
    @property
    def author(self):
        return self.__author

    @property
    def year(self):
        return self.__year

    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, value: bool):
        if isinstance(value, bool):
            self.__available = value

    # --- Abstract methods implementation (Polymorphism) ---
    def get_info(self) -> str:
        status = "✅ Available" if self.__available else "❌ Borrowed"
        return (f"  📗 [{self.item_id}] {self.title}\n"
                f"     Author : {self.__author} | Year: {self.__year}\n"
                f"     Status : {status}")

    def get_type(self) -> str:
        return "Book"


# ============================================================
#  INHERITANCE — كتاب رقمي (يرث من Book)
# ============================================================
class EBook(Book):
    """Represents a digital book — inherits from Book."""

    def __init__(self, isbn: str, title: str, author: str,
                 year: int = 2024, file_format: str = "PDF"):
        super().__init__(isbn, title, author, year)
        self.__file_format = file_format

    @property
    def file_format(self):
        return self.__file_format

    # Polymorphism: override get_info
    def get_info(self) -> str:
        base = super().get_info().replace("📗", "💻")
        return base + f"\n     Format : {self.__file_format}"

    def get_type(self) -> str:
        return "EBook"


# ============================================================
#  INHERITANCE — مجلة (ترث من LibraryItem مباشرة)
# ============================================================
class Magazine(LibraryItem):
    """Represents a magazine."""

    def __init__(self, mag_id: str, title: str, issue: int, publisher: str):
        super().__init__(mag_id, title)
        self.__issue     = issue
        self.__publisher = publisher
        self.__available = True

    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, value: bool):
        if isinstance(value, bool):
            self.__available = value

    def get_info(self) -> str:
        status = "✅ Available" if self.__available else "❌ Borrowed"
        return (f"  📰 [{self.item_id}] {self.title}\n"
                f"     Issue : #{self.__issue} | Publisher: {self.__publisher}\n"
                f"     Status: {status}")

    def get_type(self) -> str:
        return "Magazine"
