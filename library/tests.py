from django.test import TestCase
from library.models import Person, Book, User
from rest_framework.test import APITestCase
from datetime import date, datetime, timedelta
import datetime
import warnings
warnings.filterwarnings("ignore")

flag = True # setting this flag to true gives count and other information related to test cases
flag2 = False # setting this flag to true gives response information related to test cases
# Create your tests here.

class PersonTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.user2 = User.objects.create_user(username='Sam', email='sam.graham@hotmail.com', password='top_secret2')
        self.user3 = User.objects.create_user(username='Chris', email='cram@yahoo.com', password='top_secret3')


        Book.objects.create(title="Bighead", author="Jeffrey Brown", isbn="9781891830563", user_added=self.user1)
        Book.objects.create(title="Cry Yourself to Sleep", author="Jeremy Tinder", isbn="9781891830815", user_added=self.user1)
        Book.objects.create(title="Mosquito", author="Dan James", isbn="9781891830686", user_added=self.user1)
        Book.objects.create(title="Pinky & Stinky", author="James Kochalka", isbn="9781891830297", user_added=self.user1)
        Book.objects.create(title="Spiral Bound", author="Aaron Renier", isbn="9781891830501", user_added=self.user2)
        Book.objects.create(title="Three Fingers", author="Rich Koslowski", isbn="9781891830310", user_added=self.user2)
        Book.objects.create(title="Unlikely", author="Jeffrey Brown", isbn="9781891830419", user_added=self.user3)


    def test_add_book(self):

        if flag:
            print("----------------------")
            print("ADD BOOK TEST CASE")
            print("----------------------")
            print("\n")

        initial_book_count = Book.objects.count()
        if flag:
            print("The initial book count is", initial_book_count, ".")

        book = {
            "title": "Alchemist",
            "author": "Paulo Cohelo",
            "isbn": "9780694524471",
        }

        # add book by unlogged user
        response = self.client.post('/addbook/', book)

        if flag:
            print("New book count after book is added by unlogged user is", Book.objects.count(), ".")
            print("The book count is same showing only logged users can add books.")

        # since user has not logged in
        self.assertEqual(
            Book.objects.count(),
            initial_book_count
        )

        if response.status_code != 201:
            if flag2:
                print("Response after adding book is", response)

        # when user logs in
        log = {
            "username" : "jacob",
            "password" : "top_secret"
        }

        response2 = self.client.post('/login/', log)
        if response2.status_code != 201:
            if flag2:
                print("Response after logging is", response2)

        book2 = {
            "title": "Alchemist",
            "author": "Paulo Cohelo",
            "isbn": "9780694524471",
        }

        # add book by logged user
        response3 = self.client.post('/addbook/', book2)
        if response3.status_code != 201:
            if flag2:
                print("Response after adding book is", response3)

        if flag:
            print("New book count after book is added by logged user is", Book.objects.count(), ".")
            print("The book count increases by 1 showing only logged users can successfully add new books.")

        # book count should increase by 1
        self.assertEqual(
            Book.objects.count(),
            initial_book_count + 1
        )

    def test_delete_book(self):

        if flag:
            print("\n")
            print("----------------------")
            print("DELETE BOOK TEST CASE")
            print("----------------------")
            print("\n")

        initial_book_count = Book.objects.count()
        if flag:
            print("Very initial book count is", initial_book_count, ".")

        log = {
            "username" : "jacob",
            "password" : "top_secret"
        }

        response2 = self.client.post('/login/', log)

        book2 = {
            "title": "fountainhead",
            "author": "Ayn Rand",
            "isbn": "9780026009102",
        }

        # add book by logged user
        response3 = self.client.post('/addbook/', book2)

        initial_book_count = Book.objects.count()
        if flag:
            print("The book count after adding a book is", initial_book_count, ".")

        book_to_be_deleted = {
            "title": "fountainhead",
        }

        # delete book by logged user
        response3 = self.client.post('/fountainhead/deletebook/') # case sensitive
        if response3.status_code != 201:
            if flag2:
                print("Response after deleting book is", response3)

        if flag:
            print("New book count after book is deleted by logged user is", Book.objects.count(), ".")
            print("The book count decreases by 1 showing only logged users can successfully delete books.")

        # book count should increase by 1
        self.assertEqual(
            Book.objects.count(),
            initial_book_count - 1
        )

    def test_view_book(self):

        if flag:
            print("\n")
            print("----------------------")
            print("VIEW BOOK TEST CASE")
            print("----------------------")
            print("\n")

        initial_book_count = Book.objects.count()
        if flag:
            print("Very initial book count is", initial_book_count, ".")

        log = {
            "username" : "jacob",
            "password" : "top_secret"
        }

        response2 = self.client.post('/login/', log)

        today = date.today()
        # book count should increase by 1

        # 4 books are recently added by this user
        self.assertEqual(
            Book.objects.filter(user_added=self.user1, date_added__gte=today-timedelta(days=7)).count(),
            4
        )
