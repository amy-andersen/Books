from flask_app import app
from flask import render_template,redirect,request
from flask_app.models import author
from flask_app.models import book

@app.route('/authors')
#display all authors and a form to add a new author
def authors():
    return render_template('authors.html', authors=author.Author.get_all())

@app.route('/authors/<int:id>')
#display one author and all their favorite books, and a form to add a new favorite book
def one_author(id):
    data = {
        "id": id
    }
    return render_template('one_author.html', author=author.Author.get_author_with_fav_books(data), unfavorited_books=book.Book.unfavorited_books(data))

@app.route('/author_new', methods=["POST"])
#post method to add a new author
def new_author():
    data = {
        "name": request.form["name"]
    }
    author.Author.save(data)
    return redirect('/authors')

@app.route('/new_favorite_book', methods=["POST"])
#post method to add author's new favorite book 
def new_fav_book():
    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }
    author.Author.save_new_fav(data)
    return redirect(f'/authors/{request.form["author_id"]}')