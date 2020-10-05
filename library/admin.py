from django.contrib import admin

# Register your models here.
from .models import *

# Backend admin site

admin.site.register(Person)
admin.site.register(Book)
