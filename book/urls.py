from django.db.backends.utils import names_digest
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.book_test, name='book_test'),
    path('books/<int:page_number>', views.book_list, name='book_catalog'),
    path('books/', views.book_list, name='books_redirect'),
    path('registration/', views.register_page, name='register'),
    path('book/<int:book_id>', views.book, name='book'),
    path('rate-book/', views.rate_book, name='rate_book'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.profile_page, name='profile'),
    path('logout', views.do_logout, name='logout'),
    path('user_library/<int:page_number>', views.library_page, name="user_library" ),
    path('library/add/<int:book_id>', views.library_add, name='library_add'),

    path('library/update_status/', views.update_status, name='update_status'),
    path('library/delete/', views.delete_from_library, name='delete_from_library'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)