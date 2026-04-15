import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta


class Book:
    def __init__(self, title):
        self.title = title
        self.available = True
        self.borrow_count = random.randint(0, 10)


class UserRating:
    def __init__(self):
        self.late_records = {}

    def add_late(self, user, days_late):
        if user not in self.late_records:
            self.late_records[user] = 0
        self.late_records[user] += days_late

    def show_ratings(self):
        print("\nUser Late Ratings:")
        if not self.late_records:
            print("No late returns yet")
        for user, days in self.late_records.items():
            print(f"{user} was late {days} days total")


class Library:
    def __init__(self):
        self.books = []
        self.history = []
        self.borrowed_books = {}
        self.user_rating = UserRating()

    def load_books_from_excel(self, file_path):
        df = pd.read_excel(file_path)
        for title in df.iloc[:, 0]:
            self.books.append(Book(title))

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def show_books(self):
        print("\nAvailable books:")
        for book in self.books:
            status = "Available" if book.available else "Taken"
            print(f"- {book.title} ({status})")

    def borrow_book(self, title, user):
        book = self.find_book(title)

        if book:
            if book.available:
                book.available = False
                book.borrow_count += 1

                deadline = datetime.now() + timedelta(days=7)
                self.borrowed_books[title] = (user, deadline)

                self.history.append((user, title))
                print(f"You took the book! Return before {deadline.date()} ")

            else:
                print("Book is already taken ")
        else:
            print("No such book")

    def return_book(self, title):
        book = self.find_book(title)

        if book:
            book.available = True

            if title in self.borrowed_books:
                user, deadline = self.borrowed_books.pop(title)

                today = datetime.now()
                late_days = (today - deadline).days

                if late_days > 0:
                    print(f"Returned late by {late_days} days")
                    self.user_rating.add_late(user, late_days)
                else:
                    print("Returned on time")

            print("Book returned!")

        else:
            print("Book not found")

    def show_history(self):
        print("\nHistory:")
        for user, book in self.history:
            print(f"{user} borrowed '{book}'")

    def show_user_ratings(self):
        self.user_rating.show_ratings()

    def plot_popularity(self):
        titles = [book.title for book in self.books]
        counts = [book.borrow_count for book in self.books]

        plt.figure()
        plt.bar(titles, counts)
        plt.title("Book Popularity")
        plt.xlabel("Books")
        plt.ylabel("Times borrowed")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    def plot_pie(self):
        titles = [book.title for book in self.books]
        counts = [book.borrow_count for book in self.books]

        plt.figure()
        plt.pie(counts, labels=titles, autopct='%1.1f%%')
        plt.title("Popularity Share")
        plt.show()

    def plot_top_books(self):
        sorted_books = sorted(self.books, key=lambda b: b.borrow_count, reverse=True)
        top = sorted_books[:3]

        titles = [b.title for b in top]
        counts = [b.borrow_count for b in top]

        plt.figure()
        plt.barh(titles, counts)
        plt.title("Top 3 Books")
        plt.xlabel("Times borrowed")
        plt.show()


library = Library()
library.load_books_from_excel("Librarydata.xlsx")

while True:
    print("\n1. Show books")
    print("2. Borrow book")
    print("3. Return book")
    print("4. Show history")
    print("5. Show graphs")
    print("6. Show user ratings")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        library.show_books()

    elif choice == "2":
        title = input("Book title: ")
        name = input("Your name: ")
        library.borrow_book(title, name)

    elif choice == "3":
        title = input("Book title: ")
        library.return_book(title)

    elif choice == "4":
        library.show_history()

    elif choice == "5":
        library.plot_popularity()
        library.plot_pie()
        library.plot_top_books()

    elif choice == "6":
        library.show_user_ratings()

    elif choice == "0":
        break