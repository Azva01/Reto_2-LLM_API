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
        print(f"Instructions: {request.instructions[:50]}...")

        messages = [
            {
                "role": "system", 
                "content": (
                    "Tu nombre es CueBot. Eres un chatbot asistente virtual "
                    "experto en análisis de textos para "
                    "la Universidad de Cuévano. "
                    "Tu tarea es analizar textos y proporcionar respuestas "
                    "de manera clara, con un tono profesional y amable."
                    "Tus respuestas son estrictamente en español."
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Instructions: {request.instructions}\n\n"
                    f"Text: {request.text}"
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
    
