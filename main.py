
from flask import Flask, render_template, redirect, url_for, jsonify, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import TIMESTAMP
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import datetime

# Load secrets from .env if present, if not load them from the environment
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["RECIPES_SECRET_KEY"]
app.config['DEBUG'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["RECIPES_DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Create a comment table in DB
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

##CONFIGURE TABLE
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    ingredients = db.Column(db.String(250), nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.datetime.now())
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)



# Create the tables if they don't exist
db.create_all()
db.session.commit()

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Recipe Title", validators=[DataRequired()])
    ingredients = StringField("Ingredients", validators=[DataRequired()])
    img_url = StringField("Recipe Image URL", validators=[DataRequired(), URL()])
    instructions = CKEditorField("Body")
    submit = SubmitField("Submit Post")


def make_new_post(form, post_id):
    post = Recipe() if post_id is None else Recipe.query.get(post_id)
    post.title = form.title.data
    post.ingredients = form.ingredients.data
    post.instructions = form.instructions.data
    post.img_url = form.img_url.data
    return post

@app.route('/')
def get_all_posts():
    posts = Recipe.query.all()
    for post in posts:
        post.user = User.query.filter(User.id == post.user_id).first()
    return render_template("index.html", all_posts=posts)


@app.route("/recipes/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = Recipe.query.get(post_id)
    comments = Comment.query.filter(Comment.recipe_id == post_id).all()
    author = User.query.filter(User.id == post.user_id).first()
    for comment in comments:
        comment.user = User.query.filter(User.id == comment.user_id).first()
    return render_template("post.html", post=post, author=author, comments=comments)


@app.route("/recipes/<int:post_id>/comment", methods=["POST"])
@login_required
def create_comment(post_id):
    new_comment = Comment()
    new_comment.recipe_id = post_id
    new_comment.user_id = current_user.id
    new_comment.body = request.form.get("textarea")
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))




@app.route("/recipes/new", methods=['GET', 'POST'])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = make_new_post(form, post_id=None)
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)


@app.route("/recipes/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == "GET":
        post = Recipe.query.get(post_id)
        form = CreatePostForm()
        form.title.data = post.title
        form.ingredients.data = post.ingredients
        form.img_url.data = post.img_url
        form.instructions.data = post.instructions
        return render_template("make-post.html", form=form)
    make_new_post(CreatePostForm(), post_id)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

@app.route("/recipes/<int:post_id>/delete", methods=['GET'])
def delete_post(post_id):
    delete_this_post = Recipe.query.get(post_id)
    db.session.delete(delete_this_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))



@app.route("/about")
def about():
    return render_template("about.html")


### Register and Login Users

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        new_user = User()
        new_user.name = request.form.get('name')
        password = str(request.form.get('password'))
        new_user.password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
        new_user.email = request.form.get('email')

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get('email')
        password = str(request.form.get('password'))
        user = User.query.filter(User.email == email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("get_all_posts"))
        else:
            return render_template("login.html")

# User Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)