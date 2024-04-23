from django.contrib import admin

from Author.models import Book, Author
# Register your models here.


admin.site.register(Author)
admin.site.register(Book)