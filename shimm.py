import streamlit as st
from groq import Groq
import os
from groq import Groq
from dotenv import load_dotenv

# 1. Page Configuration & Styling
load_dotenv()
st.set_page_config(page_title="Shimmer Day & Spa Bot", page_icon="✨", layout="centered")

st.title("✨ Shimmer Day & Spa")
st.subheader("Virtual Assistant")
st.write("Welcome to Shimmer Day & Spa! Ask me about our services, pricing, or operating hours.")

# 2. Initialize Groq Client
# Make sure to set your GROQ_API_KEY environment variable, 
# or paste it safely here (though environment variables are best practice!)
api_key = st.secrets.get("GROQ_API_KEY") or "api"
client = Groq(api_key=api_key)

# 3. Define the Spa's Identity (System Prompt)
SPA_CONTEXT = """
You are "Shimmer," the friendly, luxurious, and helpful virtual receptionist for Shimmer Day & Spa. 
Your goal is to assist clients with information about services, operating hours, and general booking inquiries.

Here is the key information about Shimmer Day & Spa:
- Hours: Monday - Saturday: 9:00 AM - 7:00 PM | Sunday: 10:00 AM - 5:00 PM.
- Popular Services & Pricing:
  * Signature Facial (60 mins) - $95
  * Deep Tissue Massage (60 mins / 90 mins) - $110 / $150
  * Hot Stone Therapy (75 mins) - $130
  * Shimmer Luxury Pedicure & Manicure Combo - $75
  * Detox Body Wrap (60 mins) - $105
- Booking Policy: Walk-ins are welcome if space permits, but reservations are highly recommended. 
- Cancellations: Must be made at least 24 hours in advance to avoid a 50% fee.

Be polite, elegant, welcoming, and concise. Always offer to help them pick a treatment. If they ask to book an actual appointment, gather their preferred service/day and tell them you will hand it off to a human coordinator to finalize.
"""

# 4. Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SPA_CONTEXT},
        {"role": "assistant", "content": "Hello! Welcome to Shimmer Day & Spa. ✨ How can I pamper you today?"}
    ]

# 5. Display existing conversation history (skipping the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Handle User Input
if user_input := st.chat_input("Type your question here (e.g., 'What are your hours?' or 'Tell me about facials')"):
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from Groq API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # We use llama3-8b-8192 for fast, efficient text generation
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                temperature=0.6,
                max_tokens=500,
                stream=True,  # Enable streaming for that cool typewriter effect
            )
            
            # Stream the response chunk by chunk
            for chunk in completion:
                chunk_text = chunk.choices[0].delta.content or ""
                full_response += chunk_text
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"I'm sorry, I encountered a slight error. Please try again! (Error: {str(e)})"
            message_placeholder.markdown(full_response)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})