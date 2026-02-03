import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="API CueBot")

class AnalysisRequest(BaseModel):
    instructions: str
    text: str

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """
    Obtiene instrucciones y texto, devuelve respuesta del LLM.
    """
    print("Petición recibida")
    try:
        print(f"Instrucciones: {request.instructions[:50]}...")

        messages = [
            {
                "role": "system", 
                "content": (
                    "Eres un asistente experto en análisis de textos. "
                    "Tus respuestas son estrictamente en el idioma "
                    "y en el formato que el usuario te solicite."
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Instrucciones: {request.instructions}\n\n"
                    f"Texto: {request.text}"
                )
            }
        ]
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            temperature=0.7
        )
        print("Respuesta recibida de API")

        respuesta_asistente = response.choices[0].message.content
        return {"respuesta": respuesta_asistente}
    
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f'OpenAI API: {e}')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
