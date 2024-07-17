# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_bcrypt import Bcrypt

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '008df26838fa13e4064b8b3f9b72791f'
bcrypt = Bcrypt(app)

# Configure MySQL connection
# Configure MySQL connection
db_connection = mysql.connector.connect(
    host='mariadb',
    user='root',
    password='root_password',
    database='blog'
)

cursor = db_connection.cursor()

# Route for main page (index.html)
@app.route('/')
def index():
    # Fetch all blog posts from the database
    cursor.execute("SELECT * FROM blog_posts")
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

# Route for login page (login.html)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):
            session['logged_in'] = True
            return redirect(url_for('index2'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Route for page after login (index2.html)
@app.route('/index2')
def index2():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index2.html')
    else:
        return redirect(url_for('login'))

# Route for creating a blog post (create.html)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            # Insert blog post into the database
            cursor.execute("INSERT INTO blog_posts (title, content) VALUES (%s, %s)", (title, content))
            db_connection.commit()
            return redirect(url_for('index'))
        return render_template('create.html')
    else:
        return redirect(url_for('login'))

# Route for sign-up page (signup.html)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'Username already exists. Please choose a different one.'
            return render_template('signup.html', error=error)

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db_connection.commit()

        # Redirect to login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
