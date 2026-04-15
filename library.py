pfrom book import Book, EBook, Magazine, LibraryItem
from user import User


# ============================================================
#  ENCAPSULATION — كلاص المكتبة
# ============================================================
class Library:
    """Manages all library items and users."""

    def __init__(self, name: str = "My Library"):
        self.__name  = name
        self.__items: dict[str, LibraryItem] = {}   # isbn -> item
        self.__users: dict[int, User]        = {}   # id   -> user

    # ---------- Properties ----------
    @property
    def name(self):
        return self.__name

    # ======================================================
    #  ITEM MANAGEMENT
    # ======================================================
    def add_item(self, item: LibraryItem) -> bool:
        if item.item_id in self.__items:
            return False
        self.__items[item.item_id] = item
        return True

    def remove_item(self, item_id: str) -> bool:
        if item_id in self.__items:
            del self.__items[item_id]
            return True
        return False

    def find_item(self, item_id: str):
        return self.__items.get(item_id, None)

    def search_by_title(self, keyword: str) -> list:
        kw = keyword.lower()
        return [item for item in self.__items.values()
                if kw in item.title.lower()]

    # ======================================================
    #  USER MANAGEMENT
    # ======================================================
    def register_user(self, user: User) -> bool:
        if user.user_id in self.__users:
            return False
        self.__users[user.user_id] = user
        return True

    def find_user(self, user_id: int):
        return self.__users.get(user_id, None)

    # ======================================================
    #  BORROW / RETURN  — Polymorphism in action
    #  (works for Book, EBook, Magazine through LibraryItem)
    # ======================================================
    def borrow_item(self, user: User, item_id: str) -> tuple[bool, str]:
        item = self.find_item(item_id)
        if not item:
            return False, "Item not found."

        # Permission check
        if "borrow_book" not in user.get_permissions():
            return False, "You don't have permission to borrow."

        # Borrow limit check (only users with can_borrow method)
        if hasattr(user, "can_borrow") and not user.can_borrow():
            return False, f"Borrow limit reached for {user.get_role()}."

        # Availability check (Polymorphism: works for any LibraryItem subclass)
        if not item.available:
            return False, f'"{item.title}" is already borrowed.'

        item.available = False
        user.borrow_item(item_id)
        return True, f'✅ "{item.title}" borrowed successfully!'

    def return_item(self, user: User, item_id: str) -> tuple[bool, str]:
        item = self.find_item(item_id)
        if not item:
            return False, "Item not found."

        if item_id not in user.borrowed_items:
            return False, "You haven't borrowed this item."

        item.available = True
        user.return_item(item_id)
        return True, f'✅ "{item.title}" returned successfully!'

    # ======================================================
    #  DISPLAY HELPERS
    # ======================================================
    def show_all_items(self):
        if not self.__items:
            print("  (No items in library)")
            return
        # Polymorphism: each item prints itself differently
        types = {}
        for item in self.__items.values():
            t = item.get_type()
            types.setdefault(t, []).append(item)

        for t, items in types.items():
            print(f"\n  ── {t}s ──")
            for item in items:
                print(item.get_info())

    def show_all_users(self):
        if not self.__users:
            print("  (No users registered)")
            return
        for user in self.__users.values():
            print(user)

    def show_borrowed_by(self, user: User):
        ids = user.borrowed_items
        if not ids:
            print(f"  {user.name} has no borrowed items.")
            return
        for iid in ids:
            item = self.find_item(iid)
            if item:
                print(item.get_info())

    def get_stats(self) -> dict:
        total     = len(self.__items)
        available = sum(1 for i in self.__items.values() if i.available)
        borrowed  = total - available
        return {
            "total"    : total,
            "available": available,
            "borrowed" : borrowed,
            "users"    : len(self.__users),
        }
