from rest_framework import serializers

from .models import Person, Book, BorrowedBook, ReturnBook


class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'