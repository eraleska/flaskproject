from flask_mail import Message
from app import mail
from app import app
from flask import render_template, request, redirect, flash, url_for
from .forms import LoginForm, RegistrationForm, UserForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Posts
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import smtplib

@app.route('/posts')
@login_required
def posts():
    user = current_user
    posts = Posts.query.order_by(Posts.date_added)
    return render_template('index.html', user=user, posts=posts)


@app.route('/')
def hello():
    username = request.args.get('name')
    return render_template('hello.html', name=username)


@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data,
                     poster_id=poster, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash('You submit the post!')
    return render_template('add_post.html', form=form)


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for('edit_post', id=post.id))
    if current_user.id == post.poster.id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form, post=post)
    else:
        flash("Why are you trying to delete not your post?")
        posts = Posts.query.order_by(Posts.date_added)
        return render_template('index.html', posts=posts)

@app.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post was deleted")
            posts = Posts.query.order_by(Posts.date_added)
            return render_template('index.html', posts=posts)
        except:
            flash("Some problems occur. Try again!")
            posts = Posts.query.order_by(Posts.date_added)
            return render_template('index.html', posts=posts)
    else:
        flash("Hmmm.. This is not your post.. You can't delete it")
        posts = Posts.query.order_by(Posts.date_added)
        return render_template('index.html', posts=posts)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserForm()
    id = current_user.id
    name_to_update = User.query.get_or_404(id)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if request.method == 'POST':
            name_to_update.username = request.form['username']
            name_to_update.email = request.form['email']
            name_to_update.profile_pic = request.files['profile_pic']
            name_to_update.age = request.form['age']
            if request.files['profile_pic']:
                name_to_update.profile_pic = request.files['profile_pic']
                # grab profile pic
                pic_filename = secure_filename(name_to_update.profile_pic.filename)
                # set uuid
                pic_name = str(uuid.uuid1()) + '_' + pic_filename
                # save
                saver = request.files['profile_pic']
                # change to a string
                name_to_update.profile_pic = pic_name
                # if user.username == form.username.data or email == form.email.data:
                #     flash('Such username or password already exists')
                #     return redirect(url_for("account"))
                try:
                    db.session.commit()
                    saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                    flash('User updated successfully!')
                    return render_template('profile.html', form=form, name_to_update=name_to_update, id=id)
                except:
                    flash('Error here! Try again')
                    return render_template('profile.html', form=form, name_to_update=name_to_update, id=id)
            else:
                db.session.commit()
                flash('User updated successfully!')
                return render_template('profile.html', form=form, name_to_update=name_to_update, id=id)
        else:
            return render_template('profile.html', form=form, name_to_update=name_to_update, id=id)
    return render_template('profile.html', form=form, name_to_update=name_to_update, id=id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ivalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=True)
        return redirect(url_for("posts"))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, date_added=datetime.now())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete')

        msg = Message("Test message", sender="flasktestiis@yandex.ru", recipients=[request.form.get("email")])
        msg.body = "Thanks for registration"
        msg.html = "<h1>Yay</h1>"
        mail.send(msg)

        return redirect(url_for("login"))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    our_users = User.query.order_by(User.date_added)
    if request.method == 'POST':
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('User updated successfully!')
            return render_template('update.html', form=form, name_to_update=name_to_update, our_users=our_users, id=id)
        except:
            flash('Error here! Try again')
            return render_template('update.html', form=form, name_to_update=name_to_update, our_users=our_users, id=id)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, our_users=our_users, id=id)
