from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from library_forms import AuthorForm, BookForm

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
# once script directory is in path, import Contact and ContactForm
from library_forms import BookForm, AuthorForm

# Complete app setup and config
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
# TODO: connect your app to a SQLite database
dbfile = os.path.join(script_dir, "database.sqlite3")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO: add database model for Book
class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    authorID = db.Column(db.Integer, db.ForeignKey('Authors.id'), nullable=False)
    title = db.Column(db.Unicode, nullable=False)
    year = db.Column(db.Unicode, nullable=False)


# TODO: add database model for Author
class Author(db.Model):
    __tablename__ = 'Authors'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.Unicode, nullable=False)
    lastName = db.Column(db.Unicode, nullable=False)
    middleInitial = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    #db.drop_all()

@app.get("/")
def to_lib():
    return redirect(url_for("get_library"))

# TODO: add route to get author form
@app.get('/authors/')
def get_author():
    form = AuthorForm()
    return render_template("get_author.html", form=form)

# TODO: add route to post author form
@app.post('/authors/')
def post_author():
    form = AuthorForm()
    if form.validate():
        # form data is valid
        author = Author(firstName=form.firstName.data, lastName=form.lastName.data, middleInitial=form.middleInitial.data)
        db.session.add(author) 
        db.session.commit()
        return redirect(url_for("get_library"))
    else:
        # form is not valid 
        for field, error, in form.errors.items():
            flash(f"{field}, {error}")
        return redirect(url_for("get_authors"))


# TODO: complete route to get book form
@app.get('/books/')
def get_book_form():
    book_form = BookForm()
    # TODO: get a list of names and ids from the database for author.choices
    book_form.author.choices = [] # TODO: use that list here
    
    authors = Author.query.all()

    for a in authors:
        aid = f'{a.id}'
        author = f'{a.firstName}, {a.middleInitial}, {a.lastName}'
        book_form.author.choices.append((aid, author))
    
    return render_template("get_books.html", form=book_form)

    # author.choices should of type -- list of (value,label) tuples of strings
    #     value -- the value that will be submitted
    #     label -- the user readable name of that option in the dropdown menu
    # HINT: I would suggest a the following value and label
    #     value -- Author.id
    #     label -- Author.firstName Author.middleInitial Author.lastName

# TODO complete route to post book form
@app.post('/books/')
def post_book_form():
    book_form = BookForm()
    book_form.author.choices = []

    authors = Author.query.all()

    for a in authors: # Didn't know that I had to repopulate the []
        aid = f'{a.id}'
        author = f'{a.firstName}, {a.middleInitial}, {a.lastName}'
        book_form.author.choices.append((aid, author))

    # TODO: get a list of names and ids from the database for author.choices
    if book_form.validate(): 
        #book_form.author.choices = [] # TODO: use that list here
        book = Book(authorID=book_form.author.data, title=book_form.title.data, year=book_form.year.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("get_library"))  
    else:
        print(book_form.author.data, type(book_form.author.data))
        for field, error, in book_form.errors.items():
            flash(f"{field}, {error}")
        return redirect(url_for("get_book_form"))
    

    # author.choices should of type -- list of (value,label) tuples of strings
    #     value -- the value that will be submitted
    #     label -- the user readable name of that option in the dropdown menu
    # HINT: I would suggest a the following value and label
    #     value -- Author.id
    #     label -- Author.firstName Author.middleInitial Author.lastName

# TODO: add route to get list of books
@app.get("/library/")
def get_library():
    # get all books
    books = Book.query.all()
    library = []
    # get authors representing those books
    for b in books:
        author = Author.query.get_or_404(b.authorID)
        print(author)
        library.append((b, author))

    return render_template("get_library.html", library=library)

