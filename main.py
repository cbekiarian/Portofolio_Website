from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
key =os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = key


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chess', methods = ["GET","POST"])
def chess():

    pieces ='white'
    pieces = request.args.get('pieces')
    return render_template("chess.html", pieces = pieces)

@app.route('/flight-deals', methods=["GET","POST"])
def flights():
    return render_template("flights.html")



if __name__ == "__main__":
    app.run(debug=True, port=5001)
