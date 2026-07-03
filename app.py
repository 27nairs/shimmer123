import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secret key
load_dotenv()
# Paste your actual key between the quotes below:
api_key = st.secrets["MY_KEY"]
client = Groq(api_key=st.secrets["MY_KEY"])
st.title("Phoebe's Flowers 🌸")

# 2. Load the facts
try:
    with open("business_info.txt", "r") as f:
        content = f.read()
except:
    content = "Roses: $15, Lilies: $10"

# 3. Simple Chat Box
user_input = st.chat_input("Ask a question:")

# UPDATE THIS SECTION IN YOUR app.py
messages=[
    {
        "role": "system", 
        "content": f"""You are a helpful front-desk assistant for Phoebe's Flowers. 
        Your ONLY source of truth is the business info provided below. 
        
        FACTS:
        {content}
        
        INSTRUCTIONS:
        1. If a customer asks for contact info (phone, email, address), look in the FACTS and provide it clearly.
        2. If the info is NOT in the FACTS, say the exact words 'I'm sorry, I don't have that specific detail. Please visit us in person!'
        3. If the info not provided, say the exact words 'I'm sorry, I don't have that specific detail. Please visit us in person!'
        """
    },
    {"role": "user", "content": user_input}
]

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    # 4. Ask the AI
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"Use these facts: {content}"},
            {"role": "user", "content": user_input}
        ]
    )


    
    response = completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.write(response)