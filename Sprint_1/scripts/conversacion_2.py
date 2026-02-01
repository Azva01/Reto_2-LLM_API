import os
from dotenv import load_dotenv
from openai import OpenAI
import pypdf

load_dotenv()

#API Key config actualizada para OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Extracción de texto de cuento en PDF
def lectura_cuento_pdf(ruta_de_archivo):
    """
    Lee el contenido de un archivo PDF y lo devuelve como texto.
    """
    try:
        with open(ruta_de_archivo, 'rb') as file:
            lector_pdf = pypdf.PdfReader(file)
            contenido = ""
            for pagina in lector_pdf.pages:
                contenido += pagina.extract_text() + "\n"
        return contenido
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {ruta_de_archivo}."
    except Exception as e:
        return f"Error inesperado al leer el PDF. {e}"

#Función de chat con asistente   
def chat_asistente(mensajes):
    """
    Interactúa con asistente GPT-4o-mini para analizar contenido de cuento.

    """
    try:
        #Interacción con API de OpenAI
        respuesta = client.chat.completions.create(
            model='gpt-4o-mini',
            messages= mensajes,
            temperature=0.7
            
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error de API. {e}"

if __name__ == "__main__":
    texto_cuento = lectura_cuento_pdf("cuento.pdf")

    #Definir prompts y estructura de conversación
    historial = [
        {"role": "system", "content": 
            "Eres un asistente de lectura experto en análisis de cuentos. "
            "Tu tarea es ayudar al usuario a entender mejor los "
            "conceptos narrativos, temas, metáforas, simbolismos y personajes "
            "de los cuentos que leen."
        },
        {"role": "user", "content": (
            "Basándote en el siguiente cuento:\n\n"
            f"{texto_cuento}, genera 5 viñetas numeradas que muestren los "
            " momentos y puntos mas importantes de la historia."
        )} 
    ]

    #Primera respuesta del asistente
    respuesta_asistente = chat_asistente(historial)
    print(f"LLM: {respuesta_asistente}")

    #Guardar historial de conversación
    historial.append({"role": "assistant", "content": respuesta_asistente})

    #Generar archivo
    nombre_archivo = "conversacion_2.txt"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        # contenido de usuario
        f.write(f"Usuario: {historial[1]['content']}\n\n")
        #contenido de asistente
        f.write(f"LLM: {respuesta_asistente}\n")
        f.write('"""\n')
