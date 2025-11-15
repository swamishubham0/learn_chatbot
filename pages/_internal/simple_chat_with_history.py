
import streamlit as st
import subprocess
import ollama
import requests
from services.ollama_services import get_openai_client_from_ollama, get_ollama_models_as_list
from openai import OpenAI
import time


# Initialize the OpenAI client and get available models
client = get_openai_client_from_ollama()
models = get_ollama_models_as_list()

def get_time():
    return  time.strftime("%H:%M:%S", time.localtime())
    
def ask_ollama(messages, model):
    start_time = time.time()
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=250)
    end_time = time.time()
    st.markdown(f"Responded in {end_time-start_time} seconds.")
    return response.choices[0].message.content

def initialize_the_message_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        system_message = """
            You are a precise, concise AI assistant.
            - Answer ONLY to the user's latest message.
            - DO NOT summarize or expand previous messages.
            - DO NOT continue facts unless explicitly asked.
            - Do NOT invent additional information.
            Always respond in short markdown sentences.
            """
        st.session_state.messages.append({'role':'system', 'content': system_message})
        st.session_state.messages.append({'role':'assistant', 'content': 'How may I help you?'})


def run_simple_chat():
    # Model selection in sidebar
    st.sidebar.title("Model Settings")
    MODEL = st.sidebar.selectbox("Select a model", models, index=len(models)-4)
    st.write("This chat uses chat.completion.create with history of the chat.")
    
    # Initialize message history if needed
    initialize_the_message_history()
    
    # Create a container for messages
    messages_container = st.container()
    
    # Display existing messages
    with messages_container:
        for message in st.session_state.messages:
            if message['role'] != 'system':
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
    
    # Chat input at the bottom (outside the container)
    prompt = st.chat_input("What's on your mind today?")
    
    if prompt:
        # Add user message to history
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        
        # Get assistant response

        with st.spinner('Thinking...'):
            response = ask_ollama(st.session_state.messages, MODEL)
        
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        # Rerun to update the display with new messages
        st.rerun()


if __name__=="__main__":
    run_simple_chat()