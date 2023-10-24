import streamlit as st
import psycopg2
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
import os

load_dotenv()

class UserManager:
    def __init__(self):
        # Read configuration from .env file
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_NAME2 = os.getenv('DB_NAME2')
       
    def set_authenticated(self, username, value):
        st.session_state[username + '_authenticated'] = value

    def is_authenticated(self, username):
        if username + '_authenticated' not in st.session_state:
            st.session_state[username + '_authenticated'] = False
        return st.session_state[username + '_authenticated']
    
    def register_user(self, username, password):
        conn = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            password_hash = pbkdf2_sha256.hash(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
            conn.commit()
            st.success("User registered successfully!")

        conn.close()

    def login_user(self, username, password, session_state):
        conn = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, stored_password = user_data
            if pbkdf2_sha256.verify(password, stored_password):
                st.success("Login successful!")
                st.session_state.authenticated = True  # Set the user as authenticated
            else:
                st.error("Invalid credentials. Please try again.")
        else:
            st.error("User not found. Please register first.")

        conn.close()

    def logout(self):
        st.session_state["authenticated_user"] = None

    # Modify this method to store chat messages in st.session_state
    def add_chat_message(self, username, message):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append({"role": username, "content": message})

    # Modify this method to retrieve chat messages from st.session_state
    def get_chat_messages(self):
        if "messages" in st.session_state:
            return st.session_state.messages
        else:
            return []
        
    def is_admin(self, username):
        conn = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("SELECT admin FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] is True:
            return True
        else:
            return False