from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

default_value = datetime(2000, 1, 1)

def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError('ISBN должен содержать 13 символов.')

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey('Publisher',on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    page_count = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name='books')
    tags = models.JSONField(default=list)
    description = models.TextField(max_length=800, blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_short_desc(self):
        if len(self.description) > 280:
            return ' '.join(self.description.split()[:38]) + "..."
        else:
            return f"{self.description}"

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.score}"


class UserLibrary(models.Model):
    STATUS = [
        ('read','Прочитано'),
        ('planned','Хочу прочитать'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    last_change_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} ({self.get_status_display()})"