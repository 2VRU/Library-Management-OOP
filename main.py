import sys
import os

from book    import Book, EBook, Magazine
from user    import Student, Teacher, Librarian
from library import Library


# ============================================================
#  CLI COLORS (ANSI)
# ============================================================
class Color:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"

def c(text, color):
    return f"{color}{text}{Color.RESET}"


# ============================================================
#  DISPLAY HELPERS
# ============================================================
def banner():
    print(c("""
╔══════════════════════════════════════════╗
║        📚  Library Management  System   ║
║              OOP Edition  v2.0          ║
╚══════════════════════════════════════════╝
""", Color.CYAN))


def divider(title=""):
    line = "─" * 44
    if title:
        print(c(f"\n  ┌─ {title} {'─'*(38-len(title))}┐", Color.BLUE))
    else:
        print(c(f"  {line}", Color.BLUE))


def success(msg): print(c(f"\n  ✅  {msg}", Color.GREEN))
def error(msg):   print(c(f"\n  ❌  {msg}", Color.RED))
def info(msg):    print(c(f"\n  ℹ️   {msg}", Color.YELLOW))


def stats_bar(lib: Library):
    s = lib.get_stats()
    print(c(f"""
  ┌──────────────── Stats ──────────────────┐
  │  📦 Total: {s['total']:<5} 📗 Available: {s['available']:<5}     │
  │  📤 Borrowed: {s['borrowed']:<4} 👤 Users: {s['users']:<5}        │
  └─────────────────────────────────────────┘""", Color.MAGENTA))


def main_menu():
    print(c("""
  ╔══════════ MAIN MENU ══════════╗
  ║  1 │ 📋  Show All Items       ║
  ║  2 │ 📗  Add Book             ║
  ║  3 │ 💻  Add EBook            ║
  ║  4 │ 📰  Add Magazine         ║
  ║  5 │ 🔍  Search Item          ║
  ║  6 │ 📤  Borrow Item          ║
  ║  7 │ 📥  Return Item          ║
  ║  8 │ 👤  Show My Info         ║
  ║  9 │ 📊  Library Stats        ║
  ║  0 │ 🚪  Exit                 ║
  ╚═══════════════════════════════╝""", Color.CYAN))


def prompt(msg):
    return input(c(f"\n  ➤  {msg}: ", Color.YELLOW)).strip()


# ============================================================
#  ACTIONS
# ============================================================
def action_add_book(lib, user):
    if "add_book" not in user.get_permissions():
        error("You don't have permission to add books.")
        return
    divider("Add Book")
    isbn   = prompt("ISBN")
    title  = prompt("Title")
    author = prompt("Author")
    year   = prompt("Year (default 2024)") or "2024"
    book   = Book(isbn, title, author, int(year))
    if lib.add_item(book):
        success(f'Book "{title}" added!')
    else:
        error("ISBN already exists.")


def action_add_ebook(lib, user):
    if "add_book" not in user.get_permissions():
        error("You don't have permission to add items.")
        return
    divider("Add EBook")
    isbn   = prompt("ISBN")
    title  = prompt("Title")
    author = prompt("Author")
    year   = prompt("Year (default 2024)") or "2024"
    fmt    = prompt("Format (PDF/EPUB/MOBI)") or "PDF"
    ebook  = EBook(isbn, title, author, int(year), fmt.upper())
    if lib.add_item(ebook):
        success(f'EBook "{title}" added!')
    else:
        error("ISBN already exists.")


def action_add_magazine(lib, user):
    if "add_book" not in user.get_permissions():
        error("You don't have permission to add items.")
        return
    divider("Add Magazine")
    mid       = prompt("ID")
    title     = prompt("Title")
    issue     = prompt("Issue number")
    publisher = prompt("Publisher")
    mag = Magazine(mid, title, int(issue), publisher)
    if lib.add_item(mag):
        success(f'Magazine "{title}" added!')
    else:
        error("ID already exists.")


def action_search(lib):
    divider("Search")
    kw      = prompt("Enter keyword")
    results = lib.search_by_title(kw)
    if results:
        print(c(f"\n  Found {len(results)} result(s):\n", Color.GREEN))
        for item in results:
            print(item.get_info())
    else:
        info("No items found.")


def action_borrow(lib, user):
    divider("Borrow Item")
    item_id = prompt("Enter Item ID / ISBN")
    ok, msg = lib.borrow_item(user, item_id)
    success(msg) if ok else error(msg)


def action_return(lib, user):
    divider("Return Item")
    if not user.borrowed_items:
        info("You have no borrowed items.")
        return
    print(c("\n  Your borrowed items:", Color.YELLOW))
    lib.show_borrowed_by(user)
    item_id = prompt("Enter Item ID to return")
    ok, msg = lib.return_item(user, item_id)
    success(msg) if ok else error(msg)


def action_my_info(lib, user):
    divider("My Info")
    print(user)
    borrowed = user.borrowed_items
    if borrowed:
        print(c("\n  Borrowed items:", Color.YELLOW))
        lib.show_borrowed_by(user)
    print(c(f"\n  Permissions: {', '.join(user.get_permissions())}", Color.MAGENTA))


# ============================================================
#  SEED DATA
# ============================================================
def seed(lib: Library):
    # Books
    lib.add_item(Book("101", "Python Basics",     "Guido",   2020))
    lib.add_item(Book("102", "OOP Principles",    "Robert",  2019))
    lib.add_item(Book("103", "Clean Code",        "Martin",  2008))
    # EBooks
    lib.add_item(EBook("E01", "Django for Pros",  "Vincent", 2023, "PDF"))
    lib.add_item(EBook("E02", "FastAPI Guide",    "Tiangolo",2022, "EPUB"))
    # Magazines
    lib.add_item(Magazine("M01", "Tech Monthly", 45, "TechPress"))
    lib.add_item(Magazine("M02", "AI Weekly",     12, "AIMedia"))

    # Users
    lib.register_user(Student(1,   "Abdou",   "3rd Year"))
    lib.register_user(Teacher(2,   "Dr. Ali", "Computer Science"))
    lib.register_user(Librarian(3, "Admin"))


# ============================================================
#  MAIN
# ============================================================
def main():
    lib = Library("Université Library")
    seed(lib)

    banner()
    print(c("  Who are you?", Color.YELLOW))
    print("  1) Student (Abdou)")
    print("  2) Teacher (Dr. Ali)")
    print("  3) Librarian (Admin)")

    choice = prompt("Choose")
    uid_map = {"1": 1, "2": 2, "3": 3}
    user = lib.find_user(uid_map.get(choice, 1))
    if not user:
        error("Invalid choice, logging in as Student.")
        user = lib.find_user(1)

    success(f"Welcome, {user.name}! [{user.get_role()}]")

    while True:
        stats_bar(lib)
        main_menu()
        choice = prompt("Select option")

        if   choice == "1": lib.show_all_items()
        elif choice == "2": action_add_book(lib, user)
        elif choice == "3": action_add_ebook(lib, user)
        elif choice == "4": action_add_magazine(lib, user)
        elif choice == "5": action_search(lib)
        elif choice == "6": action_borrow(lib, user)
        elif choice == "7": action_return(lib, user)
        elif choice == "8": action_my_info(lib, user)
        elif choice == "9":
            divider("Statistics")
            stats_bar(lib)
        elif choice == "0":
            print(c("\n  👋  Goodbye! See you next time.\n", Color.CYAN))
            break
        else:
            error("Invalid option. Please try again.")

        input(c("\n  Press Enter to continue...", Color.BLUE))


if __name__ == "__main__":
    main()
