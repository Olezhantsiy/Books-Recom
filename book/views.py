from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
from numpy.ma.core import count
from urllib.parse import unquote
from django.core.cache import cache
from .models import Book, UserLibrary, Rating, Author, Genre, Publisher
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .forms import LoginForm, RegisterForm
from .recommendation import generate_recommendations, generate_collab_recommendations
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
import json

def book_test(request):
    books = Book.objects.all()

    popular_books = Book.objects.annotate(rating_count=Count('rating')).order_by('-rating_count')[:8]

    top_rated_books = Book.objects.annotate(average_rating=Avg('rating__score')).order_by('-average_rating')[:8]

    new_books = Book.objects.order_by('-publication_date')[:8]
    russian_classics = Book.objects.filter(genres__name='Русская классика')[:8]

    if request.user.is_authenticated:
        cache_key = f'recommendations_{request.user.id}'
        recommended_books = cache.get(cache_key)
        if not recommended_books:
            recommended_books = generate_collab_recommendations(request.user)
            cache.set(cache_key, recommended_books, 60*60)
    else:
        recommended_books = []

    context = {
        'books': books,
        'popular_books': popular_books,
        'top_rated_books': top_rated_books,
        'new_books': new_books,
        'russian_classics': russian_classics,
        'recommended_books': recommended_books
    }

    return render(request, 'book/book_main.html', context)

def book_search_test(request, page_number=None, search_title=None):
    if page_number is None:
        return redirect('books', page_number=1)

    books = Book.objects.filter(title__contains=search_title)

    per_page = 10
    paginator = Paginator(books, per_page)
    books_paginator = paginator.get_page(page_number)

    current_page = books_paginator.number
    total_pages = books_paginator.paginator.num_pages
    page_range = range(
        max(1, current_page - 2),
        min(total_pages, current_page + 2) + 1
    )

    user_library = {}
    if request.user.is_authenticated:
        user_library = UserLibrary.objects.filter(user=request.user).values_list('book_id', flat=True)

    context = {
        'books': books_paginator,
        'page_range': page_range,
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
        'user_library': user_library,
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'book/book_list.html', context)

def book_list(request, page_number=None):
    if page_number is None:
        return redirect('books', page_number=1)

    author_ids = request.GET.getlist('authors')
    genre_ids = request.GET.getlist('genres')
    publisher_ids = request.GET.getlist('publishers')
    search_title = request.GET.get('search', '')
    search_title = unquote(search_title)

    books = Book.objects.annotate(average_rating=Avg('rating__score')).order_by('id')

    if author_ids:
        books = books.filter(author__id__in=author_ids)
    if genre_ids:
        books = books.filter(genres__id__in=genre_ids)
    if publisher_ids:
        books = books.filter(publisher__id__in=publisher_ids)

    if search_title:
        search_title = search_title.replace('+', ' ')
        books = books.filter(title__icontains=search_title)


    per_page = 10
    paginator = Paginator(books, per_page)
    books_paginator = paginator.get_page(page_number)

    current_page = books_paginator.number
    total_pages = books_paginator.paginator.num_pages
    page_range = range(
        max(1, current_page - 2),
        min(total_pages, current_page + 2) + 1
    )

    user_library = {}
    if request.user.is_authenticated:
        user_library = UserLibrary.objects.filter(user=request.user).values_list('book_id', flat=True)

    context = {
        'books': books_paginator,
        'page_range': page_range,
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
        'user_library': user_library,
        'publishers': Publisher.objects.all(),
        'selected_authors': author_ids,
        'selected_genres': genre_ids,
        'selected_publishers': publisher_ids,
        'search_title': search_title
    }
    return render(request, 'book/book_list.html', context)

def book(request, book_id):
    book_info = get_object_or_404(Book, id=book_id)
    rating_objs = Rating.objects.filter(book_id=book_id)
    rating_count = rating_objs.count()
    average_rating = rating_objs.aggregate(Avg('score'))['score__avg']

    recommendations_books = generate_recommendations(book_info.title, 10)

    print(recommendations_books)

    context = {
        'book': book_info,
        'rating_count': rating_count,
        'average_rating': average_rating,
        'recommendations_books': recommendations_books,
    }
    return render(request, 'book/book.html', context)
@login_required
@csrf_exempt
def rate_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('book_id')
        rating = data.get('rating')
        user = request.user
        print(user, book_id, rating)
        if book_id and rating:
            Rating.objects.update_or_create(user=user, book_id=book_id,defaults={"score": int(rating)})
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
def library_page(request, page_number=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if page_number is None:
        return redirect('user_library', page_number=1)

    user_library = UserLibrary.objects.filter(user=request.user).select_related('book')

    per_page = 10
    paginator = Paginator(user_library, per_page)
    books_paginator = paginator.get_page(page_number)

    current_page = books_paginator.number
    total_pages = books_paginator.paginator.num_pages
    page_range = range(
        max(1, current_page - 2),
        min(total_pages, current_page + 2) + 1
    )

    context = {
        'user_books': books_paginator,
        'page_range': page_range,
    }
    return render(request, 'book/library.html', context)
@csrf_exempt
def library_add(request, book_id):
    print(f"Метод запроса: {request.method}")
    if request.method == 'POST':
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Книга не найдена'}, status=404)

        user_library, created = UserLibrary.objects.get_or_create(user=request.user, book=book)

        if user_library.status == 'planned':
            user_library.status = 'read'
        else:
            user_library.status = 'planned'

        user_library.save()
        return JsonResponse({'status': user_library.status})

    return JsonResponse({'error': 'Invalid request'}, status=400)
def login_page(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('book_test')
            else:
                form.add_error(None, 'Данные введены неверно!')
    return render(request, 'authorarization/login2.html', {'form': form})
def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    return render(request, 'authorarization/register2.html', {'form': form})
def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'authorarization/profile.html', {'user': request.user})
def do_logout(request):
    logout(request)
    return redirect('book_test')
    # return redirect('login')
@login_required
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('book_id')
        new_status = data.get('status')
        try:
            entry = UserLibrary.objects.get(id=book_id, user=request.user)
            entry.status = new_status
            entry.save()
            return JsonResponse({'success': True})
        except UserLibrary.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Книга не найдена'}, status=404)
    return JsonResponse({'success': False}, status=400)
@login_required
def delete_from_library(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('book_id')
        try:
            entry = UserLibrary.objects.get(id=book_id, user=request.user)
            entry.delete()
            return JsonResponse({'success': True})
        except UserLibrary.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Книга не найдена'}, status=404)
    return JsonResponse({'success': False}, status=400)
