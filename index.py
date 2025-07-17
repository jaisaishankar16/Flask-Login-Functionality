from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

# Create a Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['login']
users_collection = db['login_data']

# Define a route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if username and password match a user in the database
        user = users_collection.find_one({'email': email, 'password': password})
        
        if user:
            # Store username in session
            session['email'] = email
            return "Login successful"
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Define a route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if username already exists in the database
        if users_collection.find_one({'email': email}):
            error = "Username already exists"
            return render_template('register.html', error=error)
        
        # Insert new user into the database
        users_collection.insert_one({'email': email, 'password': password})
        
        # Store username in session
        session['username'] = email
        return redirect('/')
    else:
        return render_template('register.html')

# Define a route for the home page
@app.route('/')
def home():
    # Check if user is logged in
    if 'email' in session:
        return f"Welcome, {session['email']}"
    else:
        return redirect('/register')


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
