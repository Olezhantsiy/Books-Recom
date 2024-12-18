import os
import pandas as pd
import requests
from datetime import datetime
from urllib.parse import quote
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import json
from book.models import Book, Author, Publisher, Genre
import re

def normalize_title(title):
    title = title.strip()
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[\s_-]+', '_', title)
    return title

def get_or_create_author(name):
    author, created = Author.objects.get_or_create(name=name)
    return author

def get_or_create_publisher(name):
    publisher, created = Publisher.objects.get_or_create(name=name)
    return publisher

def get_or_create_genre(name):
    genre, created = Genre.objects.get_or_create(name=name)
    return genre

def parse_date(date_str):
    if isinstance(date_str, str):
        try:
            date_str = date_str.replace('января', 'January').replace('февраля', 'February').replace('марта', 'March') \
                .replace('апреля', 'April').replace('мая', 'May').replace('июня', 'June') \
                .replace('июля', 'July').replace('августа', 'August').replace('сентября', 'September') \
                .replace('октября', 'October').replace('ноября', 'November').replace('декабря', 'December')

            return datetime.strptime(date_str, '%d %B %Y')
        except ValueError:
            return datetime(2010, 10, 20)
    return datetime(2010, 10, 20)


class Command(BaseCommand):
    help = 'Импортирует книги и связанные с ними данные из CSV файла'

    # Функция для обработки жанров
    def handle_genres(self, row):
        genres_data = row['genre']
        genres = []

        try:
            genre_list = json.loads(genres_data)  # Парсим строку жанров
            for genre_dict in genre_list:
                if 'genre' in genre_dict:
                    genre_name = genre_dict['genre']
                    genre = get_or_create_genre(genre_name)  # Получаем или создаем жанр
                    genres.append(genre)
        except (json.JSONDecodeError, KeyError) as e:
            self.stdout.write(f"Error parsing genres for {row['title']}: {e}")

        return genres

    def handle(self, *args, **kwargs):
        # Чтение данных из CSV
        data = pd.read_csv('https://fm.azrail.xyz/uploads/Oleja/books-catalog_detective.csv')

        # Проверка на пропущенные значения
        self.stdout.write(str(data.isna().sum()))

        # Переименование колонок
        data.rename(columns={'namebook': 'title', 'date': 'publication_date'}, inplace=True)

        # Удаление ненужных колонок
        data.drop(columns=['web-scraper-order', 'web-scraper-start-url', 'book-link-href'], inplace=True)

        # Преобразование дат в столбце publication_date
        data['publication_date'] = data['publication_date'].apply(parse_date)

        # Заполнение пропусков в колонке 'publisher'
        data['publisher'].fillna('Издательство АСТ', inplace=True)

        # Очистка значений в колонке 'page_count'
        data['page_count'] = data['page_count'].str.extract('(\d+)')  # Оставляем только числа
        data['page_count'] = pd.to_numeric(data['page_count'], errors='coerce')  # Преобразуем в числовой тип

        # Скачивание изображений
        image_dir = 'media/book_images'  # Папка с медиа
        os.makedirs(image_dir, exist_ok=True)

        for idx, row in data.iterrows():
            try:
                # Создание или получение автора и издателя
                author = get_or_create_author(row['author'])
                publisher = get_or_create_publisher(row['publisher'])

                # Получаем ISBN, если он есть
                isbn_str = row['isbn'] if 'isbn' in row and pd.notna(row['isbn']) else None
                try:
                    # Попробуем преобразовать ISBN в целое число
                    isbn = int(isbn_str) if isbn_str else None
                except ValueError:
                    isbn = None

                # Обработка тегов
                tags = []
                try:
                    tag_list = json.loads(row['tags'])  # Парсим JSON из строки
                    tags = [tag_dict["tags"] for tag_dict in tag_list if "tags" in tag_dict]
                except (json.JSONDecodeError, KeyError):
                    self.stdout.write(f"Failed to parse tags for {row['title']}, defaulting to empty list.")

                # Создание книги
                book = Book.objects.update_or_create(
                    isbn=isbn,  # Добавляем isbn
                    title=row['title'],
                    author=author,
                    publisher=publisher,
                    publication_date=row['publication_date'],
                    page_count=row['page_count'],
                    description=" ".join([item["description"] for item in json.loads(row['description'])]),
                    tags=tags  # Добавляем список тегов
                )

                # Добавление жанров
                genres = self.handle_genres(row)  # Теперь метод handle_genres вызывается через self
                for genre in genres:
                    book.genres.add(genre)  # Связываем каждый жанр с книгой

                # Скачивание изображений
                img_urls = row['image-src'].split(',')  # Разделяем по запятой
                img_url = img_urls[0].strip()  # Берем первую ссылку и убираем лишние пробелы
                img_name = f"{normalize_title(row['title'])}.jpg"  # Применяем нормализацию к названию книги
                img_path = os.path.join(image_dir, img_name)

                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(img_path, 'wb') as file:
                        file.write(response.content)
                    book.image = f'book_images/{img_name}'  # Указываем путь к изображению
                    book.save()
                    self.stdout.write(f"Downloaded and saved image for {book.title}")
                else:
                    self.stdout.write(f"Failed to download image for {book.title}")

            except IntegrityError as e:
                self.stdout.write(f"Error saving data for {row['title']}: {e}")
            except Exception as e:
                self.stdout.write(f"Failed to process book {row['title']}: {e}")
