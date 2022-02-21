from flask import Flask, render_template, redirect, url_for, jsonify, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['DEBUG'] = True
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "date": self.date,
            "body": self.body,
            "author": self.author,
            "img_url": self.img_url,
        }


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    #body = StringField("Blog Content", validators=[DataRequired()])
    body = CKEditorField("Body")
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    all_posts = []
    for post in posts:
        all_posts.append(post.to_dict())
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = BlogPost.query.get(post_id)
    requested_post = post.to_dict()
    #return jsonify(requested_post)
    return render_template("post.html", post=post)


@app.route("/new-post", methods=['POST'])
def new_post():
    my_post = BlogPost()
    my_post.title = request.form["title"]
    my_post.subtitle = request.form["subtitle"]
    my_post.date = datetime.datetime.today()
    my_post.body = request.form["body"]
    my_post.author = request.form["author"]
    my_post.img_url = request.form["img_url"]
    db.session.add(my_post)
    db.session.commit()
    # return jsonify(my_post.to_dict())
    return render_template("make-post.html")


@app.route("/edit-post/<int:post_id>", methods=['GET'])
def edit_post(post_id):
    if request.get == "GET":
        edit_this_post = BlogPost.query.get(post_id)
        edit_this_post.body = request.form["body"]
        db.session.commit()
        return render_template("post.html", post=edit_this_post)

@app.route("/delete/<int:post_id>", methods=['GET'])
def delete_post(post_id):
    delete_this_post = BlogPost.query.get(post_id)
    db.session.delete(delete_this_post)
    db.session.commit()
    # return jsonify(delete_post.to_dict())
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not path:
        path = "index.html"

    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)