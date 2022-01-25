from flask_app import app

#import classes
from flask_app.controllers import books, authors

if __name__ == "__main__":
    app.run(debug=True)