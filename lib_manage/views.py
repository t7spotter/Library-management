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
            