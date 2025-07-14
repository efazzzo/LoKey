import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# App title
st.title("LoKey City")

# Navigation menu
page = st.sidebar.radio("Go to", ["Discover", "Submit a Venue", "My LoKey"])

# ------------------------------
# Sample data with location + coordinates
# ------------------------------
venue_data = [
    {"name": "Slate Charlotte", "mood": "Hype", "game_on": True, "location": "South End",
     "description": "Trendy rooftop bar with sports screens.", "lat": 35.2159, "lon": -80.8601},
    {"name": "Prohibition", "mood": "Chill", "game_on": False, "location": "Uptown",
     "description": "Relaxed pub with live music on weekends.", "lat": 35.2271, "lon": -80.8431},
    {"name": "Queen Park Social", "mood": "Social", "game_on": True, "location": "LoSo",
     "description": "Games, drinks, and UFC nights.", "lat": 35.1903, "lon": -80.8736},
    {"name": "The Degenerate", "mood": "Creative", "game_on": False, "location": "NoDa",
     "description": "Graffiti art, DJs, and cocktails.", "lat": 35.2471, "lon": -80.8042},
    {"name": "Hoppin’", "mood": "Hype", "game_on": True, "location": "South End",
     "description": "Lively beer wall with game day specials.", "lat": 35.2145, "lon": -80.8606},
    {"name": "The Wine Loft", "mood": "Chill", "game_on": False, "location": "Myers Park",
     "description": "Lowkey wine bar perfect for a date night.", "lat": 35.1954, "lon": -80.8310}
]

# Initialize session state
if "venue_submissions" not in st.session_state:
    st.session_state.venue_submissions = []

# Combine static + user-submitted venues
full_venue_list = venue_data + st.session_state.venue_submissions
df = pd.DataFrame(full_venue_list)

# ------------------------------
# Discover Page
# ------------------------------
if page == "Discover":
    st.header("Find Your Vibe 🎯")
    moods = df['mood'].unique().tolist()
    locations = df['location'].unique().tolist()

    selected_mood = st.radio("Choose your vibe:", moods)
    selected_location = st.selectbox("Pick a neighborhood:", ["All"] + locations)
    game_filter = st.checkbox("Only show places with the game on 🎮")

    # Filter by mood
    filtered_df = df[df['mood'] == selected_mood]

    # Filter by location
    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['location'] == selected_location]

    # Filter by game toggle
    if game_filter:
        filtered_df = filtered_df[filtered_df['game_on'] == True]

    st.subheader(f"LoKey Picks for a {selected_mood} night in {selected_location}:")

    for _, row in filtered_df.iterrows():
        st.markdown(f"### {row['name']}")
        st.write(f"📍 {row['location']}")
        st.write(row['description'])
        if row['game_on']:
            st.success("🎯 Showing the game tonight!")
        else:
            st.info("This spot is vibe-only tonight.")
        st.markdown("---")

    # Map View
    if not filtered_df.empty:
        st.subheader("Map View 🗺️")
        map_center = [filtered_df['lat'].mean(), filtered_df['lon'].mean()]
        m = folium.Map(location=map_center, zoom_start=13)
        for _, row in filtered_df.iterrows():
            popup_text = f"{row['name']}<br>{row['description']}<br>{'🎯 Game On' if row['game_on'] else 'No Game'}"
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=popup_text,
                tooltip=row['name'],
                icon=folium.Icon(color="blue" if row['game_on'] else "gray")
            ).add_to(m)
        st_folium(m, width=700, height=500)

# ------------------------------
# Submit a Venue Page
# ------------------------------
elif page == "Submit a Venue":
    st.header("LoKey Bar Portal 🍸")
    with st.form("venue_form"):
        name = st.text_input("Venue Name")
        description = st.text_area("Short Description (What’s the vibe?)")
        mood = st.selectbox("Primary Vibe Category", ["Chill", "Hype", "Creative", "Social"])
        location = st.selectbox("Neighborhood", ["South End", "Uptown", "LoSo", "NoDa", "Myers Park"])
        game_on = st.checkbox("Will you be showing a major game/fight tonight?")
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        submitted = st.form_submit_button("Submit Venue")

    if submitted:
        new_venue = {
            "name": name,
            "description": description,
            "mood": mood,
            "location": location,
            "game_on": game_on,
            "lat": lat,
            "lon": lon
        }
        st.session_state.venue_submissions.append(new_venue)
        st.success(f"✅ {name} has been submitted to LoKey City!")

# ------------------------------
# My LoKey Page
# ------------------------------
elif page == "My LoKey":
    st.header("My LoKey (Coming Soon 🚧)")
    st.info("This is where your saved spots, past vibes, and local calendar will live.")
