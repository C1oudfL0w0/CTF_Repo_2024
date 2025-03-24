from flask import Flask, render_template, request, session, redirect, url_for
import threading
import random
import string
import datetime
import rsa
from werkzeug.utils import secure_filename
import os
import subprocess

(pubkey, privkey) = rsa.newkeys(2048)

app = Flask(__name__)
app.secret_key = "super_secret_key"



UPLOAD_FOLDER = 'templates/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == users.get('admin', {}).get('password'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

    cmd_output = ""
    if 'cmd' in request.args:
        if os.path.exists("lock.txt"):  # 检查当前目录下是否存在lock.txt
            cmd = request.args.get('cmd')
            try:
                cmd_output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            except Exception as e:
                cmd_output = str(e)
        else:
            cmd_output = "lock.txt not found. Command execution not allowed."
    return render_template('admin_dashboard.html', users=users, cmd_output=cmd_output, active_tab="cmdExecute")


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Generate random users
def generate_random_users(n):
    users = {}
    for _ in range(n):
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        users[username] = {"password": password, "balance": 2000}
    return users

users = generate_random_users(1000)
users["HRP"] = {"password": "HRP", "balance": 6000}

# Add an admin user with a random password
admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
users["admin"] = {"password": admin_password, "balance": 0}

flag_price = 10000
flag = admin_password  # The flag is the password of the admin user
mutex = threading.Lock()


@app.route('/')
def index():
    if "username" in session:
        return render_template("index.html", logged_in=True, username=session["username"], balance=users[session["username"]]["balance"])
    return render_template("index.html", logged_in=False)

@app.route('/reset', methods=['GET'])
def reset():
    global users
    users = {}  # Clear all existing users
    users = generate_random_users(1000)
    users["HRP"] = {"password": "HRP", "balance": 6000}
    global admin_password
    admin_password={}
    global flag
    # Add an admin user with a random password
    admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    flag=admin_password

    users["admin"] = {"password": admin_password, "balance": 0}
    
    return redirect(url_for('index'))


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in users and users[username]["password"] == password:
        session["username"] = username
        return redirect(url_for('index'))
    return "Invalid credentials", 403

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))


def log_transfer(sender, receiver, amount):
    def encrypt_data_with_rsa(data, pubkey):
        for _ in range(200):  # Encrypt the data multiple times
            encrypted_data = rsa.encrypt(data.encode(), pubkey)
        return encrypted_data.hex()

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Encrypt the amount and timestamp
    encrypted_amount = encrypt_data_with_rsa(str(amount), pubkey)
    encrypted_timestamp = encrypt_data_with_rsa(timestamp, pubkey)
    
    log_data = f"{encrypted_timestamp} - Transfer from {sender} to {receiver} of encrypted amount {encrypted_amount}\n"
    
    for _ in range(1): 
        log_data += f"Transaction initiated from device: {random.choice(['Mobile', 'Web', 'ATM', 'In-Branch Terminal'])}\n"
        log_data += f"Initiator IP address: {random.choice(['192.168.1.', '10.0.0.', '172.16.0.'])}{random.randint(1, 254)}\n"
        log_data += f"Initiator geolocation: Latitude {random.uniform(-90, 90):.6f}, Longitude {random.uniform(-180, 180):.6f}\n"
        log_data += f"Receiver's last login device: {random.choice(['Mobile', 'Web', 'ATM'])}\n"
        log_data += f"Associated fees: ${random.uniform(0.1, 3.0):.2f}\n"
        log_data += f"Remarks: {random.choice(['Regular transfer', 'Payment for invoice #'+str(random.randint(1000,9999)), 'Refund for transaction #'+str(random.randint(1000,9999))])}\n"
        log_data += "-"*50 + "\n"

    with open('transfer_log.txt', 'a') as f:
        f.write(log_data)




@app.route('/transfer', methods=["POST"])
def transfer():
    if "username" not in session:
        return "Not logged in", 403
    
    receivers = request.form.getlist("receiver")
    amount = int(request.form.get("amount"))
    if amount <0:
        return "Insufficient funds", 400
    logging_enabled = request.form.get("logs", "false").lower() == "true"
    
    if session["username"] in receivers:
        return "Cannot transfer to self", 400
    
    for receiver in receivers:
        if receiver not in users:
            return f"Invalid user {receiver}", 400
    
    total_amount = amount * len(receivers)
    if users[session["username"]]["balance"] >= total_amount:
        for receiver in receivers:
            if logging_enabled:
                log_transfer(session["username"], receiver, amount)
            mutex.acquire()
            users[session["username"]]["balance"] -= amount
            users[receiver]["balance"] += amount
            mutex.release()
        return redirect(url_for('index'))
    return "Insufficient funds", 400


@app.route('/buy_flag')
def buy_flag():
    if "username" not in session:
        return "Not logged in", 403

    if users[session["username"]]["balance"] >= flag_price:
        users[session["username"]]["balance"] -= flag_price
        return f"Here is your flag: {flag}"
    return "Insufficient funds", 400

@app.route('/get_users', methods=["GET"])
def get_users():
    num = int(request.args.get('num', 1000))
    selected_users = random.sample(list(users.keys()), num)
    return {"users": selected_users}

@app.route('/view_balance/<username>', methods=["GET"])
def view_balance(username):
    if username in users:
        return {"username": username, "balance": users[username]["balance"]}
    return "User not found", 404

@app.route('/force_buy_flag', methods=["POST"])
def force_buy_flag():
    if "username" not in session or session["username"] != "HRP":
        return "Permission denied", 403

    target_user = request.form.get("target_user")
    if target_user not in users:
        return "User not found", 404

    if users[target_user]["balance"] >= flag_price:
        users[target_user]["balance"] -= flag_price
        return f"User {target_user} successfully bought the flag!,"+f"Here is your flag: {flag}"
    return f"User {target_user} does not have sufficient funds", 400


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)
