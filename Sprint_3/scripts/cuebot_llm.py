"""
Ejemplo 4: Draft de la interfaz gráfica para CueBot
Sin embargo falta la conexión al LLM de tu elección :(
"""

import time
import gradio as gr
from PyPDF2 import PdfReader
import requests


# Variable auxiliar para guardar el texto del PDF
CORPUS_TEXT = ''

# URL de la API del LLM
URL_API = "http://127.0.0.1:8000/analyze"

'''
# Respuestas aleatorias para prueba del chatbot (borrar lista luego)
RESPUESTAS_ALEATORIAS = [
    "Soy la respuesta aleatoria 1...",
    "Soy la respuesta aleatoria 2...",
    CORPUS_TEXT
]
'''

def extraer_texto_pdf(file_path):
    """
    Extrae el texto de un archivo PDF cargado
    """
    try:
        reader = PdfReader(file_path)
        extracted_text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                extracted_text += content + "\n"
        return extracted_text
    except Exception as e:
        return f"Error al leer PDF: {e}"


def add_text(history, text):
    """
    Agrega texto a la historia del chat y actualiza la
    interfaz
    """

    history = history + [{"role": "user", "content": text}]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    Permite agrega un texto pdf a la conversación del chat
    y guardar 
    """
    # Funcion global para recordar el texto del PDF
    global CORPUS_TEXT
    CORPUS_TEXT = extraer_texto_pdf(file.name)

    print(CORPUS_TEXT)

    mensaje_confirmacion = (
        f"Archivo '{file.name}' leído con éxito. "
        "Soy CueBot, pregúntame lo que necesites sobre el texto."
    )

    history = history + [
        {"role": "assistant", "content": mensaje_confirmacion}
    ]

    return history

    # Leemos el texto del archivo PDF y lo guardamos en
    # CORPUS_TEXT para el futuro


def bot(history):
    """
    Obtiene la respuesta del Bot
    """
    # Extrae ultimo input de texto de la historia de la conversacion del bot
    input_text = history[-1]["content"]

    #Forzar que los datos sean strings
    payload = {
        "instructions": str(input_text),
        "text": str(CORPUS_TEXT) if CORPUS_TEXT else "No hay texto cargado."
    }

    try:
        response = requests.post(URL_API, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            respuesta_llm = data.get("respuesta", "No se recibió respuesta.")
        else:
            respuesta_llm = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        respuesta_llm = (
            "Error al conectar con la API: Asegúrate de que FastAPI "
            "este corriendo"
        )
    
    # Define entrada de texto vacio
    history.append({"role": "assistant", "content": ""})
    
    for character in respuesta_llm:
        history[-1]["content"] += character
        time.sleep(0.02)
        yield history


# Crea la aplicación de Gradio
with gr.Blocks() as demo:
    gr.Markdown("# CueBot - Universidad de Cuévano")

    # Crea el chatbot
    chatbot = gr.Chatbot([], elem_id="chatbot", height=750)

    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Especifica el archivo pdf o ingresa un texto",
                container=False
            )

        # Cuadro de subida de archivo
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁 Subir Archivo:", file_types=[".pdf"])

    # Encadenamiento de eventos

    txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).success(
        bot, chatbot, chatbot
    ).success(lambda: gr.update(interactive=True), None, [txt], queue=False)

    btn.upload(add_file, [chatbot, btn], [chatbot], queue=False)

demo.queue()
if __name__ == "__main__":
    demo.launch(
        share=True,
        theme=gr.themes.Soft()
        )