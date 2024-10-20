import os
from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url='https://api.aimlapi.com'
)

def prompt_for_music(memory: str)-> str:
    """
    Recieves a memory from user, which is processed by AI and returns a prompt that can be used
    by AI models to create music that can heal user emotionally
    
    Arguments:
        memory (str): The memory from the user
        
    Return:
        prompt (str): A prompt that can be used by AI models to create music that can heal 
                        user emotionally

    """
    
    response: ChatCompletion = client.chat.completions.create(
    model ="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    messages=[
            {
                "role": "system", 
                "content": f"""You are an AI that creates prompts for a music generation model based on a 
                user’s emotional memory {memory}. Your goal is to translate the core emotions of the memory 
                (e.g., joy, nostalgia, peace) into musical elements. Describe the desired mood, tempo, and 
                instruments (e.g., piano, acoustic guitar, strings) that align with the memory’s emotional 
                tone. Specify if the music should feel calm, uplifting, or reflective, with appropriate tempo 
                and chord progressions. Ensure the music evokes the memory’s emotional depth and provides 
                comfort, closure, or joy, using clear details to guide the model"""
            },
            {
                "role": "user", 
                "content": memory
            }
        ]   
    )
    
    prompt: str = response.choices[0].message.content
    return prompt