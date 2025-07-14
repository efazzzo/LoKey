import streamlit as st
import pandas as pd

st.title("LoKey Bar Portal")
st.subheader("Submit Your Venue for LoKey City!")

# Form input for bar owners
with st.form("venue_form"):
    name = st.text_input("Venue Name")
    description = st.text_area("Short Description (What’s the vibe?)")
    mood = st.selectbox("Primary Vibe Category", ["Chill", "Hype", "Creative", "Social"])
    game_on = st.checkbox("Will you be showing a major game/fight tonight?")
    submitted = st.form_submit_button("Submit Venue")

# Save to local list (simulated for now)
if "venue_submissions" not in st.session_state:
    st.session_state.venue_submissions = []

if submitted:
    new_venue = {
        "name": name,
        "description": description,
        "mood": mood,
        "game_on": game_on
    }
    st.session_state.venue_submissions.append(new_venue)
    st.success(f"✅ {name} has been submitted to LoKey City!")

# Display submissions (for testing/demo)
if st.session_state.venue_submissions:
    st.subheader("Current Submissions:")
    for v in st.session_state.venue_submissions:
        st.markdown(f"### {v['name']}")
        st.write(v["description"])
        st.write(f"Vibe: {v['mood']}")
        st.write("🎯 Game On Tonight!" if v["game_on"] else "❌ No game tonight")
        st.markdown("---")

