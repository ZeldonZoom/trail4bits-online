import secrets, os
from PIL import Image
from flask import url_for, current_app
from flaskblog import  mail
from flask_mail import Message

# Function to generate a random 8 digit name for the picture file, returns the new file name.
# and saves the image to the local folder (static/Profile_Pictures) in our case.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/Profile_Pictures', picture_fn)
    

    # Resizing all images to a specific size that is 125x125px and saving resized filed locally.
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore and no changes will be made.    
'''
    mail.send(msg)
