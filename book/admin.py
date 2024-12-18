from django.contrib import admin
from .models import Book, Author,Genre, Publisher, Rating, UserLibrary

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Включаем поиск по имени автора

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'publication_date')  # Поля для отображения в списке
    search_fields = ['title', 'isbn']  # Поиск по названию и ISBN книги
    list_filter = ('publisher', 'publication_date')  # Фильтры
    autocomplete_fields = ['author', 'publisher']  # Автозаполнение для связанных полей

class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Поиск по имени издательства

# Регистрируем модели в админке
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(UserLibrary)
