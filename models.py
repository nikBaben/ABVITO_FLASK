from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    about = db.Column(db.String,nullable=False)
    name_item = db.Column(db.String,nullable=False)
    adress = db.Column(db.String,nullable=False)


class Goga(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime(True), nullable=False, server_default=db.func.now(tz='UTC'))
    author_id = db.Column(db.Integer, db.ForeignKey('goga.id'))
    address = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String)




    author = db.relationship('Goga', backref=db.backref('articles', lazy=True))
    category = db.relationship('Category', backref=db.backref('articles', lazy=True))




