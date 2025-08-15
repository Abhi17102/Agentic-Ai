import os
import random
import webbrowser
import wikipedia
from datetime import datetime

import streamlit as st
from langchain.agents import tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Set Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBq7Mg_a-no6SvecmbLaQy8NhWXSpZN8sg"

# ✅ Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# ✅ TOOL 1: Multiply by 4
@tool
def lwmul(x: str) -> str:
    """Multiplies the given number by 4."""
    try:
        num = int(x.strip())
        return f"{num} * 4 = {num * 4}"
    except ValueError:
        return "Please provide a valid number."

# ✅ TOOL 2: Get current date & time
@tool
def get_datetime(_: str) -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ✅ TOOL 3: Wikipedia search
@tool
def wiki_search(topic: str) -> str:
    """Searches Wikipedia and returns a short summary."""
    try:
        return wikipedia.summary(topic, sentences=2)
    except Exception:
        return "I couldn’t find anything on Wikipedia for that topic."

# ✅ TOOL 4: Random motivational quote
@tool
def random_quote(_: str) -> str:
    """Returns a random motivational quote."""
    quotes = [
        "Believe in yourself and all that you are.",
        "Success is not final, failure is not fatal.",
        "Do something today that your future self will thank you for.",
        "Hard work beats talent when talent doesn’t work hard.",
        "Great things never come from comfort zones."
    ]
    return random.choice(quotes)

# ✅ TOOL 5: Open Spotify
@tool
def open_spotify(_: str) -> str:
    """Opens Spotify in your browser."""
    url = "https://open.spotify.com/"
    webbrowser.open(url)
    return "Spotify opened in your browser!"

# ✅ Combine tools
tools = [lwmul, get_datetime, wiki_search, random_quote, open_spotify]

# ✅ Initialize agent (NOW WORKS!)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# =========================
# ✅ STREAMLIT UI
# =========================
st.set_page_config(page_title="AI Multi-Tool Assistant", page_icon="🤖")

st.title("🤖 AI Multi-Tool Assistant")
st.write("Type a command like:")
st.markdown("""
- **Multiply 7 by 4**  
- **What is the current date and time?**  
- **Search Wikipedia for Python programming**  
- **Give me a motivational quote**  
- **Open Spotify**
""")

# ✅ User input
user_command = st.text_input("👉 Enter your command:")

if st.button("Run Command"):
    if user_command.strip():
        with st.spinner("🤔 Thinking..."):
            try:
                result = agent.run(user_command)
                st.success(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a command first!")

# ✅ Optional: Show available tools
with st.expander("Available Tools"):
    st.write("""
    - **Multiply by 4**  
    - **Get current date & time**  
    - **Wikipedia search**  
    - **Random motivational quote**  
    - **Open Spotify**
    """)
