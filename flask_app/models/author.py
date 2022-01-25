from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

#initiate class
class Author:
    def __init__(self, data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fav_books = [] #a list to show which are the favorite books of this author

    schema_name = "books_schema"

#return all authors from db
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
#call the connectToMySQL function with the target schema
        results = connectToMySQL(cls.schema_name).query_db(query)
# Create an empty list to append instances of authors
        authors = []
# Iterate over the db results and create instances of authors
        for author in results:
            authors.append( cls(author) )
        return authors

#add a new author to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO authors ( name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        return connectToMySQL(cls.schema_name).query_db( query, data )

#keep track of which authors are not already favorites of a book 
    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        authors = []
        results = connectToMySQL(cls.schema_name).query_db(query,data)
        for db_row in results:
            authors.append(cls(db_row))
        return authors

#add an author's new favorite book to db
    @classmethod
    def save_new_fav(cls, data):
        query = "INSERT INTO favorites ( author_id, book_id , created_at, updated_at ) VALUES ( %(author_id)s , %(book_id)s , NOW() , NOW() );"
        return connectToMySQL(cls.schema_name).query_db( query, data )

#return one author from database with all their favorite books
    @classmethod
    def get_author_with_fav_books( cls, data ):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db( query, data )
        print(results)
        #results will be a list of author objects with the favorite books attached to each row
        author = cls( results[0] )
        for db_row in results:
            book_data = {
                "id": db_row["books.id"],
                "title": db_row["title"],
                "num_of_pages": db_row["num_of_pages"],
                "created_at": db_row["books.created_at"],
                "updated_at": db_row["books.updated_at"]
            }
            author.fav_books.append( book.Book( book_data ))
        return author