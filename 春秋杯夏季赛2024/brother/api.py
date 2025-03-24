import mysql.connector, time, threading, socket
from flask import Flask, request

app = Flask(__name__)


def mysql_keepalive():
    config = {
        'user': 'ctf',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'mysql',
        'port': 6666,

    }
    try:
        db_connection = mysql.connector.connect(**config)
        cursor = db_connection.cursor()
    except mysql.connector.Error as err:
        print(err)
        exit(0)
    while True:
        try:
            cursor.execute("SELECT VERSION();")
            cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"连接中断: {err}")
        time.sleep(10)


def handle_client_connection(client_socket):
    try:
        while True:
            client_socket.send('{"code":0, "path": ""}'.encode('utf-8'))
            time.sleep(10)
    except Exception as e:
        print(f"Error handling client: {e}")


def update_api():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 7777
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"update_api Listening on port {port}...")
    while True:
        client_socket, addr = server_socket.accept()
        handle_client_connection(client_socket)


@app.route('/evil', methods=['POST'])
def evil():
    code = request.json['code']
    key = request.json['key']
    if key == open("./evil.key").read():
        exec(code)
        return "ok"
    else:
        return "key error"


if __name__ == '__main__':
    threading.Thread(target=mysql_keepalive).start()
    threading.Thread(target=update_api).start()
    app.run("127.0.0.1", 5000)