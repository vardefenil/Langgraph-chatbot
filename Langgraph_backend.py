from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

class chatstate(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:chatstate):
    messages=state["messages"]
    Response=llm.invoke(messages)
    return {"messages":[Response]}

checkpointer=InMemorySaver()
graph = StateGraph(chatstate)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

    