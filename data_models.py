
"""
data_models.py - Define SQLAlchemy data models for the library application.

This module defines the SQLAlchemy models `Author` and `Book` for the library application.
It provides methods for adding authors and books to the database, and deleting books.

Attributes:
    db: The SQLAlchemy instance used for database interactions.

Classes:
    Author: Represents an author in the database.
    Book: Represents a book in the database.
"""
# data_models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):

    """
    Represents an author in the database.

    Attributes:
        id (int): The primary key for the author.
        name (str): The name of the author.
        birth_date (datetime.date): The birth date of the author.
        date_of_death (datetime.date): The date of death of the author.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        # return f"Author(id={self.id}, name='{self.name}', birth_date={self.birth_date}, date_of_death={self.date_of_death})"
        return f"{self.name}"

    @classmethod
    def add_author(cls, name, birth_date, date_of_death):
        """
        Add a new author to the database.

        Args:
            name (str): The name of the author.
            birth_date (datetime.date): The birth date of the author.
            date_of_death (datetime.date): The date of death of the author.

        Returns:
            Author: The newly created Author instance.
        """

        # Create a new Author record in the database
        author = cls(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        return author


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (int): The primary key for the book.
        isbn (str): The ISBN of the book.
        title (str): The title of the book.
        publication_year (int): The publication year of the book.
        author_id (int): The foreign key referencing the author of the book.
        author (Author): The Author instance associated with the book.
    """

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('book', lazy=True))

    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', publication_year={self.publication_year}, author_id={self.author_id})"

    @classmethod
    def add_book(cls, title, isbn, publication_year, author_id):
        """
        Add a new book to the database.

        Args:
            title (str): The title of the book.
            isbn (str): The ISBN of the book.
            publication_year (int): The publication year of the book.
            author_id (int): The foreign key referencing the author of the book.

        Returns:
            Book: The newly created Book instance.
        """

        # Create a new Book record in the database
        book = cls(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        return book

    def delete_book(self):
        """
        Delete the book from the database.

        Deletes the current book instance from the database.

        Returns:
            None
        """
        db.session.delete(self)
        db.session.commit()