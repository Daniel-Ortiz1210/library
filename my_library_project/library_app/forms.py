from django import forms
from django.contrib.auth.models import User
from .models import Book

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, required=True)
    email = forms.EmailField(max_length=100, min_length=10, required=True)
    password = forms.CharField(max_length=50, min_length=10, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se ha registrado')
        else:
            return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se ha registrado')
        else:
            return email
    
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
            )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, required=True)
    password = forms.CharField(max_length=50, min_length=5, required=True)


class NewBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    pub_date = forms.DateField()
    genre = forms.CharField()
    isbn = forms.CharField()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError('Este libro ya se ha registrado')
        else:
            return title
    
    def save(self):
        book = Book.objects.create(
            title=self.cleaned_data.get('title'),
            author=self.cleaned_data.get('author'),
            pub_date=self.cleaned_data.get('pub_date'),
            genre=self.cleaned_data.get('genre'),
            isbn=self.cleaned_data.get('isbn')
        )
        book.save()
        return book


class UpdateBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField(required=False)
    pub_date = forms.DateField(required=False)
    genre = forms.CharField(required=False)
    isbn = forms.CharField(required=False)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError('Este libro ya se ha registrado')
    
    def save(self, book):
        book.title = self.cleaned_data['title']
        #book.author = self.cleaned_data.get('author')
        #book.pub_date = self.cleaned_data('pub_date')
        #book.isbn = self.cleaned_data.get('isbn')
        #book.genre = self.cleaned_data.get('genre')
        book.save()
        return book