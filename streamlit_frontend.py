import streamlit as st
from Langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}


if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


# Loading the conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Type here")


if user_input:

    # Add user message to history
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)


    # Send message to LangGraph
    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=CONFIG
    )


    # Get AI response
    ai_message = response["messages"][-1].content


    # Gemini may return content as a list
    if isinstance(ai_message, list):
        ai_message = "".join(
            item["text"]
            for item in ai_message
            if isinstance(item, dict)
            and item.get("type") == "text"
        )


    # Add AI response to history
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })


    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_message)