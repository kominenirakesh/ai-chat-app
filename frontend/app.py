import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Chat App")

st.title("AI Chat App")

# Store selected thread
if "selected_thread" not in st.session_state:
    st.session_state.selected_thread = None

# Create new thread
if st.sidebar.button("➕ New Chat"):

    response = requests.post(
        f"{API_URL}/thread"
    )

    thread_data = response.json()

    st.session_state.selected_thread = thread_data["id"]

    st.rerun()

# Load threads
threads = requests.get(
    f"{API_URL}/threads"
).json()

st.sidebar.title("Chats")

# Display threads
for thread in threads:

    if st.sidebar.button(
        f"{thread['title']} ({thread['id']})"
    ):
        st.session_state.selected_thread = thread["id"]

        st.rerun()

# Load selected thread
if st.session_state.selected_thread:

    messages = requests.get(
        f"{API_URL}/messages/{st.session_state.selected_thread}"
    ).json()

    # Show messages
    for msg in messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    prompt = st.chat_input("Type a message")

    if prompt:

        requests.post(
            f"{API_URL}/chat",
            params={
                "thread_id": st.session_state.selected_thread,
                "message": prompt
            }
        )

        st.rerun()