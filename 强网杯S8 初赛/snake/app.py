from flask import Flask, render_template, jsonify, request, session, redirect
import random
import sqlite3
import time
from jinja2 import Template

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_secret_key'

# 初始化数据库
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            best_time REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# 查询用户
def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = '" + username + "'")
    user = c.fetchone()
    conn.close()
    return user

# 添加或更新用户
def add_or_update_user(username, best_time=None):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    user = get_user(username)
    if user:
        if best_time and (user[2] == 0 or best_time < user[2]):
            c.execute('UPDATE users SET best_time = ? WHERE username = ?', (best_time, username))
    else:
        c.execute('INSERT INTO users (username, best_time) VALUES (?, ?)', (username, best_time or 0))
    conn.commit()
    conn.close()

# 初始化游戏状态
def reset_game():
    global snake, direction, food, score, start_time
    snake = [(10, 10)]
    direction = 'RIGHT'
    food = (random.randint(0, 19), random.randint(0, 19))
    score = 0
    start_time = time.time()

init_db()

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('index.html')
    reset_game()
    return render_template('game.html', username=session['username'])

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form.get('username')
    add_or_update_user(username)
    session['username'] = username
    return jsonify({'status': 'success'})

@app.route('/move', methods=['POST'])
def move():
    global snake, direction, food, score, start_time
    
    # 获取新的方向
    new_direction = request.json.get('direction')
    
    # 更新方向
    if new_direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        direction = new_direction
    
    # 计算新位置
    head_x, head_y = snake[0]
    if direction == 'UP':
        head_y -= 1
    elif direction == 'DOWN':
        head_y += 1
    elif direction == 'LEFT':
        head_x -= 1
    elif direction == 'RIGHT':
        head_x += 1
    
    # 检查碰撞
    if head_x < 0 or head_x >= 20 or head_y < 0 or head_y >= 20 or (head_x, head_y) in snake:
        reset_game()
        return jsonify({'status': 'game_over', 'score': score})
    
    # 添加新头部
    snake.insert(0, (head_x, head_y))
    
    # 检查是否吃到食物
    if (head_x, head_y) == food:
        score += 1
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in snake:
                break
    else:
        snake.pop()
    
    # 检查是否通关
    if score >= 50:
        elapsed_time = time.time() - start_time
        add_or_update_user(session['username'], elapsed_time)
        return jsonify({'status': 'win', 'url': f"/snake_win?username={session['username']}"})
    return jsonify({'status': 'ok', 'snake': snake, 'food': food, 'score': score})

@app.route('/snake_win')
def win():
    username = request.args.get('username')
    user = get_user(username)
    best_time = user[2] if user else 0
    f = open('templates/win.html','r', encoding='utf-8')
    content = f.read().replace("{{ best_time }}",str(best_time))
    f.close()
    t = Template(content)
    return t.render(username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)