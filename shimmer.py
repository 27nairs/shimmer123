import streamlit as st
import datetime

import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shimmer Salon Concierge", page_icon="✨", layout="centered")
# Initialize Groq Client safely using Streamlit secrets
api_key = st.secrets["MY_KEY"]
client = Groq(api_key=api_key)
# --- CUSTOM STYLING (Optional) ---
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: bold; color: #FF69B4; text-align: center; }
    .subtitle { font-size: 20px; text-align: center; color: #555; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-title">✨ Shimmer Salon ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Digital Luxury Concierge</div>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR / NAVIGATION ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Book an Appointment", "Services Menu", "FAQs & Consultation"])

# --- DATA ---
services = {
    "Haircut & Styling": 65,
    "Full Highlights": 150,
    "Balayage": 180,
    "Hydrating Hair Facial": 45,
    "Gel Manicure": 40,
    "Luxury Pedicure": 55
}
stylists = ["Alex (Master Stylist)", "Jordan (Color Specialist)", "Taylor (Nail Artist)", "No Preference"]

# --- PAGE 1: BOOK AN APPOINTMENT ---
if page == "Book an Appointment":
    st.header("📅 Schedule Your Shimmer Experience")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
        with col2:
            phone = st.text_input("Phone Number")
            stylist = st.selectbox("Choose a Stylist/Artist", stylists)
            
        selected_services = st.multiselect("Select Services", list(services.keys()))
        
        col3, col4 = st.columns(2)
        with col3:
            date = st.date_input("Preferred Date", min_value=datetime.date.today())
        with col4:
            time = st.time_input("Preferred Time")
            
        notes = st.text_area("Special Notes or Requests (e.g., allergies, hair length)")
        
        # Calculate dynamic total price
        total_price = sum([services[s] for s in selected_services])
        if total_price > 0:
            st.info(f"**Estimated Total:** ${total_price}")
            
        submit = st.form_submit_button("Request Booking")
        
    if submit:
        if name and email and selected_services:
            st.success(f"Thank you, {name}! Your request for {', '.join(selected_services)} on {date} at {time} has been sent to Shimmer Salon. We will confirm via email shortly.")
        else:
            st.error("Please fill out your Name, Email, and select at least one service.")

# --- PAGE 2: SERVICES MENU ---
elif page == "Services Menu":
    st.header("💇‍♀️ Our Shimmer Services Menu")
    st.write("We use premium, eco-friendly products to give you the ultimate glow.")
    
    # Display services in a clean table format
    st.table([{"Service": k, "Starting Price": f"${v}"} for k, v in services.items()])

# --- PAGE 3: FAQs & CONSULTATION ---
elif page == "FAQs & Consultation":
    st.header("🤖 Virtual Consultation & FAQs")
    
    st.subheader("Not sure what to get?")
    hair_goal = st.selectbox("What is your primary hair or nail goal?", [
        "Select an option...",
        "I want a complete color transformation",
        "My hair feels dry and damaged",
        "I just need a clean trim and style",
        "I want long-lasting nail color"
    ])
    
    if hair_goal == "I want a complete color transformation":
        st.success("✨ **Concierge Recommends:** Book a **Balayage** or **Full Highlights** with Jordan!")
    elif hair_goal == "My hair feels dry and damaged":
        st.success("✨ **Concierge Recommends:** Try our **Hydrating Hair Facial** paired with a fresh trim.")
    elif hair_goal == "I just need a clean trim and style":
        st.success("✨ **Concierge Recommends:** Book a **Haircut & Styling** with Alex.")
    elif hair_goal == "I want long-lasting nail color":
        st.success("✨ **Concierge Recommends:** Try our **Gel Manicure** with Taylor.")

    st.divider()
    st.subheader("Frequently Asked Questions")
    with st.expander("What is your cancellation policy?"):
        st.write("We require 24 hours notice for all cancellations. Late cancellations may incur a 50% fee.")
    with st.expander("Do you accept walk-ins?"):
        st.write("While we love seeing you, we highly recommend booking in advance to ensure a stylist is available for your desired time!")