import streamlit as st
from pages._internal.simple_chat import run_simple_chat

simple_chat, chat_with_history = st.tabs(tabs=['simple chat', 'chat with history'])

with simple_chat:
    run_simple_chat()