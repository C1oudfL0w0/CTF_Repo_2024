import os
import logging
import subprocess
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

if not app.debug:
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'gif', 'log', 'tex'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compile_tex(file_path):
    output_filename = file_path.rsplit('.', 1)[0] + '.pdf'
    try:
        subprocess.check_call(['pdflatex', file_path])
        return output_filename
    except subprocess.CalledProcessError as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        content = file.read()
        try:
            content_str = content.decode('utf-8')
        except UnicodeDecodeError:
            return 'File content is not decodable'
        for bad_char in ['\\x', '..', '*', '/', 'input', 'include', 'write18', 'immediate', 'app', 'flag']:
            if bad_char in content_str:
                return 'File content is not safe'
        file.seek(0)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return 'File uploaded successfully, And you can compile the tex file'
    else:
        return 'Invalid file type or name'

@app.route('/compile', methods=['GET'])
def compile():
    filename = request.args.get('filename')

    if not filename:
        return 'No filename provided', 400

    if len(filename) >= 7:
        return 'Invalid file name length', 400

    if not filename.endswith('.tex'):
        return 'Invalid file type', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(file_path)
    if not os.path.isfile(file_path):
        return 'File not found', 404

    output_pdf = compile_tex(file_path)
    if output_pdf.endswith('.pdf'):
        return "Compilation succeeded"
    else:
        return 'Compilation failed', 500

@app.route('/log')
def log():
    try:
        with open('app.log', 'r') as log_file:
            log_contents = log_file.read()
        return render_template('log.html', log_contents=log_contents)
    except FileNotFoundError:
        return 'Log file not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)