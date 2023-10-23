import streamlit as st
from UserManager import UserManager  # Import the UserManager class from the user_manager module

# Initialize the user manager
user_manager = UserManager()

# Place the login, register, and page selection on the sidebar
st.sidebar.title("User Authentication")

if "username" not in st.session_state:
    st.session_state.username = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit page selection
state = st.sidebar.radio("Select a state", ["Register", "Login"])

if state == "Register":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        user_manager.register_user(username, password)

if state == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user_manager.login_user(username, password, st.session_state):
            st.session_state.authenticated = True
            # st.experimental_rerun()

# Render chat interface if user is authenticated
if st.session_state.authenticated:
    st.title("Chatroom")
    st.write(f"Welcome, {username} to the chatroom!")

    # Chatbox to leave messages
    message = st.text_input("Leave a message:")
    if st.button("Send"):
        user_manager.add_chat_message(username, message)

    # Display chat messages
    chat_messages = user_manager.get_chat_messages()
    for chat_message in chat_messages:
        with st.chat_message(chat_message["role"]):
            st.markdown(chat_message["content"])
