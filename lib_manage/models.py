from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

class Person(models.Model):
    name = models.CharField(max_length=300)
    tell = models.CharField(max_length=11)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    balance = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    isbn = models.CharField(max_length=13)
    publishel = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    number_of_available = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} {self.number_of_available}"


class BorrowedBook(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrowed_date = models.DateTimeField(default=timezone.now)
    must_return_date = models.DateTimeField(default=(timezone.now() + timedelta(days=10)))
    actual_return_date = models.DateTimeField(null=True, blank=True)
    return_book = models.OneToOneField('ReturnBook', on_delete=models.CASCADE, null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person} borrowed {self.book}"
    
    def calculate_penalty(self):
        if self.must_return_date.date() < timezone.now().date():
            days_diff = (timezone.now().date() - self.must_return_date.date()).days
            penalty_amount = days_diff * 1 # '1' is amount of penalty per day.
            self.person.balance -= penalty_amount
            self.person.save()
    

class ReturnBook(models.Model):
    borrowed_book = models.OneToOneField('BorrowedBook', on_delete=models.CASCADE)
    return_date = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.borrowed_book
    