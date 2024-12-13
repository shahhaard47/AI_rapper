# Project Structure for Basic Chatting App

# Directory Layout

# chatgpt_streamlit/
# |-- app.py  # Streamlit app entry point
# |-- config.py  # Configuration file for API keys and settings
# |-- requirements.txt  # Python dependencies
# |-- utils/
# |   |-- __init__.py
# |   |-- openai_helpers.py  # Wrapper for OpenAI API calls
# |-- .gitignore  # To exclude sensitive files from git

# app.py (basic Streamlit app)
import streamlit as st
import hashlib
from utils.openai_helpers import get_chatgpt_response
import config
from openai import OpenAI

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load credentials from secrets
credentials = st.secrets["credentials"]
hashed_credentials = {user: hash_password(pwd) for user, pwd in credentials.items()}

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# Login form 
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in hashed_credentials and hash_password(password) == hashed_credentials[username]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")

    # Set your OpenAI API key
    if 'client' not in st.session_state:
        st.session_state['client'] = OpenAI(api_key=config.OPENAI_API_KEY)

    st.title("Chat with GPT")

    # Initialize or retrieve chat history for the logged-in user
    user = st.session_state.username
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = {}
    if user not in st.session_state.chat_histories:
        st.session_state.chat_histories[user] = {}

    user_chats = st.session_state.chat_histories[user]

    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "New Chat"

    # Function to summarize chat
    def summarize_chat(messages):
        try:
            summary_response = st.session_state.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages + [{"role": "system", "content": "Summarize this conversation in a concise name."}],
                max_tokens=20
            )
            return summary_response.choices[0].message.content.strip().replace('"', '')
        except Exception as e:
            return "Chat Summary"

    # Sidebar for chat selection and new chat creation
    with st.sidebar:
        st.header("Chats")

        # List existing chats
        chat_names = list(user_chats.keys())
        if st.session_state.current_chat not in chat_names:
            chat_names.insert(0, st.session_state.current_chat)

        selected_chat = st.selectbox("Select a chat:", options=chat_names, index=0)

        if selected_chat != st.session_state.current_chat:
            st.session_state.current_chat = selected_chat

        # Start a new chat
        if st.button("Start New Chat"):
            new_chat_name = "New Chat"
            user_chats[new_chat_name] = []
            st.session_state.current_chat = new_chat_name

        # Allow renaming the current chat
        if st.session_state.current_chat != "New Chat":
            new_name = st.text_input("Rename current chat:", value=st.session_state.current_chat)
            if st.button("Rename Chat") and new_name.strip() and new_name != st.session_state.current_chat:
                # Rename the chat in the history
                user_chats[new_name] = user_chats.pop(st.session_state.current_chat)
                st.session_state.current_chat = new_name

    # Initialize messages for the current chat
    if st.session_state.current_chat not in user_chats:
        user_chats[st.session_state.current_chat] = []

    st.session_state.messages = user_chats[st.session_state.current_chat]

    # Automatically name the chat after two messages
    if st.session_state.current_chat == "New Chat" and len(st.session_state.messages) >= 2:
        new_chat_name = summarize_chat(st.session_state.messages).replace('"', '')
        if new_chat_name not in user_chats:
            user_chats[new_chat_name] = st.session_state.messages
        st.session_state.current_chat = new_chat_name
        if "New Chat" in user_chats:
            del user_chats["New Chat"]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input and response handling
    if prompt := st.chat_input("Ask me anything:"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response using OpenAI's API
        response = st.session_state.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            max_tokens=150
        )
        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Update chat history
    user_chats[st.session_state.current_chat] = st.session_state.messages
