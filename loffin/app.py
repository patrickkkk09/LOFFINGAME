from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin1232022',
    database='loffine_db'
)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/home')  # Redirect to home page if the user is already logged in
    return render_template('LOFLOGIN.html')

@app.route('/logout', methods=['POST'])
def logout():
    for key in list(session.keys()):
        session.pop(key)

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    app.logger.info(username)
    app.logger.info(password)
    # Perform login validation against the MySQL database
    cursor = db.cursor()
    cursor.execute('SELECT * FROM registered_tbl WHERE username_tbl = %s AND password_tbl = %s', (username, password))
    user = cursor.fetchone()

    app.logger.info(user)
    if user:
        # Store the user ID in the session
        session['user_id'] = user[0]
        return redirect('/home')  # Redirect to the home page on successful login
    else:
        return render_template('LOFLOGIN.html', error='Invalid username or password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            return render_template('LOFREGISTERPAGE.html', error='Passwords do not match')

        cursor = db.cursor()
        cursor.execute('INSERT INTO registered_tbl (username_tbl, email_tbl, password_tbl, confirmed_password_tbl) VALUES (%s, %s, %s, %s)',
                       (username, email, password, confirm_password))
        db.commit()

        return redirect('/')

    return render_template('LOFREGISTERPAGE.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('LOFHOMEPAGE.html')
    else:
        return redirect('/')
    

@app.route('/python-game')
def python_game():
    return render_template('LOFGAME.html')

@app.route('/settings')
def settings():
    
    return render_template("LOFSETTINGS.html")

@app.route('/profile')
def profile():
    
    return render_template("LOFPROFILE.html")

@app.route('/leaderboards')
def leaderboards():
    
    return render_template("LOFLEADERBOARD.html")

if __name__ == '_main_':
    app.run(debug=True)