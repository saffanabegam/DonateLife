import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from website_loader import get_website_content
# -----------------
# Setup
# -----------------

load_dotenv()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
# 2. Example of generating a response for VARDAN AI
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # Or 'gemini-2.5-pro' depending on your preference
        contents="What is organ donation?",
    )
    
    # Display the answer in your chat interface
    st.write(response.text)

except Exception as e:
    st.error(f"An error occurred: {e}")
    
website_data = get_website_content()
SYSTEM_PROMPT = """
You are VARDAN AI.

Official AI assistant of Donate Life NGO,
Surat, Gujarat, India.

Your purpose:
Provide intelligent, helpful, and educational responses about organ donation and Donate Life NGO.

Answer priority:

1. Use Donate Life website information when relevant.
2. Expand naturally using Gemini knowledge.
3. Add examples only when useful.

Response Style:

- Keep responses medium length
- Usually 100–220 words
- Give direct answers first
- Use short sections
- Use bullet points only if they improve readability
- Avoid long paragraphs
- Avoid repeating information
- Explain clearly and naturally

Rules:

- Answer in a friendly and professional tone
- For Donate Life NGO questions:
  prioritize website information

- For organ donation questions:
  combine:
  • educational explanation
  • awareness information
  • website information when relevant

- If website information is limited:
  continue using Gemini knowledge

- If user asks unrelated questions:
Reply:
"I specialize in organ donation and Donate Life NGO information."

- Do not provide medical diagnosis
- Do not invent NGO details

End naturally.
"""
# -----------------
# Page Config
# -----------------

st.set_page_config(
    page_title="VARDAN AI",
    page_icon="🫀",
    layout="wide"
)

# -----------------
# Session Storage
# -----------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# -----------------
# Sidebar
# -----------------

with st.sidebar:

    # Logo center
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image(
            "logo.jpg",
            width=120
        )

    # Title
    st.markdown(
        """
        <h2 style='text-align:center;'>
        VARDAN AI
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center;color:gray;'>
        Donate Life NGO<br>
        Surat, Gujarat
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # WEBSITE SECTION
    st.markdown("### 🌐 Connect")

    st.link_button(
        "Visit Website",
        "https://www.donatelife.org.in/",
        use_container_width=True
    )

    st.divider()

    # SMALL QUOTE
    st.caption(
        "🫀 One organ donor can save multiple lives."
    )

    st.divider()

    # NEW CHAT
    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.current_chat = (
            "New Chat"
        )

        st.session_state.messages = []

        st.rerun()

    st.markdown(
        "### 💬 History"
    )

    # SHOW CHATS
    for chat in reversed(
        list(
            st.session_state.all_chats.keys()
        )
    ):

        if st.button(
            chat,
            key=chat,
            use_container_width=True
        ):

            st.session_state.current_chat = (
                chat
            )

            st.session_state.messages = (
                st.session_state.all_chats[
                    chat
                ]
            )

            st.rerun()
# -----------------
# Main Page
# -----------------

st.title("🫀 VARDAN AI")

st.caption(
    "Donate Life AI Assistant"
)

# -----------------
# Show Chat
# -----------------

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):
        st.write(
            msg["content"]
        )

# -----------------
# User Input
# -----------------

prompt = st.chat_input(
    "Ask about organ donation..."
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Set title only for first message
    if (
        st.session_state.current_chat
        == "New Chat"
    ):

        chat_title = (
            prompt.strip()
        )

        if len(chat_title) > 40:

            chat_title = (
                chat_title[:40]
                + "..."
            )

        st.session_state.current_chat = (
            chat_title
        )

    # Show user message
    with st.chat_message(
        "user"
    ):
        st.write(prompt)

    # Build conversation text
    history = "\n".join(
        [
            f'{m["role"]}: {m["content"]}'
            for m in (
                st.session_state.messages[-6:]
            )
        ]
    )

    final_prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{history}

Assistant:
"""

    try:

        response = (
            client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )
        )

        answer = (
            response.text
        )

    except Exception as e:

        answer = (
            f"Error: {e}"
        )

    # Show assistant answer
    with st.chat_message(
        "assistant"
    ):
        st.write(answer)

    # Save assistant answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save chat
    st.session_state.all_chats[
        st.session_state.current_chat
    ] = (
        st.session_state.messages.copy()
    )

    st.rerun()
