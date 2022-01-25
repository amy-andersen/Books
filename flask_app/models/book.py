from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

#initiate class
class Book:
    def __init__(self, data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = [] #a list to show which authors have favorited a specific book

    schema_name = "books_schema"

#return all books from db
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
#call the connectToMySQL function with the target schema
        results = connectToMySQL(cls.schema_name).query_db(query)
# Create an empty list to append instances of books
        books = []
# Iterate over the db results and create instances of books
        for book in results:
            books.append( cls(book) )
        return books

#add a new book to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO books ( title , num_of_pages , created_at, updated_at ) VALUES ( %(title)s , %(num_of_pages)s , NOW() , NOW() );"
        return connectToMySQL(cls.schema_name).query_db( query, data )

#find the books that are not already favorited by the author
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"
        results = connectToMySQL(cls.schema_name).query_db(query,data)
        books = []
        for db_row in results:
            books.append(cls(db_row))
        print(books)
        return books

#return one book from database with all favorite authors
    @classmethod
    def get_book_with_fav_authors( cls, data ):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db( query, data )
        print(results)
        #results will be a list of book objects with the favorite authors attached to each row
        book = cls( results[0] )
        for db_row in results:
            author_data = {
                "id": db_row["authors.id"],
                "name": db_row["name"],
                "created_at": db_row["authors.created_at"],
                "updated_at": db_row["authors.updated_at"]
            }
            book.authors_who_favorited.append( author.Author( author_data ))
        return book