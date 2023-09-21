from rest_framework import serializers

from .models import Person, Book, BorrowedBook, ReturnBook


class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1
        

