from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, NewBookForm, UpdateBookForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        '''
        Si el usuario ya se esta autenticado, no tiene caso visitar esta url, lo redirijimos a index
        '''
        return redirect('index')

    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}')
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect('index')
        else:
            messages.error(request, 'No existe un usuario registrado con este username')
            return redirect('login')
    return render(request, 'login.html', {
        'form': form
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user is not None:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
        else:
            messages.error(request, 'No pudimos crear el usuario')
            return redirect('register')
    return render(request, 'register.html', {
        'form': form
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con éxito!')
    return redirect('login')


def index(request):
    return render(request, 'index.html')


def books_list(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


@login_required(login_url='/login')
def add_book(request):

    form = NewBookForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        book = form.save()
        messages.success(request, 'Libro agregado con éxito')
        return redirect('books')
    
    return render(request, 'new-book.html', {'form': form})

# Añadir la vista eliminar
# Barra de busqueda
# Vista de busqeuda

@login_required(login_url='/login')
def update_book(request, book_id):
    book = Book.objects.get(pk=book_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        pub_date = request.POST.get('pub_date')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        isbn = request.POST.get('isbn')
        book.title = title
        book.pub_date = pub_date
        book.author = author
        book.genre = genre
        book.isbn = isbn
        book.save()
        return redirect('books')
    
    return render(request, 'update-book.html')


def search_view(request):

    if request.method == 'GET':
        search = request.GET.get('search')
        books = Book.objects.all()
        filter_books = books.filter(title__icontains=search) | books.filter(author__icontains=search) | books.filter(genre__icontains=search)
        count = filter_books.count()
        return render(request, 'search-results.html', {'books': filter_books, 'search': search, 'count': count})


def delete(request, book_id):
    book = Book.objects.filter(pk=book_id).delete()
    return redirect('index')