# utils/auth.py
import hashlib
import streamlit as st

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate the user by comparing hashed credentials."""
    credentials = st.secrets["credentials"]
    hashed_credentials = {user: hash_password(pwd) for user, pwd in credentials.items()}

    return username in hashed_credentials and hash_password(password) == hashed_credentials[username]
