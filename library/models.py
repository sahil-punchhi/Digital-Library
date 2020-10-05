from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# create your models here


class Person(User):
    country = CountryField(blank_label = '(select country)')

    def __str__(self):
        return self.first_name + ' - ' + self.email + ' - ' + self.username + ' - ' + str(self.country)


class Book(models.Model):
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    isbn = models.CharField(max_length=13)
    user_added = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.author + ' - ' + str(self.date_added)[:10] + ' - ' + self.isbn + ' - ' + str(self.user_added)

    def save(self, *args, **kwargs):
        if self.isbn:
            if not len(self.isbn) == 13:
                raise Exception("ISBN is not valid.")
            super().save(*args, **kwargs)





# user1=User(username="aman6", password="qazxc1234")
# user1.save()
# book1 = Book(title="Alchemist", author="Paulo", isbn="1231231231235", user_added=user1)  # create a ToDoList
#
# book1.save()  # saves the ToDoList in the database
#
# print(book1.id)  # prints 1, each list is given an id automatically
#
# print(Book.objects.all())
