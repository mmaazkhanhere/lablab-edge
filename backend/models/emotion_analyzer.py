import os
from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url='https://api.aimlapi.com'
)

def emotion_analyzer(memory: str) -> str:
    response: ChatCompletion = client.chat.completions.create(
    model ="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    messages=[
            {"role": "system", "content": f"You will be given a text that will be a user memory {memory}. Your /"
                                        "task is to analyze the emotion of the memory text."},
            {"role": "user", "content": memory}
        ]   
    )
    
    ai_message: str = response.choices[0].message.content
    return ai_message