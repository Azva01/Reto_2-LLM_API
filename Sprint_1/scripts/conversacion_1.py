import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

#API Key config actualizada para OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generar_resumen(ruta_de_archivo):
    """
    Genera resumen conciso de documento de texto extenso usando GPT-4o-mini.
    """
    try:
        #Lectura de contenido:
        with open(ruta_de_archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()

        #Estructura del prompt: Rol, tarea y formato:
        prompt_de_sistema = (           
            "Eres un asistente de ámbito académico experto en analisis de "
            "documentos de texto." "Tu trabajo consiste en leer documentos "
            "extensos y generar resúmenes concisos que capturen los puntos "
            "clave y las ideas principales."     
        )

        prompt_de_usuario = (
            "Genera un resumen del siguiente documento:\n\n"
            f"{contenido}\n\n"
            "Genera una respuesta que cumpla con el siguiente formato y "
            "requerimientos:\n"
            "1. El resumen debe ser en idioma español.\n"
            "2. Debe estar conformado por solo dos párrafos.\n"
            "3. Debes agregar un tercer párrafo que tenga unicamente el"
            "nombre del documento y el titulo correspondiente de la noticia."
        )

        #Interacción con API de OpenAI
        respuesta = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": prompt_de_sistema},
                {"role": "user", "content": prompt_de_usuario}
            ],
            temperature=0.5
        )

        return respuesta.choices[0].message.content
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {ruta_de_archivo}."
    #except para manejo de API
    except OpenAIError as e:
        return f"Error: Comunicación con API fallida. {e}"
    except Exception as e:
        return f"Error inesperado. {e}"


if __name__ == "__main__":
    resultado = generar_resumen("news_digital_bank.txt")

    print("Respuesta del asistente académico:\n")
    print(resultado)
    
with open("resumen_noticia.txt", "w", encoding="utf-8") as f:
    f.write(resultado)
print("\n[✓] El resumen ha sido guardado en 'resumen_noticia.txt'")