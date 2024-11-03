import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

base_url = 'https://api.rhymes.ai/v1'
api_key = os.getenv("ARIA_API_KEY")

client: ChatOpenAI = ChatOpenAI(
    model="aria",
    base_url=base_url,
    api_key=api_key,
    max_tokens=512
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

    response = client.invoke([
        SystemMessage(content=f"""You are an AI that creates prompts for a music generation model based on a user’s emotional memory {memory}. Your goal is to translate the core emotions of the memory 
                (e.g., joy, nostalgia, peace) into musical elements. Describe the desired mood, tempo, and instruments (e.g., piano, acoustic guitar, strings) that align with the memory’s emotional tone. Specify if the music should feel calm, uplifting, or reflective, with appropriate tempo and chord progressions. Ensure the music evokes the memory’s emotional depth and provides comfort, closure, or joy, using clear details to guide the model"""),
        HumanMessage(content=memory)
    ])
    
    prompt: AIMessage = response.content
    return prompt