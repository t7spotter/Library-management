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