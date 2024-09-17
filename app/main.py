from time import sleep
import streamlit as st
from dotenv import load_dotenv
from api_handlers import LitellmHandler
from utils import generate_response
from config_menu import config_menu
from logger import logger
import os

# Load environment variables
load_dotenv()

def load_css():
    with open(os.path.join(os.path.dirname(__file__), "..", "static", "styles.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def setup_page():
    st.set_page_config(page_title="multi1 - Unified AI Reasoning Chains", page_icon="🧠", layout="wide")
    load_css()
    st.markdown("""
    <h1 class="main-title">
        🧠 multi1 - Unified AI Reasoning Chains
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p class="main-description">
        This app demonstrates AI reasoning chains using different backends: Ollama, Perplexity AI, and Groq.
        Choose a backend and enter your query to see the step-by-step reasoning process.
    </p>
    """, unsafe_allow_html=True)

def get_api_handler(model, api_key):
    return LitellmHandler(model=model, api_key=api_key)

def main():
    logger.info("Starting the application")
    setup_page()

    st.sidebar.markdown('<h3 class="sidebar-title">⚙️ Settings</h3>', unsafe_allow_html=True)
    config = config_menu()
    
    api_handler = get_api_handler(model=config.model, api_key=config.api_key)

    user_query = st.text_input("💬 Enter your query:", placeholder="e.g., How many 'R's are in the word strawberry?")

    if user_query:
        logger.info(f"Received user query: {user_query}")
        st.write("🔍 Generating response...")
        response_container = st.empty()
        time_container = st.empty()


        max_steps=    config.max_steps
        max_tokens=   config.max_tokens
        temperature=  config.temperature
        timeout=      config.timeout
        sleeptime=    config.sleeptime
        
        try:
            for steps, total_thinking_time in generate_response(user_query, api_handler, max_steps=max_steps, max_tokens=max_tokens, temperature=temperature, timeout=timeout, sleeptime=sleeptime):
                with response_container.container():
                    for title, content, _ in steps:
                        if title.startswith("Final Answer"):
                            st.markdown(f'<h3 class="expander-title">🎯 {title}</h3>', unsafe_allow_html=True)
                            st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                            logger.info(f"Final answer generated: {content}")
                        else:
                            with st.expander(f"📝 {title}", expanded=True):
                                st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                            logger.debug(f"Step completed: {title}")

                if total_thinking_time is not None:
                    time_container.markdown(f'<p class="thinking-time">⏱️ Total thinking time: {total_thinking_time:.2f} seconds</p>', unsafe_allow_html=True)
                    logger.info(f"Total thinking time: {total_thinking_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            st.error("An error occurred while generating the response. Please try again.")

if __name__ == "__main__":
    main()