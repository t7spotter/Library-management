from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.utils import timezone

from .models import Person, Book, BorrowedBook, ReturnBook
from .serializers import PersonSerializers, BookSerializers, BorrowedBookSerializers, ReturnBookSerializers, ContainSearchSerializer


class GetPostPerson(APIView):
    def get(self, request: Request, pk=None):
        if pk:
            query = Person.objects.get(pk=pk)
            ser = PersonSerializers(query)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            query = Person.objects.all()
            ser = PersonSerializers(query, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        
    def post(self, request: Request):
        ser = PersonSerializers(data=request.data)
        if ser.is_valid():
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request: Request, pk):
        try:
            query = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response({"message" : "Can not find this person"}, status=status.HTTP_404_NOT_FOUND)
        else:
            query.delete()
            return Response({"message" : "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request: Request, pk):
        try:
            query = Person.objects.get(pk=pk)
            ser = PersonSerializers(query, data=request.data)
        except Person.DoesNotExist:
            return Response({"message" : "Can not find this person"}, status=status.HTTP_404_NOT_FOUND)
        if ser.is_valid:
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        
        
class GetPostBook(APIView):
    def get(self, request: Request, pk=None):
        if pk:
            query = Book.objects.get(pk=pk)
            ser = BookSerializers(query)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            query = Book.objects.all()
            ser = BookSerializers(query, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        
    def post(self, request: Request):
        ser = BookSerializers(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request: Request, pk):
        try:
            query = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"message" : "Can not find this item"}, status=status.HTTP_404_NOT_FOUND)
        else:
            query.delete()
            return Response({"message" : "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request: Request, pk):
        try:
            query = Book.objects.get(pk=pk)
            ser = BookSerializers(query, data=request.data)
        except Book.DoesNotExist:
            return Response({"message" : "Can not find this item"}, status=status.HTTP_404_NOT_FOUND)
        if ser.is_valid:
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)


class BorrowBook(APIView):
    def post(self, request: Request):
        person_name = request.data.get('person')
        book_title = request.data.get('book')
        
        if not request.data:
            return Response({"message" : "Please send valid request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                person = Person.objects.get(name=person_name)
            except Person.DoesNotExist:
                return Response({"message" : "There is no person with this name"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                book = Book.objects.get(title=book_title)
            except Book.DoesNotExist:
                Response({"message" : "There is no book with this title"}, status=status.HTTP_404_NOT_FOUND)
            
            if person.balance < 0:
                return Response({"message" : "Your balance is negative, please charge your balance and try again."}, status=status.HTTP_403_FORBIDDEN)
            elif book.number_of_available == 0:
                return Response ({"message" : "This book is borrowed by another user."}, status=status.HTTP_403_FORBIDDEN)
            else:
                borrowed_book = BorrowedBook.objects.create(book=book, person=person)
                book.number_of_available -= 1
                borrowed_book.save()
                return Response({"message" : "Book borrowed successfully"}, status=status.HTTP_200_OK)
            
    def get(self, requset: Request):
        query = BorrowedBook.objects.all()
        ser = BorrowedBookSerializers(query, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ReturnBook(APIView):
    def post(self, request: Request):
        ser = ReturnBookSerializers(data=request.data)
        if ser.is_valid():
            borrowed_book_id = request.data.get('borrowed_book')
            borrowed_book = BorrowedBook.objects.get(id=borrowed_book_id)
            ser.save(borrowed_book=borrowed_book)
            
            #####################################
            borrowed_book.actual_return_date = timezone.now()
            borrowed_book.is_returned = True
            borrowed_book.calculate_penalty()
            borrowed_book.save()
            
            #returning the returned book to the storehouse (Book model):
            returned_book = ReturnBook.objects.get(id=ser.data.get('id'))
            borrowed_book = BorrowedBook.objects.get(id=returned_book.borrowed_book_id)
            book = Book.objects.get(id=borrowed_book.book_id)

            book.number_of_available += 1
            book.save()
            
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)