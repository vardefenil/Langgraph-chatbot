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


# Loading conversation history
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


    # Stream AI response
    with st.chat_message("assistant"):

        def generate_response():

            for message_chunk, metadata in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG,
                stream_mode="messages"
            ):

                content = message_chunk.content

                if isinstance(content, list):

                    for item in content:

                        if (
                            isinstance(item, dict)
                            and item.get("type") == "text"
                        ):
                            yield item.get("text", "")

                elif isinstance(content, str):

                    yield content


        ai_message = st.write_stream(generate_response())


    # Save AI response
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })