from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=300)
    tell = models.CharField(max_length=11)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    balance = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    
    def __str__(self):
        return self.name
