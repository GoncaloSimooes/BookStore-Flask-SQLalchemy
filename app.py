from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data_models import db, Author, Book
import requests

app = Flask(__name__)

# Set the SQLite database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

# Create the SQLAlchemy instance
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.

    If a POST request is received, extract author information from the form,
    use the add_author method from the Author class to add the author to the database,
    and display a success message. For GET requests, render the add_author.html form.

    Returns:
        If POST request: Rendered template with success message.
        If GET request: Rendered add_author.html form.
    """
    if request.method == 'POST':
        # Extract author information from the form
        name = request.form['name']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        date_of_death = datetime.strptime(request.form['date_of_death'], '%Y-%m-%d').date()

        # Use the add_author method from the Author class
        Author.add_author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        # Display success message on the /add_author page
        return render_template('add_author.html', message='Author added successfully!')

    # For GET request, render the add_author.html form
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the database.

    If a POST request is received, extract book information from the form,
    use the add_book method from the Book class to add the book to the database,
    and display a success message. For GET requests, fetch authors' data from the database
    and render the add_book.html form.

    Returns:
        If POST request: Rendered template with success message.
        If GET request: Rendered add_book.html form with authors data.
    """

    if request.method == 'POST':
        # Extract author information from the form
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        # Use the add_book method from the book class
        Book.add_book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)

        # Display success message on the /add_book page
        return render_template('add_book.html', message='Book added successfully!')

    # Fetch authors' data from the database
    authors = Author.query.all()

    # For GET request, render the add_book.html form with the authors data
    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """
    Display a list of books with optional sorting and search functionality.

    Fetch books data from the Book table and optionally filter and sort the books based on
    query parameters. Fetch the book cover images from the Google Books API and prepare
    the data for rendering in the home.html template.

    Returns:
        Rendered home.html template with books data.
    """

    # Get the selected sorting option from the query parameters
    sort_by = request.args.get('sort_by')

    # Get the search query from the query parameters
    search_query = request.args.get('search_query')

    # QUERY the book table to fetch all books data
    books = Book.query.all()

    # Filter the books based on the search query
    if search_query:
        books = [book for book in books if search_query.lower() in book.title.lower() or
                 search_query.lower() in book.author.name.lower()]

    # Sort the books based on the selected option
    if sort_by == 'title':
        books.sort(key=lambda x: x.title)
    elif sort_by == 'author':
        books.sort(key=lambda x: x.author.name)

    # Prepare the books data in a format the Jinja code in the HTML file expects
    books_data = []
    for book in books:
        book_info = {
            'title': book.title,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'author_name': book.author
        }
        # Fetch the book's cover image using Google Books API (change API endpoint if needed)
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{book.isbn}')
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                cover_link = data['items'][0]['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
                book_info['cover_image'] = cover_link
            else:
                book_info['cover_image'] = ''  # Set a default image link if not found
        else:
            book_info['cover_image'] = ''  # Set a default image link if API request fails

        books_data.append(book_info)

    # Pass the books data to the render_template function
    return render_template('home.html', books=books_data)


@app.route('/book/<int:book_id>/delete', methods=['GET'])
def delete_book(book_id):
    """
    Delete books by partial title match.

    If a GET request is received with a delete_query parameter,
    delete books whose titles contain the specified query.
    Redirect to the home page or render the delete_success.html template.

    Returns:
        If books are deleted: Redirect to home page or delete_success.html template.
        If no books are deleted: Rendered delete_success.html template.
    """

    book = Book.query.get(book_id)

    if not book:
        return redirect('/', code=303, message='Book not found!')

    if request.method == 'POST':
        book.delete_book()
        return redirect('/', code=200, message='Book deleted successfully!')

    return render_template('delete_book.html', book=book)


if __name__ == "__main__":
    # Create the tables within a Flask application context
    with app.app_context():
        db.create_all()
    # Start the Flask development server
    # from data_models import Author
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
    app.run(debug=True)