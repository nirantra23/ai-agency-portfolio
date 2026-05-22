import streamlit as st
import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from current directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Page configuration
st.set_page_config(
    page_title="🦷 SmileCare Dental Chatbot",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        height: 550px;
        overflow-y: auto;
        margin-bottom: 20px;
    }
    
    .user-message-wrapper {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 15px;
        animation: slideIn 0.3s ease-in-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        font-size: 14px;
        line-height: 1.5;
    }
    
    .bot-message-wrapper {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 15px;
        animation: slideIn 0.3s ease-in-out;
    }
    
    .bot-message {
        background: #f0f0f0;
        color: #333;
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        font-size: 14px;
        line-height: 1.5;
    }
    
    .header {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .header h1 {
        margin: 0;
        color: #667eea;
        font-size: 2.5em;
    }
    
    .input-area {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client with proper error handling
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("❌ GROQ_API_KEY not found!")
        st.info("""
        **How to fix:**
        1. Create a `.env` file in the same folder as this script
        2. Add: `GROQ_API_KEY=your_actual_key_here`
        3. Save the file
        4. Restart the app
        """)
        st.stop()
    
    return Groq(api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "llama-3.3-70b-versatile"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

# SmileCare system prompt
SYSTEM_PROMPT = """You are a helpful assistant for a dental clinic called SmileCare. 
Answer questions about appointments, services, and dental health only. 
If asked anything else, politely say you can only help with dental questions.
SERVICES & PRICES:
- Consultation: $50
- Teeth Cleaning: $100–$150
- Whitening: $400–$600
- Filling: $75–$187
- Root Canal: $375–$750
- Braces (metal): $3,125–$5,000

HOURS: Mon–Sat 9am–7pm. Sunday closed.
PHONE: +91-XXXXXXXXXX
BOOKING: Call or WhatsApp us anytime.

RULES: Only answer dental questions. 
If unsure, say "Let me have our team call you."
Keep answers under 3 sentences. Be warm """

# Header
st.markdown("""
    <div class='header'>
        <h1>🦷 SmileCare Dental Chatbot</h1>
        <p style='color: #666; margin: 0; font-size: 1.1em;'>Welcome to SmileCare! How can we help you today?</p>
    </div>
""", unsafe_allow_html=True)

# Create columns
col1, col2 = st.columns([3, 1])

with col1:
    # Chat display
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    if len(st.session_state.messages) == 0:
        st.markdown("""
            <div style='text-align: center; color: #999; padding: 50px 20px;'>
                <h2>👋 Welcome to SmileCare!</h2>
                <p>Ask us about appointments, services, and dental health</p>
            </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class='user-message-wrapper'>
                    <div class='user-message'>{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='bot-message-wrapper'>
                    <div class='bot-message'>{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### ⚙️ Settings")
    
    st.session_state.model = st.selectbox(
        "AI Model:",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama2-70b-4096"],
        index=0
    )
    
    st.session_state.temperature = st.slider(
        "Response Style:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="0 = Factual, 1 = Creative"
    )
    
    st.metric("Messages", len(st.session_state.messages))
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()

# Input area
st.markdown("<div class='input-area'>", unsafe_allow_html=True)
user_input = st.chat_input("Ask us about dental services, appointments, or health...", key="user_input")
st.markdown("</div>", unsafe_allow_html=True)

# Handle user input
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    try:
        client = init_groq_client()
        
        messages_with_system = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + st.session_state.messages
        
        with st.spinner("🤖 Thinking..."):
            response = client.chat.completions.create(
                model=st.session_state.model,
                messages=messages_with_system,
                temperature=st.session_state.temperature,
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            
            assistant_message = response.choices[0].message.content
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure your GROQ_API_KEY is valid and properly set in the .env file")

# Sidebar information
with st.sidebar:
    st.markdown("### 🏥 SmileCare Info")
    st.write("""
    **SmileCare Dental Clinic**
    
    We provide:
    - Regular checkups
    - Teeth cleaning
    - Dental treatments
    - Emergency services
    """)
    
    st.markdown("---")
    st.markdown("### 📋 System Prompt")
    st.info(SYSTEM_PROMPT)
    
    st.markdown("---")
    st.markdown("### ℹ️ About This Bot")
    st.caption("Powered by Groq API with Llama 3.3 70B model")