from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory
import os

app = Flask(_name_)
app.secret_key = os.urandom(24)

# Temporary storage for users (in-memory simulation for demonstration purposes)
users = []

# Path to store user-uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simulate a database with an in-memory list
def save_user(user):
    users.append(user)

# Login page with template embedded
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle Login
        username = request.form['username']
        password = request.form['password']
        pic = request.files['userPic']
        
        if not username or not password:
            return render_template_string(index_html, message="Please enter both username and password.", message_type="error")

        # Save the uploaded picture with the username
        pic_filename = f"{username}_{pic.filename}" if pic else 'default.png'
        pic.save(os.path.join(UPLOAD_FOLDER, pic_filename))

        # Simulate user login
        user = {
            'username': username,
            'password': password,
            'pic': pic_filename
        }

        # Save user (for demo purposes)
        save_user(user)

        # Store session data for the user
        session['username'] = username
        session['logged_in'] = True

        # Redirect to visit page
        return redirect(url_for('visit'))
    
    return render_template_string(index_html)

# Visit page with template embedded
@app.route('/visit')
def visit():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # If not logged in, redirect to login page

    return render_template_string(visit_html, username=session.get('username'))

# Admin panel page with template embedded
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_password = request.form['adminPassword']
        if admin_password == 'TH3_FAIZU':
            return render_template_string(admin_html, users=users)
        else:
            return render_template_string(admin_html, message="Invalid Admin Password.", message_type="error")

    return render_template_string(admin_html)

# Delete user from the list
@app.route('/delete_user/<username>')
def delete_user(username):
    global users
    users = [user for user in users if user['username'] != username]
    return redirect(url_for('admin'))

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# HTML templates integrated into the Flask app
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 50px auto; padding: 20px; background: #fff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; }
        input[type="text"], input[type="password"], input[type="file"] {
            width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #ddd; border-radius: 5px;
        }
        button { width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="username" placeholder="Enter Username" required><br>
            <input type="password" name="password" placeholder="Enter Password" required><br>
            <input type="file" name="userPic" accept="image/*"><br>
            <button type="submit">Login</button>
        </form>
        {% if message %}
        <p class="{{ message_type }}">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

visit_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 50px auto; padding: 20px; background: #fff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; }
        a { text-align: center; display: block; margin-top: 20px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px; text-decoration: none; }
        a:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ username }}!</h2>
        <p>Your visit is confirmed. Click below to proceed.</p>
        <a href="https://faizuhere.onrender.com/" target="_blank">Visit</a>
    </div>
</body>
</html>
"""

admin_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 700px; margin: 50px auto; padding: 20px; background: #fff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; }
        input[type="password"] {
            width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #ddd; border-radius: 5px;
        }
        button { width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .user-list { margin-top: 20px; }
        .user-list li { margin: 10px 0; }
        .delete { color: red; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Admin Panel</h2>
        <form method="POST">
            <input type="password" name="adminPassword" placeholder="Enter Admin Password" required><br>
            <button type="submit">Login as Admin</button>
        </form>
        
        {% if message %}
        <p class="error">{{ message }}</p>
        {% endif %}
        
        {% if users %}
        <div class="user-list">
            <h3>All Users:</h3>
            <ul>
                {% for user in users %}
                <li>
                    <img src="{{ url_for('uploaded_file', filename=user['pic']) }}" width="50" height="50" alt="User Picture">
                    {{ user['username'] }}
                    <a href="{{ url_for('delete_user', username=user['username']) }}" class="delete">Delete</a>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% else %}
        <p>No users yet.</p>
        {% endif %}
    </div>
</body>
</html>
"""

# Running the app
if _name_ == '_main_':
    app.run(debug=True)
