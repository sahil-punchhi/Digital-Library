from django.core.serializers import serialize
from django.db.models import Count, Case, When, IntegerField
from rest_framework import serializers
from .models import *
from django.db import connection
from collections import defaultdict

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
