import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

st.title("GPT Chatbot with Web Search 🔍")

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your_openai_api_key_here":
    st.error("Please set your OPENAI_API_KEY in the .env file")
    st.info("Get your API key from: https://platform.openai.com/api-keys")
    st.stop()

client = OpenAI(api_key=api_key)

# Add web search toggle in sidebar
with st.sidebar:
    st.header("Settings")
    enable_search = st.toggle("Enable Web Search", value=True)
    force_search = st.checkbox("Force search on ALL queries", value=True)

    if enable_search:
        st.success("🔍 Web search is ENABLED")
        st.caption("Auto-detects when to search based on keywords")
    else:
        st.info("Web search is disabled")

    if force_search:
        st.warning("⚡ Forcing search on EVERY message")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to perform web search
def web_search(query, max_results=5):
    """Search the web using DuckDuckGo"""
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return None

        search_summary = ""
        for i, result in enumerate(results, 1):
            search_summary += f"[Source {i}] {result['title']}\n"
            search_summary += f"{result['body']}\n"
            search_summary += f"URL: {result['href']}\n\n"

        return search_summary
    except Exception as e:
        st.warning(f"Search failed: {str(e)}")
        return None

# Function to determine if web search is needed
def needs_web_search(prompt):
    """Check if the query might benefit from web search"""
    # More comprehensive keyword list
    search_keywords = [
        "latest", "current", "news", "today", "recent", "2024", "2025",
        "what is happening", "what's happening", "what is", "what's",
        "search", "find", "look up", "weather", "temperature", "forecast",
        "stock", "price", "score", "update", "now", "right now",
        "this week", "this month", "this year", "recently", "tell me about",
        "information about", "nyc", "new york"
    ]
    prompt_lower = prompt.lower()
    # Return True if ANY keyword is found
    has_keyword = any(keyword in prompt_lower for keyword in search_keywords)

    # Also search if the query is a question (ends with ?)
    is_question = "?" in prompt

    return has_keyword or is_question

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to talk about?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if web search is needed and enabled
    search_results = None
    should_search = force_search or needs_web_search(prompt)

    if enable_search and should_search:
        with st.spinner("🔍 Searching..."):
            search_results = web_search(prompt)

    # Prepare messages for OpenAI - build the API messages fresh each time
    messages_for_api = []

    # Add system message with search results if available
    if search_results:
        system_prompt = f"""CRITICAL INSTRUCTIONS - READ CAREFULLY:

The user asked: "{prompt}"

I have performed a LIVE INTERNET SEARCH and retrieved the following CURRENT, UP-TO-DATE information:

=== WEB SEARCH RESULTS ===
{search_results}
=== END OF SEARCH RESULTS ===

YOUR TASK:
1. Read the search results above
2. Answer the user's question using ONLY this information
3. DO NOT under ANY circumstances say "I don't have access to real-time information"
4. DO NOT say "I cannot browse the internet"
5. DO NOT apologize for not having current data
6. You MUST use the search results provided above
7. Cite sources by including the URLs

If you say you don't have internet access, you will be incorrect - the search was already performed and the results are right above."""
        messages_for_api.append({"role": "system", "content": system_prompt})

    # Add only the LAST user message (not full history when we have search results)
    # This prevents the AI from seeing its own previous "I don't have internet" responses
    if search_results:
        messages_for_api.append({"role": "user", "content": prompt})
    else:
        # No search results, use full conversation history
        for msg in st.session_state.messages:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})

    # Call OpenAI API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Create the message with streaming
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history (without the system message)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
