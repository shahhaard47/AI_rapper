# app.py
import streamlit as st
from utils.auth import authenticate_user
from utils.chat import ChatManager
import config
from openai import OpenAI

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# Login and authentication
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")

    # Set up OpenAI client
    if 'client' not in st.session_state:
        st.session_state['client'] = OpenAI(api_key=config.OPENAI_API_KEY)

    chat_manager = ChatManager(st.session_state.username, st.session_state['client'])

    st.title("Chat with GPT")

    # Sidebar for chat selection and new chat creation
    with st.sidebar:
        st.header("Chats")

        chat_manager.display_sidebar()

    # Display and handle chat messages
    chat_manager.display_chat()

    # Handle new user input
    prompt = st.chat_input("Ask me anything:")
    if prompt:
        chat_manager.handle_user_input(prompt)
