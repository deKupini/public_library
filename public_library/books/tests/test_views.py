import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient

from ..models import Book

client = APIClient()


def test_get_empty_book_list(db):
    response = client.get('/books/')
    assert response.status_code == 200
    assert len(response.data) == 0


def test_get_book_list_with_single_book(book_1, db):
    response = client.get('/books/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0] == {
        'id': '123456',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'borrowed': True,
        'borrow_date': '2022-01-01',
        'borrower': '567890'
    }


def test_get_book_list_with_multiple_books(book_1, book_2, db):
    response = client.get('/books/')
    assert response.status_code == 200
    assert len(response.data) == 2


def test_create_book(db):
    response = client.post('/books/', {
        'id': '123456',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
    })
    assert response.status_code == 201
    assert Book.objects.count() == 1


def test_create_book_with_duplicate_id(book_1, db):
    response = client.post('/books/', {
        'id': '123456',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
    })
    assert response.status_code == 400
    assert not Book.objects.count == 1


def test_create_book_with_too_short_id(db):
    response = client.post('/books/', {
        'id': '12345',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
    })
    assert response.status_code == 400
    assert not Book.objects.count()


def test_create_book_with_non_digit_id(db):
    response = client.post('/books/', {
        'id': 'ABCDEF',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
    })
    assert response.status_code == 400
    assert not Book.objects.count()


@pytest.mark.parametrize('field', ['id', 'title', 'author'])
def test_create_book_with_blank_fields(field, db):
    data = {
        'id': '123456',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
    }
    data[field] = ''
    response = client.post('/books/', data)
    assert response.status_code == 400
    assert not Book.objects.count()


def test_delete_book(book_1, db):
    response = client.delete('/books/123456/')
    assert response.status_code == 204
    assert not Book.objects.filter(id='123456').exists()


def test_delete_non_existing_book(db):
    response = client.delete('/books/123456/')
    assert response.status_code == 404
    assert not Book.objects.filter(id='123456').exists()


@freeze_time("2022-01-01")
def test_borrow_book(book_2, db):
    client.patch('/books/789012/borrow/', {'borrower': '123456'})
    book = Book.objects.get(id='789012')
    assert book.borrowed
    assert book.borrow_date.strftime('%Y-%m-%d') == '2022-01-01'
    assert book.borrower == '123456'


def test_borrow_non_existing_book(db):
    response = client.patch('/books/123456/borrow/', {'borrower': '123456'})
    assert response.status_code == 404


def test_borrow_already_borrowed_book(book_1, db):
    response = client.patch('/books/123456/borrow/', {'borrower': '123456'})
    assert response.status_code == 400
    book = Book.objects.get(id='123456')
    assert book.borrowed
    assert book.borrow_date.strftime('%Y-%m-%d') == book_1.borrow_date
    assert book.borrower == book_1.borrower
