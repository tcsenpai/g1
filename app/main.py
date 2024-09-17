import streamlit as st
from dotenv import load_dotenv
from api_handlers import OllamaHandler, PerplexityHandler, GroqHandler
from utils import generate_response
from config_menu import config_menu, display_config
from logger import logger
import os

# Load environment variables from .env file
load_dotenv()

def load_css():
    # Load custom CSS styles
    with open(os.path.join(os.path.dirname(__file__), "..", "static", "styles.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def setup_page():
    # Configure the Streamlit page
    st.set_page_config(page_title="multi1 - Unified AI Reasoning Chains", page_icon="🧠", layout="wide")
    load_css()
    
    # Display the main title
    st.markdown("""
    <h1 class="main-title">
        🧠 multi1 - Unified AI Reasoning Chains
    </h1>
    """, unsafe_allow_html=True)
    
    # Display the app description
    st.markdown("""
    <p class="main-description">
        This app demonstrates AI reasoning chains using different backends: Ollama, Perplexity AI, and Groq.
        Choose a backend and enter your query to see the step-by-step reasoning process.
    </p>
    """, unsafe_allow_html=True)

def get_api_handler(backend, config):
    # Create and return the appropriate API handler based on the selected backend
    if backend == "Ollama":
        return OllamaHandler(config['OLLAMA_URL'], config['OLLAMA_MODEL'])
    elif backend == "Perplexity AI":
        return PerplexityHandler(config['PERPLEXITY_API_KEY'], config['PERPLEXITY_MODEL'])
    else:  # Groq
        return GroqHandler(config['GROQ_API_KEY'], config['GROQ_MODEL'])

def main():
    logger.info("Starting the application")
    setup_page()

    # Set up the sidebar for configuration
    st.sidebar.markdown('<h3 class="sidebar-title">⚙️ Settings</h3>', unsafe_allow_html=True)
    config = config_menu()
    
    # Allow user to select the AI backend
    backend = st.sidebar.selectbox("Choose AI Backend", ["Ollama", "Perplexity AI", "Groq"])
    display_config(backend, config)
    api_handler = get_api_handler(backend, config)
    logger.info(f"Selected backend: {backend}")

    # User input field
    user_query = st.text_input("💬 Enter your query:", placeholder="e.g., How many 'R's are in the word strawberry?")

    if user_query:
        logger.info(f"Received user query: {user_query}")
        st.write("🔍 Generating response...")
        response_container = st.empty()
        time_container = st.empty()

        try:
            # Generate and display the response
            for steps, total_thinking_time in generate_response(user_query, api_handler):
                with response_container.container():
                    for title, content, _ in steps:
                        if title.startswith("Final Answer"):
                            # Display the final answer
                            st.markdown(f'<h3 class="expander-title">🎯 {title}</h3>', unsafe_allow_html=True)
                            st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                            logger.info(f"Final answer generated: {content}")
                        else:
                            # Display intermediate steps
                            with st.expander(f"📝 {title}", expanded=True):
                                st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                            logger.debug(f"Step completed: {title}")

                # Display total thinking time
                if total_thinking_time is not None:
                    time_container.markdown(f'<p class="thinking-time">⏱️ Total thinking time: {total_thinking_time:.2f} seconds</p>', unsafe_allow_html=True)
                    logger.info(f"Total thinking time: {total_thinking_time:.2f} seconds")
        except Exception as e:
            # Handle and display any errors
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            st.error("An error occurred while generating the response. Please try again.")

if __name__ == "__main__":
    main()