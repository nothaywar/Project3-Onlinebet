import streamlit as st
from UserManager import UserManager  # Import the UserManager class from the user_manager module
import time
# Initialize the user manager
user_manager = UserManager()

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "team_choice": None,
        "wallet_address": "",
        "eth_amount": 0.0
    }

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
    st.title("💬Chatroom💬")
    st.write(f"Welcome, {username} to the chatroom!")

    # Chatbox to leave messages
    message = st.text_input("Leave a message:")
    if st.button("Send"):
        user_manager.add_chat_message(username, message)

    # Display chat messages
    with st.container():
        chat_messages = user_manager.get_chat_messages()
        for chat_message in chat_messages:
            with st.chat_message(chat_message["role"]):
                st.markdown(chat_message["content"])
    # Check if the user is an admin and display the button to create a game
    if user_manager.is_admin(username):
        if st.button("Create Game"):
            st.toast("🚨ADMIN is creating a game🚨")
            time.sleep(3)
            st.toast("🚨ADMIN is creating a game🚨")
            time.sleep(3)
    # Input fields for team choice, wallet address, and ETH amount
            team_choice = st.radio("Choose a Team", ["Team A", "Team B"])
            wallet_address = st.text_input("Enter Wallet Address", value=st.session_state.user_data["wallet_address"])
            eth_amount = st.number_input("Enter ETH Amount", min_value=0.0, value=st.session_state.user_data["eth_amount"])

            # Update user choices in the session state
            if st.button("Update Choices"):
                st.session_state.user_data["team_choice"] = team_choice
                st.session_state.user_data["wallet_address"] = wallet_address
                st.session_state.user_data["eth_amount"] = eth_amount