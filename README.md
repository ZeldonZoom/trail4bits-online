# Trail4Bits - Flask Blog Application

A modern, feature-rich blogging platform built with Flask, allowing users to create, manage and share their posts while maintaining their personal profiles.

## Features

- **User Authentication**
  - User registration with email verification
  - Secure login/logout functionality
  - Password reset capability via email
  
- **User Profiles**
  - Customizable profile pictures
  - User bio and information management
  - Account settings management
  
- **Blog Posts**
  - Create, read, update, and delete posts
  - Rich text content support
  - Post timestamps and author attribution
  
- **UI/UX**
  - Responsive design using Bootstrap 4
  - Clean and intuitive interface
  - Flash messages for user feedback
  - Sidebar with quick access to latest posts and announcements

## Technology Stack

- **Backend**
  - Flask 3.0.0
  - SQLAlchemy 2.0.22
  - Flask-Login 0.6.2
  - Flask-Mail 0.9.1
  - Flask-Bcrypt 1.0.1
  
- **Frontend**
  - Bootstrap 4.0.0
  - HTML5/CSS3
  - jQuery 3.2.1
  
- **Database**
  - SQLAlchemy ORM
  
## Installation

1. Clone the repository:
```bash
git clone https://github.com/schadenfroid/trail4bits-online.git
cd trail4bits-online
```
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Create a configuration file at /etc/config.json with the following structure:
```bash
{
    "SECRET_KEY": "your-secret-key",
    "SQLALCHEMY_DATABASE_URI": "your-database-uri",
    "EMAIL_USER": "your-email@example.com",
    "EMAIL_PASS": "your-email-password"
}
```
4. Run the application:
```bash
python run.py
```

## Usage
1. Register a new account using your email address
2. Verify your email address through the verification link
3. Log in to your account
4. Customize your profile with a picture and bio
5. Start creating and sharing posts
6. Explore other users' posts on the home page

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Flask documentation and community
- Bootstrap team for the excellent UI framework
- Flask documentation and community
- Corey Schafer for his Flask YouTube playlist, which provided invaluable guidance and inspiration for this project
- All contributors who help improve this project
