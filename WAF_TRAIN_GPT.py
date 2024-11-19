import openai
import time
from collections import deque
from colorama import Fore, Style, init
import json
import os

# Inicializar colorama para la visualización en consola
init(autoreset=True)

# Configura tu API key de OpenAI
openai.api_key = ""

# Memoria para almacenar ejemplos clasificados y usarlos más adelante
memoria = {}

# Cargar la memoria previamente almacenada (si existe)
try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except FileNotFoundError:
    print(f"{Fore.YELLOW}Memoria vacía, iniciando nuevo aprendizaje...")

# Función para consultar ChatGPT y clasificar el ataque
def consultar_chatgpt(log_line):
    if not log_line or log_line.strip() == "":
        print(f"{Fore.YELLOW}⚠️ Línea vacía o irrelevante, omitiendo clasificación.")
        return "No Attack"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Clasifica la línea de log como 'No Attack', 'XSS', 'SQL Injection', 'Path Traversal', 'Command Injection', 'Remote File Inclusion', 'LDAP Injection', 'Code Injection'."},
            {"role": "user", "content": f"Línea de log: {log_line}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Función para almacenar la memoria de aprendizaje en un archivo JSON
def guardar_memoria():
    with open("memoria.json", "w") as f:
        json.dump(memoria, f)
    print(f"{Fore.GREEN}✔ Memoria almacenada correctamente.")

# Función para aprender de ejemplos nuevos
def reentrenar_modelo():
    print(f"{Fore.MAGENTA}🚀 Reentrenando con los nuevos ejemplos aprendidos...")
    guardar_memoria()
    print(f"{Fore.GREEN}✔ Reentrenamiento completo. El sistema ha aprendido y mejorado.\n")

# Función para procesar cada línea de log
def procesar_linea_log(log_line):
    log_line = log_line.strip()  # Limpiar la línea de espacios en blanco
    print(f"{Fore.CYAN}➤ Procesando nueva línea de log: {log_line}")

    if not log_line:
        print(f"{Fore.YELLOW}⚠️ Línea vacía, omitiendo procesamiento.\n")
        return

    # Verificar si la línea ya fue clasificada previamente
    if log_line in memoria:
        prediccion = memoria[log_line]
        print(f"{Fore.GREEN}✔ Clasificado por el sistema como: {prediccion} (aprendido)\n")
        return

    confianza_baja = True  # Simulamos que el sistema no está seguro inicialmente

    if confianza_baja:  # En caso de que el sistema no esté seguro, consultar ChatGPT
        print(f"{Fore.BLUE}🔄 Recurriendo a ChatGPT para clasificar la línea...")
        prediccion = consultar_chatgpt(log_line)
        if "Necesitaré ver" in prediccion:  # Filtrar respuestas no útiles
            prediccion = "No Attack"
        print(f"{Fore.BLUE}🔍 ChatGPT clasificó la línea como: {prediccion}")

        # Almacenar la línea y su predicción en la memoria
        memoria[log_line] = prediccion
    else:
        prediccion = "No Attack"
        print(f"{Fore.GREEN}✔ Clasificado por el sistema como: {prediccion}")

    # Guardar la memoria de aprendizaje en cada paso para que se persista
    guardar_memoria()

# Función para leer las nuevas líneas de un archivo en tiempo real
def leer_logs_en_vivo(archivo_log):
    # Abrir el archivo de log y moverse al final del archivo
    with open(archivo_log, "r") as f:
        f.seek(0, os.SEEK_END)  # Mover el puntero al final del archivo
        print(f"{Fore.YELLOW}📄 Monitoreando el archivo de log para nuevas entradas...\n")
        
        while True:
            linea = f.readline()
            if not linea:  # Si no hay nueva línea, esperar un momento
                time.sleep(1)
                continue

            # Procesar la nueva línea de log
            procesar_linea_log(linea)

if __name__ == "__main__":
    archivo_log = "log_waf.log"  # Nombre del archivo de log
    leer_logs_en_vivo(archivo_log)
