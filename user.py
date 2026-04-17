from abc import ABC, abstractmethod


# ============================================================
#  ABSTRACTION — كلاص مجرد للمستخدم
# ============================================================
class User(ABC):
    """Abstract base class for all library users."""

    def __init__(self, user_id: int, name: str):
        self._user_id       = user_id
        self._name          = name
        self._borrowed_items = []       # list of item_ids

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def borrowed_items(self):
        return list(self._borrowed_items)   # return a copy

    def borrow_item(self, item_id: str):
        self._borrowed_items.append(item_id)

    def return_item(self, item_id: str) -> bool:
        if item_id in self._borrowed_items:
            self._borrowed_items.remove(item_id)
            return True
        return False

    @abstractmethod
    def get_role(self) -> str:
        pass

    @abstractmethod
    def get_permissions(self) -> list:
        pass

    # Polymorphism: __str__
    def __str__(self):
        return (f"  👤 [{self._user_id}] {self._name} | Role: {self.get_role()}\n"
                f"     Borrowed: {len(self._borrowed_items)} item(s)")


# ============================================================
#  INHERITANCE — طالب
# ============================================================
class Student(User):
    """Student user — can borrow up to 3 items."""

    MAX_BORROW = 3

    def __init__(self, user_id: int, name: str, grade: str = "N/A"):
        super().__init__(user_id, name)
        self.__grade = grade

    @property
    def grade(self):
        return self.__grade

    def can_borrow(self) -> bool:
        return len(self._borrowed_items) < self.MAX_BORROW

    # Polymorphism
    def get_role(self) -> str:
        return "Student"

    def get_permissions(self) -> list:
        return ["view_books", "borrow_book", "return_book"]

    def __str__(self):
        base = super().__str__()
        return base + f" / Grade: {self.__grade} (limit: {self.MAX_BORROW})"


# ============================================================
#  INHERITANCE — أستاذ
# ============================================================
class Teacher(User):
    """Teacher user — can borrow up to 10 items and add books."""

    MAX_BORROW = 10

    def __init__(self, user_id: int, name: str, department: str = "General"):
        super().__init__(user_id, name)
        self.__department = department

    @property
    def department(self):
        return self.__department

    def can_borrow(self) -> bool:
        return len(self._borrowed_items) < self.MAX_BORROW

    # Polymorphism
    def get_role(self) -> str:
        return "Teacher"

    def get_permissions(self) -> list:
        return ["view_books", "borrow_book", "return_book", "add_book", "remove_book"]

    def __str__(self):
        base = super().__str__()
        return base + f" / Dept: {self.__department} (limit: {self.MAX_BORROW})"


# ============================================================
#  INHERITANCE — مدير المكتبة
# ============================================================
class Librarian(User):
    """Librarian — full access."""

    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name)

    def can_borrow(self) -> bool:
        return True

    def get_role(self) -> str:
        return "Librarian"

    def get_permissions(self) -> list:
        return ["view_books", "borrow_book", "return_book",
                "add_book", "remove_book", "manage_users"]

    def __str__(self):
        return super().__str__() + " / Full Access 🔑"
