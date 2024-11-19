import openai
import time
import json
import os
from collections import deque
from colorama import Fore, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Inicializar colorama para la visualización en consola
init(autoreset=True)

# Configura tu API key de OpenAI
openai.api_key = ""

# Memoria para almacenar ejemplos clasificados y usarlos más adelante
memoria = {}

# Inicializar modelo Naive Bayes
vectorizer = TfidfVectorizer(max_features=1000)  # Transformar texto a vectores
model = MultinomialNB()

# Cargar la memoria previamente almacenada (si existe)
try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except FileNotFoundError:
    print(f"{Fore.YELLOW}Memoria vacía, iniciando nuevo aprendizaje...")

# Función para entrenar el modelo con los datos actuales de la memoria
def entrenar_modelo():
    if len(memoria) < 5:  # Solo entrenar si hay suficientes datos
        print(f"{Fore.YELLOW}No hay suficientes datos para entrenar el modelo aún.")
        return

    entradas = list(memoria.keys())
    etiquetas = list(memoria.values())

    # Transformar texto de logs a vectores
    X = vectorizer.fit_transform(entradas).toarray()
    y = etiquetas  # Las etiquetas son los tipos de ataques clasificados

    # Entrenar el modelo Naive Bayes
    model.fit(X, y)
    print(f"{Fore.GREEN}✔ Modelo entrenado con {len(entradas)} ejemplos.")

# Función para intentar clasificar una nueva línea de log usando el modelo
def clasificar_con_modelo(log_line):
    try:
        log_vector = vectorizer.transform([log_line]).toarray()
        prediccion = model.predict(log_vector)
        return prediccion[0]  # Retornar la clase predicha
    except ValueError:
        return None  # Si el modelo no tiene suficientes datos o no está entrenado

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

# Función para determinar si una línea de log es sospechosa
def es_log_sospechoso(log_line):
    # Si el log contiene patrones típicos de ataques
    patrones_sospechosos = ["select", "union", "http", "%", "admin", "cat", "shadow", "alert", "svg", "cmd.exe"]
    return any(patron in log_line.lower() for patron in patrones_sospechosos)

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

    # Intentar clasificar con el modelo propio primero (si está entrenado)
    prediccion_con_modelo = clasificar_con_modelo(log_line)

    # Si el modelo predice "No Attack" pero el log es sospechoso, recurrir a ChatGPT
    if prediccion_con_modelo == "No Attack" and es_log_sospechoso(log_line):
        print(f"{Fore.YELLOW}🔍 El modelo predijo 'No Attack', pero la línea parece sospechosa. Recurriendo a ChatGPT...")
        prediccion = consultar_chatgpt(log_line)
        memoria[log_line] = prediccion  # Guardar en memoria
        guardar_memoria()
        entrenar_modelo()  # Reentrenar el modelo con el nuevo dato
    elif not prediccion_con_modelo:  # Si el modelo no tiene predicción, recurrir a ChatGPT
        print(f"{Fore.YELLOW}Modelo no entrenado o insuficientemente entrenado, recurriendo a ChatGPT...")
        prediccion = consultar_chatgpt(log_line)
        memoria[log_line] = prediccion  # Guardar en memoria
        guardar_memoria()
        entrenar_modelo()  # Reentrenar el modelo con el nuevo dato
    else:
        print(f"{Fore.GREEN}✔ Clasificado por el modelo como: {prediccion_con_modelo}")
        memoria[log_line] = prediccion_con_modelo  # Guardar en memoria
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
