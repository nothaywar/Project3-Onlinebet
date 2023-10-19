import streamlit as st
from UserManager import UserManager  # Import the UserManager class from the user_manager module

st.title("User Registration and Login")

# Initialize the user manager
user_manager = UserManager()

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

# Check if the user is authenticated and redirect to the chatroom subapp
if user_manager.is_authenticated(username):
    st.subapp("Chatroom", chatroom, username)
