from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, CreateBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookSerializer
        return BookSerializer

    @action(detail=True, methods=['patch'])
    def borrow(self, request, pk):
        book = self.get_object()
        if book.borrowed:
            return Response({'message': 'Book already borrowed'}, status=400)
        book.borrower = request.data['borrower']
        book.borrow_date = datetime.now().date()
        book.borrowed = True
        book.save()
        return Response({'message': 'Book borrowed successfully'}, status=200)

    @action(detail=True, methods=['patch'])
    def return_(self, request, pk):
        book = self.get_object()
        if not book.borrowed:
            return Response({'message': 'Book not borrowed'}, status=400)
        book.borrower = None
        book.borrow_date = None
        book.borrowed = False
        book.save()
        return Response({'message': 'Book returned successfully'}, status=200)
