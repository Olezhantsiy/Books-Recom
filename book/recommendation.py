import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from .models import Rating, Book
import os

def generate_recommendations(book_title, top_n=10):
    books = Book.objects.all()
    titles = [book.title for book in books]
    combined_features = [
        f"{book.title} {book.author.name} {', '.join([genre.name for genre in book.genres.all()])} {', '.join(book.tags)} " #{book.description or ''}
        for book in books
    ]

    # Проверяем, существует ли введённый заголовок
    close_match = difflib.get_close_matches(book_title, titles, n=1)
    if not close_match:
        return f"No recommendations found for '{book_title}'."

    # Выбранное совпадение
    selected_title = close_match[0]

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)

    similarity = cosine_similarity(feature_vectors)

    selected_index = titles.index(selected_title)
    similarity_scores = list(enumerate(similarity[selected_index]))

    sorted_similar_books = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for index, score in sorted_similar_books[1:top_n + 1]:  # Пропускаем саму книгу
        book = books[index]
        recommendations.append({
            'id':book.id,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher.name,
            'publication_date': book.publication_date,
            'page_count': book.page_count,
            'genres': [genre.name for genre in book.genres.all()],
            'tags': book.tags,
            'description': book.description,
            'image': book.image if book.image else None
        })

    return recommendations

def load_model():
    return joblib.load('book/models/best_model.pkl')


# Получение рекомендаций для пользователя
def generate_collab_recommendations(user_id, num_recommendations=10):
    model = load_model()

    rated_books = Rating.objects.filter(user_id=user_id)
    rated_book_ids = rated_books.values_list('book_id', flat=True)

    recommendations = []
    for book in Book.objects.exclude(id__in=rated_book_ids):
        est = model.predict(uid=user_id, iid=book.id).est
        recommendations.append((book.id, est))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    top_books = [Book.objects.get(id=book_id) for book_id, _ in recommendations[:num_recommendations]]
    return top_books