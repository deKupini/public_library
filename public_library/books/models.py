from django.db import models


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    borrowed = models.BooleanField(default=False)
    borrow_date = models.DateField(null=True, default=None)
    borrower = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.title
