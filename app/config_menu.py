import streamlit as st
import os
from dotenv import load_dotenv, set_key
from dataclasses import dataclass

@dataclass
class StInputs:
    model:str
    api_key:str
    temperature:float
    timeout:float
    sleeptime:float
    max_steps:int
    max_tokens:int
    
    
def load_env_vars():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return {
        'MODEL': os.getenv('MODEL', 'gemini/gemini-1.5-pro'),
        "MODEL_API_KEY": os.getenv("MODEL_API_KEY", ""),
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
        model = new_config['MODEL'] = st.text_input("Model (in Litellm style, provider/llm-name)", value=config['MODEL'], placeholder='openai/gpt-3.5-turbo') 
        api_key = new_config['MODEL_API_KEY'] = st.text_input("Model API Key", value=config['MODEL_API_KEY'], placeholder='api key here') 
        timeout = st.number_input("Timout",           value=30.0, min_value=1.0, max_value=60.0, step=1.0)  
        max_tokens =st.number_input("Max Tokens",     value=512, min_value=300, max_value=2048, step = 100)  
        temperature =st.number_input("Temperature",   value=0.1, min_value=0.0, max_value=2.0, step=0.1)
        max_steps = st.number_input("Max Steps (number of reasoning steps)",      value=20, min_value=1, max_value=20, step=1)
        sleeptime = st.number_input("Sleeptime between request hits(to avoid too many requests error)" ,value=1.0, min_value=0.0, max_value=30.0, step=1.0)
        
        if st.button("Save Configuration"):
            save_env_vars(new_config)
            st.success("Configuration saved successfully!")
    
    inputs = StInputs(
        model=model,
        api_key=api_key,
        timeout=timeout,
        max_tokens=max_tokens,
        temperature=temperature,
        max_steps=max_steps,
        sleeptime=sleeptime
    )

    return inputs

