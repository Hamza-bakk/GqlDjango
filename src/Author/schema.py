import graphene
from graphene import ResolveInfo

from graphene_django import DjangoObjectType
from .models import Author, Book  
from django.contrib.auth.models import User


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = '__all__'
        
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)
    all_users = graphene.List(UserType)

    def resolve_all_authors(root, info: ResolveInfo):
        return Author.objects.all()

    def resolve_all_books(root, info):
        return Book.objects.all()
    
    def resolve_all_users(root, info):
        return User.objects.all()
    
class CreateAuthor(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    author = graphene.Field(AuthorType)

    def mutate(self, info, first_name, last_name):
        author = Author.objects.create(first_name=first_name, last_name=last_name)
        return CreateAuthor(author=author)
    

class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()

    author = graphene.Field(AuthorType)

    def mutate(self, info, id, first_name=None, last_name=None):
        author = Author.objects.get(pk=id)
        if first_name is not None:
            author.first_name = first_name
        if last_name is not None:
            author.last_name = last_name
        author.save()
        return UpdateAuthor(author=author)

class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    author_id = graphene.ID()

    def mutate(self, info, id):
        author = Author.objects.get(pk=id)
        author.delete()
        return DeleteAuthor(author_id=id)

class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
