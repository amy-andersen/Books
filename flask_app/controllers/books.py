from flask_app import app
from flask import render_template,redirect,request
from flask_app.models import book
from flask_app.models import author

@app.route('/books')
#display all books and a form to add a new book
def books():
    return render_template('books.html', books=book.Book.get_all())

@app.route('/books/<int:id>')
#display one book with author favorites, and a form to add a new favorite author
def one_book(id):
    data = {
        "id": id
    }
    return render_template('one_book.html', book=book.Book.get_book_with_fav_authors(data), unfavorited_authors=author.Author.unfavorited_authors(data))

@app.route('/book_new', methods=["POST"])
#post method to add a new book
def new_book():
    data = {
        "title": request.form["title"],
        "num_of_pages": request.form["num_of_pages"]
    }
    book.Book.save(data)
    return redirect(f'/books'/{request.form["book_id"]})