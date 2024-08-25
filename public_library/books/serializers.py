from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author')

    def validate_id(self, value):
        if len(value) != 6:
            raise serializers.ValidationError('ID must be 6 characters long')
        if not value.isdigit():
            raise serializers.ValidationError('ID must be a number')
        return value
