import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import book_app
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    # Reset the global collection for each test
    book_app.collection = BookCollection()


def test_handle_list_unread_empty(capsys):
    """handle_list_unread displays 'No books found' when collection is empty."""
    book_app.handle_list_unread()
    captured = capsys.readouterr()
    assert "No books found." in captured.out


def test_handle_list_unread_shows_unread_only(capsys):
    """handle_list_unread displays only unread books."""
    book_app.collection.add_book("Read Book", "Author One", 2020)
    book_app.collection.add_book("Unread Book", "Author Two", 2021)
    book_app.collection.mark_as_read("Read Book")
    
    book_app.handle_list_unread()
    captured = capsys.readouterr()
    
    assert "Unread Book" in captured.out
    assert "Read Book" not in captured.out
    assert "Your Book Collection:" in captured.out


def test_handle_list_unread_shows_multiple(capsys):
    """handle_list_unread displays all unread books when multiple exist."""
    book_app.collection.add_book("Book A", "Author A", 2020)
    book_app.collection.add_book("Book B", "Author B", 2021)
    book_app.collection.add_book("Book C", "Author C", 2022)
    book_app.collection.mark_as_read("Book B")
    
    book_app.handle_list_unread()
    captured = capsys.readouterr()
    
    assert "Book A" in captured.out
    assert "Book C" in captured.out
    assert "Book B" not in captured.out


def test_handle_list_unread_all_read(capsys):
    """handle_list_unread displays 'No books found' when all books are read."""
    book_app.collection.add_book("Book A", "Author A", 2020)
    book_app.collection.add_book("Book B", "Author B", 2021)
    book_app.collection.mark_as_read("Book A")
    book_app.collection.mark_as_read("Book B")
    
    book_app.handle_list_unread()
    captured = capsys.readouterr()
    assert "No books found." in captured.out


def test_show_books_displays_unread_symbol(capsys):
    """show_books displays empty checkbox for unread books."""
    book_app.collection.add_book("Unread Book", "Author", 2020)
    books_list = book_app.collection.list_unread()
    book_app.show_books(books_list)
    
    captured = capsys.readouterr()
    assert "[ ]" in captured.out  # Space = unread
    assert "Unread Book" in captured.out


def test_show_books_displays_read_symbol(capsys):
    """show_books displays checkmark for read books."""
    book_app.collection.add_book("Read Book", "Author", 2020)
    book_app.collection.mark_as_read("Read Book")
    books_list = book_app.collection.list_books()
    book_app.show_books(books_list)
    
    captured = capsys.readouterr()
    assert "[✓]" in captured.out  # Checkmark = read
    assert "Read Book" in captured.out
