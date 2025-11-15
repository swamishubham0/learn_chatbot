import streamlit as st
from pages._internal.simple_chat_with_history import run_simple_chat
from pages._internal.text_completion import run_text_completion

simple_chat, text_completion, chat_with_history = st.tabs(tabs=['simple Chat', 'Text Completion', 'chat with history'])

with simple_chat:
    run_simple_chat()

with text_completion:
    run_text_completion()    
