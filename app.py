import streamlit as st
from user_manager import UserManager  # Import the UserManager class from the user_manager module

st.title("User Registration and Login")

# Initialize the user manager
user_manager = UserManager('config.yaml')

# Streamlit page selection
page = st.radio("Select a Page", ["Register", "Login"])

if page == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        user_manager.register_user(username, password)

if page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_manager.login_user(username, password)
