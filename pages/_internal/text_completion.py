import streamlit as st
from services.ollama_services import get_openai_client_from_ollama
from services.measurements import measure_execution_time
client = get_openai_client_from_ollama()

@measure_execution_time
def get_prompt_response(prompt):
        response = client.completions.create(model="llama3.2", prompt=prompt)
        return response

    
def run_text_completion():
    st.write("This tab uses client.completion.create with prompt.")
    if prompt:= st.chat_input("What's on your mind today?",key='text_completion'):
        with st.spinner('Thinking...', show_time=True):
            response,t  = get_prompt_response(prompt)
        st.markdown (t)
            
        st.markdown(response.choices[0].text.strip())
        st.write(f"tokens: {response.usage.total_tokens}, prompt tokens: {response.usage.prompt_tokens},completion tokens: {response.usage.completion_tokens} ")

