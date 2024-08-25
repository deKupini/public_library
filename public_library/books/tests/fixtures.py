import pytest

from ..models import Book


@pytest.fixture
def book_1(db):
    return Book.objects.create(
        id=123456,
        title='The Great Gatsby',
        author='F. Scott Fitzgerald',
        borrowed=True,
        borrow_date='2022-01-01',
        borrower=567890
    )

@pytest.fixture
def book_2(db):
    return Book.objects.create(
        id=789012,
        title='To Kill a Mockingbird',
        author='Harper Lee',
        borrowed=False
    )