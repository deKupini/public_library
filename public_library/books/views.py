from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, CreateBookSerializer, PartialUpdateBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookSerializer
        if self.action == 'partial_update':
            return PartialUpdateBookSerializer
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
