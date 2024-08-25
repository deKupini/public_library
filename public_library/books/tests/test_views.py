from rest_framework.test import APIClient

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
        'id': 123456,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'borrowed': True,
        'borrow_date': '2022-01-01',
        'borrower': 567890
    }


def test_get_book_list_with_multiple_books(book_1, book_2, db):
    response = client.get('/books/')
    assert response.status_code == 200
    assert len(response.data) == 2
