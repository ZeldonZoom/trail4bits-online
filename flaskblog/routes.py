import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistraionForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, bcrypt, db
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    posts  = Post.query.all()
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistraionForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember= form.remember.data)
                # when redirected to login page from any other page this piece of code will redirect to
                # the page you were redirected from, to the login page
                # e.g. trying to access account page without logging in, you'll get redirected to login page
                # and when you'll login you will be redirected back to account page.
                next_page = request.args.get('next')
                return redirect(next_page)  if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Function to generate a random 8 digit name for the picture file, returns the new file name.
# and saves the image to the local folder (static/Profile_Pictures) in our case.

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Profile_Pictures', picture_fn)
    

    # Resizing all images to a specific size that is 125x125px and saving resized filed locally.
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
         if form.picture.data:
              picture_file = save_picture(form.picture.data)
              current_user.image_file = picture_file
         current_user.username = form.username.data
         current_user.email = form.email.data
         db.session.commit()
         flash('Your Account has been updated', 'success')
         return redirect(url_for('account'))
    elif request.method =='GET':
         form.username.data=current_user.username
         form.email.data=current_user.email
    image_file = url_for('static', filename='Profile_Pictures/'+f'{current_user.image_file}')
    return render_template('account.html', title='Account', image_file = image_file, form=form)



# This route directs user to a new page where user can create a new post.
# Uses the create_post.html template
@app.route("/post/new", methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
         post = Post(title=form.title.data, content=form.content.data, author=current_user)
         db.session.add(post)
         db.session.commit()
         flash('Your post has been successfully created!')
         return(redirect(url_for('home')))
    return render_template('create_post.html', title='New post', form=form)


# This route directs user to a new page where user can see the post, (this route gets the post from the db using post_id).
@app.route("/post/<int:post_id>")
def post(post_id):
     post = Post.query.get_or_404(post_id)
     return render_template('post.html', title=post.title, post=post, legend='New Post')


# This route directs user to a new page where user can see and update the post, (gets the post from the db using post_id).
# Uses the same template as create post template.
@app.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    form=PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
         abort(403)
    form.title.data=post.title
    form.content.data=post.content
    return render_template('create_post.html', title='Update Post', post=post, form=form, legend='Update Post')
