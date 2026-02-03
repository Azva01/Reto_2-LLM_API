#librería requests
import requests

#petición
url_api = "http://127.0.0.1:8000/analyze"
archivo = "news_el_economista.txt"

def ejecutar_prueba_api():
    #lectura de archivo:
    try: 
        with open(archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
        return
    
    #Instrucciones del usuario
    instrucciones = ("Basándote en el texto proporcionado, genera: "
    "1. Un resumen estructurado en forma de 5 viñetas numeradas que destaquen "
    "los puntos clave y las ideas principales del contenido. "
    "2. El resumen debe estar en idioma ingles americano(US). "
    "3. No debe contener información en español.")

    payload = {
        "instructions": instrucciones,
        "text": contenido
    }

    #Usar Api, agregue timeout de 30 segundos
    print("Conectando con la API...")
    response = requests.post(url_api, json=payload, timeout=30)

    if response.status_code == 200:
        respuesta_llm = response.json().get("respuesta")

        nombre_archivo_salida = "conversacion_3.txt"

        with open(nombre_archivo_salida, 'w', encoding='utf-8') as file:
            file.write('"""\n')
            file.write(
                f"Usuario:{instrucciones}. Analizar el siguiente "
                f"documento:{contenido[:100]}...\n")
            file.write(f"LLM: {respuesta_llm}\n")
            file.write('"""\n')

        print(f"Respuesta guardada en {nombre_archivo_salida}")
        print(respuesta_llm)
    else:
        print(f"Error en la API: {response.status_code}")

if __name__ == "__main__":
    ejecutar_prueba_api()