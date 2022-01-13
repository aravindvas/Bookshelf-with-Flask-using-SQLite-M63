from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/')
def home():
    all_b = db.session.query(Book).all()
    return render_template("index.html", bk=all_b)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_bk = Book(
            title= request.form["tit"],
            author= request.form["aut"],
            rating= request.form["rat"],
        )
        db.session.add(new_bk)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route('/editt', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        bk_id = request.form["id"]
        bk_to_upd = Book.query.get(bk_id)
        bk_to_upd.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    bk_id = request.args.get('id')
    bk_selected = Book.query.get(bk_id)
    return render_template("edit.html", bok=bk_selected)

@app.route("/deletee")
def delete():
    bk_id2 = request.args.get('id2')
    bk_to_del = Book.query.get(bk_id2)
    db.session.delete(bk_to_del)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True, host="localhost")

