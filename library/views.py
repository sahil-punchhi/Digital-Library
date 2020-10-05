from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from .models import Person
from .models import Book
from django.views.generic.edit import DeleteView # this is the generic view
from isbntools.app import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .addBook import BookForm
from datetime import date, datetime, timedelta
import datetime

# Create your views here.

# view entire book collection
@login_required(login_url='/accounts/login/')
@require_http_methods(["GET"])
def index(request):
    if request.method == 'GET':
        ls = {}

        ls["dataset"] = Book.objects.filter(user_added=request.user)
        ls["dataset2"] = Book.objects.filter(user_added=request.user)
        ls["days"] = 0

        # indexview(ls=ls)
        return render(request, "library/viewbooks.html", ls)

# view book collection for a specific number of days
@login_required(login_url='/accounts/login/')
@require_http_methods(["GET"])
def index2(request, no_of_days):
    if request.method == 'GET':
        ls = {}
        today = date.today()

        ls["dataset"] = Book.objects.filter(user_added=request.user, date_added__gte=today-timedelta(days=int(no_of_days)))
        ls["dataset2"] = Book.objects.filter(user_added=request.user)
        ls["days"] = no_of_days

        # indexview(ls=ls)
        return render(request, "library/viewbooks.html", ls)

# add a book to the collection
@login_required(login_url='/accounts/login/')
@require_http_methods(["POST", "GET"])
def add_book(request):
    if request.method == 'POST':

        filled = BookForm(request.POST)
        if filled.is_valid():
            book = filled.save(commit=False)
            book.user_added = request.user
            # Validation of a book using Google Books API
            try:
                # goob service uses Google Books APIs; no API key is needed
                meta_dict = meta(book.isbn, service='goob')
            except:
                return HttpResponseRedirect('/invalidisbn/')
            book.save()


            return HttpResponseRedirect('/viewbook/')

        return HttpResponse("This is not a valid entry.")
    else:
        form = BookForm()
    return render(request, 'library/addbook.html', {'form': form})

# special case of invalid isbn
@login_required(login_url='/accounts/login/')
def invalidisbn(request):

    ls = {}
    ls["days"] = 0
    ls["dataset"] = Book.objects.filter(user_added=request.user)

    return render(request, "library/invalidisbn.html", ls)

# delete a book from a collection - take input title or isbn
@login_required(login_url='/accounts/login/')
def delete(request):

    ls = {}
    ls["days"] = 0
    ls["dataset"] = Book.objects.filter(user_added=request.user)

    return render(request, "library/delete.html", ls)

# delete a book from a collection by entering book title or its isbn Number
# isbn number is considered as a 13 digit number without dashes or spaces
@login_required(login_url='/accounts/login/')
def delete_book(request, title):
    print(title)

    ls = {}
    ls["dataset"] = Book.objects.filter(user_added=request.user)

    # book title
    if len(str(title))==13 and int(title):
        ls["dataset2"] = Book.objects.filter(user_added=request.user, isbn=title)
        obj = get_object_or_404(Book, isbn = title)

    # book isbn
    else:
        ls["dataset2"] = Book.objects.filter(user_added=request.user, title=title)
        obj = get_object_or_404(Book, title = title)

    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect('/viewbook/')

    return render(request, "library/deletebook.html", ls)
