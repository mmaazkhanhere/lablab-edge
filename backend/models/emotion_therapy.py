import os
from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url='https://api.aimlapi.com'
)

def emotion_therapy(memory: str) -> str:
    """
    Recieves a memory from user, which is processed by AI and provide emotional therapy to the user
    
    Arguments:
        memory (str): The memory from the user
        
    Return:
        ai_response (str): A emotional therapy response to the user from AI
    
    """
    
    response: ChatCompletion = client.chat.completions.create(
    model ="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    messages=[
            {
                "role": "system", 
                "content": f"""You are an empathetic AI therapist designed to help users process and heal from 
                            emotional memories. You will be provide a memory {memory} and your goal is to provide 
                            compassionate support, validate the  user's feelings, and offer therapeutic insights based on the emotions conveyed. 
                            First, identify the core emotion (e.g., sadness, anger, joy), then reflect back 
                            with empathy, validating the user’s experience. Provide tailored therapeutic 
                            advice, such as cognitive reframing, mindfulness, self-compassion, or closure 
                            techniques, to help the user emotionally heal. Encourage positive actions and 
                            self-care, while maintaining a respectful, non-judgmental, and sensitive approach 
                            to foster growth and resilience, always ensuring the user feels safe and understood."""
            },
            {
                "role": "user", 
                "content": memory
            }
        ]   
    )
    
    ai_response: str = response.choices[0].message.content
    return ai_response