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
    streaming=True
)

def store_chat_history(memory: str, ai_response: str):
    """
    Store the chat history in a file.
    
    Arguments:
        memory (str): The memory provided by the user.
        ai_response (str): The AI's emotional therapy response.
    """
    with open("chat_history.txt", "a") as f:
        f.write(f"User: {memory}\n")
        f.write(f"AI: {ai_response}\n")
        f.write("-" * 40 + "\n")

def emotion_therapy(memory: str):
    """
    Recieves a memory from user, which is processed by AI and provides emotional therapy to the user.
    
    Arguments:
        memory (str): The memory from the user.
        
    Return:
        ai_response (str): An emotional therapy response to the user from AI.
    """
    response = client.stream([
        SystemMessage(content=f"""You are an empathetic AI therapist designed to help users process and heal from emotional memories. You will be provided a memory {memory} and your goal is to provide compassionate support, validate the user’s feelings, and offer therapeutic insights based on the emotions conveyed. First, identify the core emotion (e.g., sadness, anger, joy), then reflect back with empathy, validating the user’s experience. Provide tailored therapeutic techniques such as cognitive reframing, mindfulness, self-compassion, or closure techniques, to help the user emotionally heal. Encourage positive actions and self-care, while maintaining a respectful, non-judgmental, and sensitive approach to foster growth and resilience, always ensuring the user feels safe and understood."""),
        HumanMessage(content=memory)
    ])

    # Process the response and yield the output while storing chat history
    for chunk in response:
        if chunk.content is not None:
            ai_response = chunk.content
            yield ai_response
            store_chat_history(memory, ai_response)  # Save memory and AI response to chat history
