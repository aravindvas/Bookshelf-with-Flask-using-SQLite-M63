from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app=app)

class bookk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)

    def __repr__(self):
        return f'<books {self.title}>'

db.create_all()

new_book = bookk(id=2, title="Harry Potter", author="J. K. Rowling", rating=9.3)
print(new_book)
db.session.add(new_book)
db.session.commit()

all_books = []


@app.route('/')
def home():
    return render_template("index.html", bk=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_bk = {
            "title": request.form["tit"],
            "author": request.form["aut"],
            "rating": request.form["rat"],
        }
        all_books.append(new_bk)
        return redirect(url_for('home'))
    # print(all_books)
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, host="localhost")

