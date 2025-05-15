from flask import Flask, request, render_template, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chiaNyidindu1'
app.config['MYSQL_DB'] = 'volunteer_hub'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            flash("Please enter both email and password.", "error")
            return render_template('login page.html')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            print("User from DB:", user)
            print("Password from form:", password)
            print("Password hash from DB:", user['password'])
            print("Check hash result:", check_password_hash(user['password'], password))
            cursor.close()
            conn.close()
            if user:
                print("Password from form:", password)
                print("Password hash from DB:", user['password'])
                print("Check hash result:", check_password_hash(user['password'], password))
            if user and check_password_hash(user['password'], password):
                session['user_email'] = user['email']
                flash("Login successful!", "success")
                return redirect(url_for('home'))  # This will go to /home and render home page.html
            else:
                flash("Invalid credentials.", "error")
        else:
            flash("Database connection failed.", "error")
    return render_template('login page.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')

        # Basic validation
        if not all([full_name, email, password, confirm_password, terms]):
            flash("All fields are required and Terms must be accepted.", "error")
            return render_template('create_account.html')
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('create_account.html')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    flash("Email already registered.", "error")
                    return render_template('create_account.html')
                cursor.execute(
                    "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
                    (full_name, email, hashed_password)
                )
                conn.commit()
                flash("Account created successfully! Please log in.", "success")
                return redirect(url_for('login'))
            except Exception as err:
                flash(f"Database error: {err}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Database connection failed.", "error")
    return render_template('create_account.html')

@app.route('/home')
def home():
    user_email = session.get('user_email', '')
    user_initial = user_email[0].upper() if user_email else 'U'
    return render_template('home page.html', user_email=user_email, user_initial=user_initial)

@app.route('/about')
def about():
    return render_template('about page.html')

@app.route('/profile')
def profile():
    user_email = session.get('user_email', '')
    user_initial = user_email[0].upper() if user_email else 'U'
    user_name = "User Name"  # Replace with actual name if available
    return render_template('profile.html', user_email=user_email, user_initial=user_initial, user_name=user_name)

@app.route('/settings')
def settings():
    user_email = session.get('user_email', '')
    user_initial = user_email[0].upper() if user_email else 'U'
    return render_template('settings.html', user_email=user_email, user_initial=user_initial)

@app.route('/callforisreal')
def callforisreal():
    return render_template('callforisreal.html')

@app.route('/about2')
def about2():
    return render_template('about2.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)