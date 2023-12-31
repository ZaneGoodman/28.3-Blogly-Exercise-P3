"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///Blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


from flask_debugtoolbar import DebugToolbarExtension

app.config["SECRET_KEY"] = "SECRET!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)


# routes for user table
@app.route("/")
def user_list():
    """List users"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/", methods=["POST"])
def add_user():
    """Retrieve New user from form data & add to db"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route("/user-details/<int:user_id>")
def user_details(user_id):
    """shows user details"""
    user = User.query.get(user_id)
    post = Post.query.filter(Post.user_id == user_id).all()
    return render_template("details.html", user=user, post=post)


@app.route("/user-details/<int:user_id>/edit")
def edit_user(user_id):
    """directed to user edit form"""
    user = User.query.get(user_id)

    return render_template("edit_user.html", user=user)


@app.route("/user-details/<int:user_id>/edit", methods=["POST"])
def apply_edits_to_user(user_id):
    """Apply changes to user details from edit user form"""
    user = User.query.get(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    db.session.add(user)
    db.session.commit()
    return redirect(f"/user-details/{user.id}")


@app.route("/user-details/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user"""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect("/")


# Routes for Post table


@app.route("/user-details/<int:user_id>/add-post")
def add_post_form(user_id):
    """Sends user to form to add a post"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("create_post.html", user=user, tags=tags)


@app.route("/user-details/<int:user_id>/add-post", methods=["POST"])
def add_post(user_id):
    """Retrieve New post information and update db"""

    title = request.form["title"]
    content = request.form["content"]
    selected_tag_ids = request.form.getlist("tag")

    new_post = Post(title=title, content=content, user_id=user_id)
    # Using the tag_id's retrieved from the checkboxed tags grab the full tag object and append to the post #
    for tag_id in selected_tag_ids:
        tag = Tag.query.get(tag_id)
        new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user-details/{user_id}")


@app.route("/user-details/<int:user_id>/<int:post_id>")
def user_post(user_id, post_id):
    """Look at full post"""

    user = User.query.get(user_id)

    post = Post.query.get(post_id)

    tags = post.tags

    return render_template("post.html", user=user, post=post, tags=tags)


@app.route("/user-details/<int:user_id>/<int:post_id>/edit-post")
def edit_post(user_id, post_id):
    """Show edit form"""
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", user=user, post=post, tags=tags)


@app.route("/user-details/<int:user_id>/<int:post_id>/edit-post", methods=["POST"])
def apply_edits_to_post(user_id, post_id):
    """Look at full post"""

    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    title = request.form["title"]
    content = request.form["content"]
    selected_tag_ids = request.form.getlist("tag")

    post.title = title
    post.content = content
    # Using the tag_id's retrieved from the checkboxed tags grab the full tag object and append to the post #
    for tag_id in selected_tag_ids:
        tag = Tag.query.get(tag_id)
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/user-details/{user.id}/{post.id}")


@app.route("/user-details/<int:user_id>/<int:post_id>/delete-post")
def delete_post(user_id, post_id):
    """Delete post"""
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f"/user-details/{user.id}")


# routes for tags


@app.route("/tags")
def tag_list():
    """Send user to list of tags"""
    tags = Tag.query.all()

    return render_template("tag_list.html", tags=tags)


@app.route("/tags/add-tag")
def add_tag():
    return render_template("create_tag.html")


@app.route("/tags/add-tag", methods=["POST"])
def add_new_tag_to_db():
    new_tag_name = request.form["tag_name"]
    new_tag = Tag(tag_name=new_tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def add_edits_to_tag_list(tag_id):
    tag = Tag.query.get(tag_id)
    edited_tag_name = request.form["tag_name"]
    tag.tag_name = edited_tag_name

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete-tag")
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
