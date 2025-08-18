import streamlit as st
from chatbot import HistoryChatBot
from config import MODEL_NAME, PROMPT_TEMPLATE

st.title("AI History Chatbot")
st.write("Ask any history question you will get fun and factually answers with a quiz in the end, Type Exit to start new chat.")

# Initialize the prompt message
if "messages" not in st.session_state:
     st.session_state.messages = []
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = HistoryChatBot(MODEL_NAME, PROMPT_TEMPLATE)
    except Exception as e:
        st.write(e)
        st.write(e)
        st.error("Unable to import Olama")
        st.stop()

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# User Input
user_input = st.chat_input("Please type your Query: ")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    # creating history of user inputs
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    if user_input.lower().strip()=="exit":
        st.session_state.messages = []
        st.session_state.chatbot.clear_memory()
    else:
        try:
            response = st.session_state.chatbot.get_response(user_input)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({'role': 'assistant', 'content': response})
        except Exception as e:
            print(e)
            st.error("Unable to Get Response from Ollama")