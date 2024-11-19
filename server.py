# server.py

from flask import Flask, request
import logging
from datetime import datetime

app = Flask(__name__)

# Configurar logging
logging.basicConfig(filename='log_waf.log', level=logging.INFO, format='%(message)s')

@app.before_request
def log_request_info():
    timestamp = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
    ip = request.remote_addr
    method = request.method
    path = request.path
    url = request.url
    user_agent = request.headers.get('User-Agent', 'Unknown')
    status_code = '200'  # Puedes ajustar según la lógica de tu aplicación
    body = request.get_data(as_text=True)

    log_entry = f'INFO:werkzeug:{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status_code} -\n'
    log_entry += f'INFO:app:Request: {method} {url} Headers: {{\'User-Agent\': \'{user_agent}\'}} Body: {body.encode() if body else ""}\n'

    app.logger.info(log_entry)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'Bienvenido a la aplicación web protegida por el WAF.'

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # Aquí puedes implementar lógica adicional para manejar inicios de sesión
    return f'Intento de inicio de sesión con usuario: {username} y contraseña: {password}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
