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
        

class BorrowedBookSerializers(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = '__all__'
        depth = 1
        

class ReturnBookSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReturnBook
        fields = '__all__'
        depth = 2
        
