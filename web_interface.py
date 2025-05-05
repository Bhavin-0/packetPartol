from flask import Flask, render_template_string, send_file, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import csv

app = Flask(__name__)

# Flask-Login setup
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Dummy User Data
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'admin': {'password': 'password'}}  # Change this to a more secure approach

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# CSS styles for the beautiful interface
STYLES = """
<style>
    :root {
        --primary: #6c5ce7;
        --secondary: #a29bfe;
        --accent: #fd79a8;
        --dark: #2d3436;
        --light: #f5f6fa;
        --success: #00b894;
        --danger: #d63031;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        margin: 0;
        padding: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        color: var(--dark);
    }
    
    .auth-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        padding: 40px;
        width: 400px;
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    h1 {
        color: var(--primary);
        margin-bottom: 30px;
        font-weight: 700;
    }
    
    .form-group {
        margin-bottom: 25px;
        text-align: left;
    }
    
    label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: var(--dark);
    }
    
    input {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #ddd;
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.3s;
        box-sizing: border-box;
    }
    
    input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
        outline: none;
    }
    
    .btn {
        background: var(--primary);
        color: white;
        border: none;
        padding: 14px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .btn:hover {
        background: #5649d6;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .btn:active {
        transform: translateY(0);
    }
    
    .message {
        margin-top: 20px;
        padding: 10px;
        border-radius: 5px;
    }
    
    .error {
        background-color: #ffebee;
        color: var(--danger);
    }
    
    .dashboard {
        max-width: 800px;
        margin: 50px auto;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .nav {
        display: flex;
        justify-content: space-around;
        margin-top: 30px;
    }
    
    .nav a {
        text-decoration: none;
        color: white;
        background: var(--accent);
        padding: 12px 25px;
        border-radius: 30px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .nav a:hover {
        background: #fc5d9d;
        transform: scale(1.05);
    }
    
    .welcome {
        color: var(--primary);
        font-size: 28px;
        margin-bottom: 30px;
    }
    
    .decoration {
        position: absolute;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: rgba(253, 121, 168, 0.2);
        z-index: -1;
    }
    
    .decoration:nth-child(1) {
        top: -50px;
        left: -50px;
    }
    
    .decoration:nth-child(2) {
        bottom: -50px;
        right: -50px;
        background: rgba(108, 92, 231, 0.2);
    }
</style>
"""

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(f'''
                {STYLES}
                <div class="auth-container">
                    <div class="decoration"></div>
                    <div class="decoration"></div>
                    <h1>Welcome Back</h1>
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn">Login</button>
                    </form>
                    <div class="message error">Invalid credentials. Please try again.</div>
                </div>
            ''')
    
    return render_template_string(f'''
        {STYLES}
        <div class="auth-container">
            <div class="decoration"></div>
            <div class="decoration"></div>
            <h1>Welcome Back</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
        </div>
    ''')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(f'''
        {STYLES}
        <div class="dashboard">
            <h1 class="welcome">Welcome, {current_user.id}!</h1>
            <p>You have successfully logged in to the system.</p>
            <div class="nav">
                <a href="/download_csv">Download CSV</a>
                <a href="/logout">Logout</a>
            </div>
        </div>
    ''')

@app.route('/download_csv')
@login_required
def download_csv():
    log_file = 'logs/packets.log'

    if not os.path.exists(log_file):
        return "Log file does not exist.", 404

    csv_filename = 'logs/packets.csv'
    with open(log_file, 'r') as log_file, open(csv_filename, 'w', newline='') as csv_file:
        log_reader = csv.reader(log_file)
        csv_writer = csv.writer(csv_file)
        
        csv_writer.writerow(['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info'])
        for row in log_reader:
            csv_writer.writerow(row)

    return send_file(csv_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)