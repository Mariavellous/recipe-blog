from flask import Flask, render_template, redirect, url_for, jsonify, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime
import requests


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['DEBUG'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)
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
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    #body = StringField("Blog Content", validators=[DataRequired()])
    body = CKEditorField("Body")
    submit = SubmitField("Submit Post")


def make_new_post(form, post_id):
    post = BlogPost() if post_id is None else BlogPost.query.get(post_id)
    post.title = form.title.data
    post.subtitle = form.subtitle.data
    post.body = form.body.data
    post.author = form.author.data
    post.img_url = form.img_url.data
    post.date = datetime.datetime.today().strftime("%B %d, %Y")
    return post

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


@app.route("/new-post", methods=['GET', 'POST'])
def new_post():
    # db.session.add(my_post)
    # db.session.commit()
    form = CreatePostForm()
    if form.validate_on_submit():
        post = make_new_post(form, post_id=None)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == "GET":
        post = BlogPost.query.get(post_id)
        form = CreatePostForm()
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.author.data = post.author
        form.img_url.data = post.img_url
        form.body.data = post.body
        return render_template("make-post.html", form=form)
    post = make_new_post(CreatePostForm(),post_id)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)