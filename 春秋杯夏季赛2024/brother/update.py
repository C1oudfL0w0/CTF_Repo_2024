import json
import socket
import tarfile

def extract_specific_file(tar_path, file_name, extract_path):
    with tarfile.open(tar_path, "r:gz") as tar:
        file_info = tar.getmember(file_name)
        tar.extract(file_info, path=extract_path)
        print("ok")

s = socket.socket()
s.connect(("127.0.0.1", 7777))
while True:
    data = s.recv(1024)
    try:
        js = json.loads(data)
        if js['code'] == 1:
            extract_specific_file(js['path'], 'new.bin', "/updatedir")
    except:
        s.send(b'Error')