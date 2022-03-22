from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=60, unique=True)
    author = models.CharField(max_length=60, unique=False)
    pub_date = models.DateField()
    genre = models.CharField(max_length=60)
    isbn = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.title}'
    