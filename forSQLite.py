from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

dbs = sqlite3.connect("boooks.db")
crsr = dbs.cursor()
crsr.execute("CREATE TABLE IF NOT EXISTS bks (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

crsr.execute("INSERT INTO bks VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
dbs.commit()

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

