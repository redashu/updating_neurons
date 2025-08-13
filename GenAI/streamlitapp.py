import os
import streamlit as st
from openai import OpenAI

# Set your OpenAI API key
# Option 1: Hardcode (not recommended for production)
# os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxx"

# Option 2: Use environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-proj-"))

st.set_page_config(page_title="Azure VM Chatbot", page_icon="🤖", layout="centered")

st.title("💬 Chatbot with OpenAI GPT-4o-mini")
st.markdown("This chatbot runs on your **Azure VM** using **Streamlit**.")

# Store chat history in Streamlit session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input box
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Append user message to history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Send to OpenAI
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input
        )
        bot_reply = response.output_text
    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"

    # Append bot message to history
    st.session_state.history.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
