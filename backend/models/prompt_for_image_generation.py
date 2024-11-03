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
    streaming=False,
    max_tokens=512
)

def prompt_for_images(memory: str)-> str:
    """
    Recieves a memory from user, which is processed by AI and returns a prompt that can be used
    by AI models to create image that can heal user emotionally
    
    Arguments:
        memory (str): The memory from the user
        
    Return:
        prompt (str): A prompt that can be used by AI models to create image that can heal 
                        user emotionally

    """

    response = client.invoke([
        SystemMessage(content=f"""You are an AI designed to create prompts for an image generation model based on a user’s emotional memory {memory}. Your task is to ensure that the generated image 
                accurately reflects the memory’s specific details and emotional atmosphere. Analyze the 
                memory for key visual elements such as people, places, objects, and activities, along with the emotional tone, whether it be nostalgia, joy, peace, or any other feeling. Your prompt should clearly describe these elements, including settings, individuals involved, and any significant objects, while conveying the right mood through the description of lighting, colors, and overall atmosphere. The goal is to guide the model to create an image that not only mirrors the memory but also evokes the emotions tied to it, with sufficient detail to reflect both the context and the emotional depth of the user's recollection."""),
        HumanMessage(content=memory)
    ])
    
    prompt: AIMessage = response.content
    return prompt