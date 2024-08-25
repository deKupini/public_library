from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer, CreateBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookSerializer
        return BookSerializer
