
import streamlit as st
import subprocess
import ollama
import requests
from services.ollama_services import get_openai_client_from_ollama, get_ollama_models_as_list
from openai import OpenAI
import time


client = get_openai_client_from_ollama()
models = get_ollama_models_as_list()

MODEL = st.sidebar.selectbox("Select a model", models, index=len(models)-1)
def get_time():
    return  time.strftime("%H:%M:%S", time.localtime())
    
def ask_ollama(messages):
    start_time = time.time()
    response = client.chat.completions.create(model=MODEL, messages=messages)
    end_time = time.time()
    st.markdown(f"Responded in {end_time-start_time} seconds.")
    return response.choices[0].message.content

def initialize_the_message_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        system_message = "You are a helpful assistant who always responds in markdown and in short sentences."
        st.session_state.messages.append({'role':'system', 'content': system_message})
        st.session_state.messages.append({'role':'assistant', 'content': 'How may I help you?'})

def write_message_history_to_chat_window():
    for message in st.session_state.messages:
        if message['role']!= 'system':
            with st.chat_message(message['role']):
                st.markdown(message['content'])


def get_user_to_ask_question_to_ollama():
    user_question = st.chat_input("What's on your mind today?")
    if user_question:
        with st.chat_message('user'):
            st.markdown( user_question)
        st.markdown(f"timestamp: {get_time()}")
        st.session_state.messages.append({'role':'user', 'content': user_question})

def write_assistant_message_to_chat_window(assistant_message):
    with st.chat_message('assistant'):
        st.markdown(assistant_message)
    st.session_state.messages.append({'role': 'assistant', 'content': assistant_message})



def main():
    initialize_the_message_history()
    write_message_history_to_chat_window()
    get_user_to_ask_question_to_ollama()
    assistant_message = ask_ollama(st.session_state.messages)
    write_assistant_message_to_chat_window(assistant_message)

if __name__=="__main__":
    main()