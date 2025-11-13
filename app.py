
import streamlit as st
import subprocess
import ollama
import requests
from services.ollama_services import get_ollama_url, get_ollama_models_as_list
from openai import OpenAI

# url, started, message  = get_ollama_url()
# url = url +'/v1'
# print(url)
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# client = OpenAI(base_url=url, api_key='ollama')
models = get_ollama_models_as_list()

MODEL = st.sidebar.selectbox("Select a model", models, index=len(models)-1)
if "messages" not in st.session_state:
    st.session_state.messages = []
    system_message = "You are a helpful assistant"
    st.session_state.messages.append({'role':'system', 'content': system_message})
    st.session_state.messages.append({'role':'assistant', 'content': 'How may I help you?'})

for message in st.session_state.messages:
    if message['role']!= 'system':
        with st.chat_message(message['role']):
            st.markdown(message['content'])

user_question = st.chat_input("What's on your mind today?")

if user_question:
    with st.chat_message('user'):
        st.markdown( user_question)
    st.session_state.messages.append({'role':'user', 'content': user_question})
    model_response = client.chat.completions.create(
            messages=st.session_state.messages
            , model= MODEL
            , stream=False    
        )
    assistant_message = model_response.choices[0].message.content
    with st.chat_message('assistant'):
        st.markdown(assistant_message)
    st.session_state.messages.append({'role': 'assistant', 'content': assistant_message})
    print(f"MODEL RESPONSE: {assistant_message}")
