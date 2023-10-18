import streamlit as st
import psycopg2
from passlib.hash import pbkdf2_sha256

st.title("User Registration and Login")

# Function to register a user
def register_user(username, password):
    conn = psycopg2.connect(
        database="blockchain",
        user="postgres",  
        password="Frank1320!5",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Username already exists. Please choose a different one.")
    else:
        # Hash the password
        password_hash = pbkdf2_sha256.hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        st.success("User registered successfully!")

    conn.close()

# Function to log in a user
def login_user(username, password):
    conn = psycopg2.connect(
        database="blockchain",
        user="postgres",
        password="Frank1320!5",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, stored_password = user_data
        if pbkdf2_sha256.verify(password, stored_password):
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")
    else:
        st.error("User not found. Please register first.")

    conn.close()

page = st.radio("Select a Page", ["Register", "Login"])

if page == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        register_user(username, password)

if page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login_user(username, password)