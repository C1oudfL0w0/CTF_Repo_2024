from flask import Flask, render_template, request, redirect, url_for, session, render_template_string,Markup,make_response,flash
import random
import hashlib
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash  
import pymysql
from jinja2 import Template
# flag{Yes_You_find_Me!}
app = Flask(__name__)
app.secret_key = 'icssla'  # 设置一个密钥用于session加密
# 数据库连接配置  
db_config = {  
    'host': 'localhost',  
    'user': 'root',  
    'password': 'abc123!@#',  
    'db': 'flask_login_db',  
    'charset': 'utf8mb4',  
    'cursorclass': pymysql.cursors.DictCursor,  
} 
# 设置 session cookie 的 HttpOnly 和 Secure 标志
app.config['SESSION_COOKIE_HTTPONLY'] = False  # 设置为 False，允许 JavaScript 访问
app.config['SESSION_COOKIE_SECURE'] = False  # 设置为 False，允许在 HTTP 上发送 cookie

def contains_sql_keywords(input_string, keywords): 
    for keyword in keywords:  
        if keyword in input_string:  
            return True  
    return False  

def contains_ssti_keywords(input_string, keywords): 
    for keyword in keywords:  
        if keyword in input_string:  
            return True  
    return False  
# 假设这是你的用户数据库
#users = {
#    "admin": "admin@123"
#}
md5_hash = hashlib.md5() 
# 生成随机风机数据
def generate_random_data(page, num_entries=100):
    data = []
    for i in range(num_entries):
        fan = f"Fan {i+1}"
        speed = random.randint(1000, 3000)  # 转速范围 1000-3000 RPM
        power = random.uniform(100.0, 500.0)  # 发电量范围 100-500 kW
        data.append({"fan": fan, "speed": speed, "power": power})
    page_size = 10  # 每页显示的数据条数
    try:
        page = int(page)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return data[start_index:end_index], page
    except ValueError:
        return [], 1  # 如果输入的不是有效的整数，返回空数据和默认页数1

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql_keywords = ['select', 'from', 'where', 'union', 'join', 'sleep',' ']  
        input_string = f"{username}:{password}"  
        md5_hash.update(input_string.encode('utf-8'))
        hex_dig = md5_hash.hexdigest()
        connection = pymysql.connect(**db_config)  
        if contains_sql_keywords(username, sql_keywords):  
            return "Error: There are illegal characters in the character you entered.", 400
        try:  
            with connection.cursor() as cursor:  
                # 执行查询  
                sql = "SELECT * FROM users WHERE username ='" + username +"'"
                cursor.execute(sql)  
                #sql = "SELECT * FROM users WHERE username = %s"  
                #cursor.execute(sql, (username,))  
                result = cursor.fetchone()  
                # 验证用户名和密码  
                if result and result['password'] == password:   
                    flash('Login successful!', 'success')  
                    session['username'] = username  
                    # 假设 session_token 是与 session 相关的一个值  
                    session_token = str(random.randint(100000, 999999))  # 仅为示例  
                    response = make_response(redirect(url_for('index')))  
                    response.set_cookie('username', hex_dig, httponly=False, secure=False)  
                    return response  
                else:  
                    flash('Invalid username or password', 'danger')
                    return 'Invalid credentials'
        finally:  
            connection.close()  
    return render_template('login.html')

@app.route('/logout')
def logout():