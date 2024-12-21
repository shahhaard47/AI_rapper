# utils/chat.py
import streamlit as st
from utils.chat_db import init_db, save_chat, load_chats

def summarize_chat(client, messages):
    """Generate a summary for the chat."""
    try:
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages + [{"role": "system", "content": "Summarize this conversation in a concise name."}],
            max_tokens=20
        )
        return summary_response.choices[0].message.content.strip().replace('"', '')
    except Exception as e:
        return "Chat Summary"

class ChatManager:
    def __init__(self, username, client):
        self.username = username
        self.client = client

        # Initialize database
        init_db()

        # Load chats from the database
        self.user_chats = load_chats(username)

        if "current_chat" not in st.session_state:
            st.session_state.current_chat = "New Chat"

    def save_current_chat(self):
        """Save the current chat to the database."""
        chat_name = st.session_state.current_chat
        if chat_name and chat_name in self.user_chats:
            save_chat(self.username, chat_name, self.user_chats[chat_name])

    def display_sidebar(self):
        """Display the chat management sidebar."""
        chat_names = list(self.user_chats.keys())
        if st.session_state.current_chat not in chat_names:
            chat_names.insert(0, st.session_state.current_chat)

        selected_chat = st.selectbox("Select a chat:", options=chat_names, index=0)

        if selected_chat != st.session_state.current_chat:
            st.session_state.current_chat = selected_chat

        if st.button("Start New Chat"):
            new_chat_name = "New Chat"
            self.user_chats[new_chat_name] = []
            st.session_state.current_chat = new_chat_name

        if st.session_state.current_chat != "New Chat":
            new_name = st.text_input("Rename current chat:", value=st.session_state.current_chat)
            if st.button("Rename Chat") and new_name.strip() and new_name != st.session_state.current_chat:
                self.user_chats[new_name] = self.user_chats.pop(st.session_state.current_chat)
                st.session_state.current_chat = new_name

    def display_chat(self):
        """Display the chat messages."""
        current_chat = st.session_state.current_chat
        if current_chat not in self.user_chats:
            self.user_chats[current_chat] = []

        st.session_state.messages = self.user_chats[current_chat]

        if current_chat == "New Chat" and len(st.session_state.messages) >= 2:
            new_chat_name = summarize_chat(self.client, st.session_state.messages).replace('"', '')
            if new_chat_name not in self.user_chats:
                self.user_chats[new_chat_name] = st.session_state.messages
            st.session_state.current_chat = new_chat_name
            if "New Chat" in self.user_chats:
                del self.user_chats["New Chat"]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Save the chat after displaying
        self.save_current_chat()

    def handle_user_input(self, prompt):
        """Handle user input and save chat state."""
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            max_tokens=150
        )
        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        self.user_chats[st.session_state.current_chat] = st.session_state.messages
        self.save_current_chat()
