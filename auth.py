import streamlit as st
from database import add_user, login_user

def login_page():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful 🎉")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")

def signup_page():
    st.subheader("Create New Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            add_user(username, email, password)
            st.success("Account Created Successfully 🎉")
        except:
            st.error("Username already exists ❌")
