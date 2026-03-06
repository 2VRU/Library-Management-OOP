class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"ID: {self.user_id} | Name: {self.name}"

class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.limit = 3  # حد الاستعارة للطلاب

class Teacher(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.limit = 10  # حد الاستعارة للأساتذة