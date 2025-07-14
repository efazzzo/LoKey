import streamlit as st
import pandas as pd

# Sample data: mock list of venues with mood tags and whether they show games
venue_data = [
    {"name": "Slate Charlotte", "mood": "Hype", "game_on": True, "description": "Trendy rooftop bar with sports screens."},
    {"name": "Prohibition", "mood": "Chill", "game_on": False, "description": "Relaxed pub with live music on weekends."},
    {"name": "Queen Park Social", "mood": "Social", "game_on": True, "description": "Games, drinks, and UFC nights."},
    {"name": "The Degenerate", "mood": "Creative", "game_on": False, "description": "Graffiti art, DJs, and cocktails."},
    {"name": "Hoppin’", "mood": "Hype", "game_on": True, "description": "Lively beer wall with game day specials."},
    {"name": "The Wine Loft", "mood": "Chill", "game_on": False, "description": "Lowkey wine bar perfect for a date night."}
]

# Convert to DataFrame for filtering
df = pd.DataFrame(venue_data)

# Streamlit UI
st.title("LoKey City: Discover the Vibe")
st.subheader("What kind of mood are you in?")

# Mood filter buttons
moods = df['mood'].unique().tolist()
selected_mood = st.radio("Choose your vibe:", moods)

# "Game On" toggle
game_filter = st.checkbox("Only show places with the game on 🎮")

# Filter based on selections
filtered_df = df[df['mood'] == selected_mood]
if game_filter:
    filtered_df = filtered_df[filtered_df['game_on'] == True]

# Display results
st.subheader(f"LoKey Picks for a {selected_mood} night:")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['name']}")
    st.write(row['description'])
    if row['game_on']:
        st.success("🎯 Showing the game tonight!")
    else:
        st.info("This spot is vibe-only tonight.")
