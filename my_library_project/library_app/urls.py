from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('books', views.books_list, name="books"),
    path('add-book', views.add_book, name="add_book"),
    path('update-book/<book_id>', views.update_book, name="update_book"),
    path('search-result', views.search_view, name="search_view"),
    path('delete/<book_id>', views.delete, name="delete"),
]