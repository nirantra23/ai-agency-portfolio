import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.set_page_config(page_title="🦷 SmileCare Dental Chatbot",)
st.title("🦷 SmileCare Dental Chatbot")  
st.caption("Available 24/7 to answer your dental questions.")

SYSTEM_PROMPT = """Your are a friendly assistant for SmileCare Dental Clinic,


SERVICES & PRICES:
- Regular Checkup: $50
- Teeth Cleaning: $80
- Cavity Filling: $150
- Root Canal: $500
- Teeth Whitening: $200
- Consultation: $30
HOURS:
- Monday to Saturday: 8am - 7pm, Sunday closed
PHONE: (555) 123-4567
ADDRESS: 123 Smile St, Happy Town, USA
BOOKING: Call or Whatsapp us anytime.

RULES: Only answer dental related questions,
If unsure, say "Let me check with our dental experts and get back to you!
Keep answers under 3 sentences and be warm."""


if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Ask me anything about dental care or our clinic!"): 
    st.session_state.messages.append({"role": "user", "content": prompt })
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner(""):
            r= client.chat.completion.create(
            model=""llama-3.3-70b-versatile"",
            messages=[{"role":"system","content": SYSTEM_PROMPT}
                     + st.session_state.message],
            )
            reply = r.choices[0].message.content
            st.write(reply)
    st.session_state.messages.append({"role":"assistant","content": reply})