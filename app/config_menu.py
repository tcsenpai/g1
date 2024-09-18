import streamlit as st
import os
from dotenv import load_dotenv, set_key

def load_env_vars():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return {
        'OLLAMA_URL': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
        'OLLAMA_MODEL': os.getenv('OLLAMA_MODEL', 'mistral'),
        'PERPLEXITY_API_KEY': os.getenv('PERPLEXITY_API_KEY', ''),
        'PERPLEXITY_MODEL': os.getenv('PERPLEXITY_MODEL', 'mistral-7b-instruct'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
        'GROQ_MODEL': os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
    }

def save_env_vars(config):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    for key, value in config.items():
        set_key(env_path, key, value)

def config_menu():
    st.sidebar.markdown("## 🛠️ Configuration")
    
    config = load_env_vars()
    
    with st.sidebar.expander("Edit Configuration"):
        new_config = {}
        new_config['OLLAMA_URL'] = st.text_input("Ollama URL", value=config['OLLAMA_URL'])
        new_config['OLLAMA_MODEL'] = st.text_input("Ollama Model", value=config['OLLAMA_MODEL'])
        new_config['PERPLEXITY_API_KEY'] = st.text_input("Perplexity API Key", value=config['PERPLEXITY_API_KEY'], type="password")
        new_config['PERPLEXITY_MODEL'] = st.text_input("Perplexity Model", value=config['PERPLEXITY_MODEL'])
        new_config['GROQ_API_KEY'] = st.text_input("Groq API Key", value=config['GROQ_API_KEY'], type="password")
        new_config['GROQ_MODEL'] = st.text_input("Groq Model", value=config['GROQ_MODEL'])
        
        if st.button("Save Configuration"):
            save_env_vars(new_config)
            st.success("Configuration saved successfully!")
    
    return config

def display_config(backend, config):
    st.sidebar.markdown("## 🛠️ Current Configuration")
    if backend == "Ollama":
        st.sidebar.markdown(f"- 🖥️ Ollama URL: `{config['OLLAMA_URL']}`")
        st.sidebar.markdown(f"- 🤖 Ollama Model: `{config['OLLAMA_MODEL']}`")
    elif backend == "Perplexity AI":
        st.sidebar.markdown(f"- 🧠 Perplexity AI Model: `{config['PERPLEXITY_MODEL']}`")
    elif backend == "Groq":
        st.sidebar.markdown(f"- ⚡ Groq Model: `{config['GROQ_MODEL']}`")
