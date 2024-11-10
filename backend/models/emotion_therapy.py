import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.schema import AIMessage
load_dotenv()

class State(TypedDict): 
    messages: Annotated[list, add_messages]
llm_model = ChatGroq(
    model="llama-3.2-1b-preview",
    verbose=True,
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
)

def chatbot(state: State):
    return {"messages": [llm_model.invoke(state["messages"])]}


memory = MemorySaver()

def therapy_agent():
  graph_builder = StateGraph(State)

  graph_builder.add_node("chatbot", chatbot)

  graph_builder.add_edge(START, "chatbot")
  graph_builder.add_edge("chatbot", END)

  graph = graph_builder.compile(checkpointer=memory)
  return graph

def emotion_therapy(memory: str):
  graph = therapy_agent()
  messages = []
  config = {"configurable": {"thread_id": "1556"}}
  events = graph.stream(
      {"messages": [("user", memory)]},  # Changed here
      config=config,
      stream_mode="values"
  )
  for event in events:
      messages.extend(event['messages'])  # Collect each event message

  # Filter for the last AIMessage in the accumulated messages
  ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
  return ai_messages[-1].content if ai_messages else None  # Return the last AI message if available
