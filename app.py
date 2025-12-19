import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from pathlib import Path
from datetime import datetime

# Configure page
st.set_page_config(page_title="LoKey - Culpeper", page_icon="🔑", layout="wide")

# Database file path
DB_FILE = Path(__file__).parent / "lokey_venues.json"

# ------------------------------
# Database Functions
# ------------------------------
def load_venues():
    """Load venues from JSON database"""
    if DB_FILE.exists():
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            return data.get('venues', [])
    return []

def save_venues(venues):
    """Save venues to JSON database"""
    with open(DB_FILE, 'w') as f:
        json.dump({'venues': venues}, f, indent=2)

def add_venue(venue_data):
    """Add new venue to database"""
    venues = load_venues()
    # Generate new ID
    new_id = max([v.get('id', 0) for v in venues], default=0) + 1
    venue_data['id'] = new_id
    venue_data['verified'] = False
    venue_data['submitted_at'] = datetime.now().isoformat()
    venues.append(venue_data)
    save_venues(venues)
    return new_id

# ------------------------------
# App Header
# ------------------------------
st.title("🔑 LoKey")
st.caption("Culpeper's vibe-first discovery platform")

# Navigation
page = st.sidebar.radio("Navigate", ["🎯 Discover", "➕ Submit a Venue", "📍 My LoKey"])

# Load venues
venues = load_venues()
df = pd.DataFrame(venues) if venues else pd.DataFrame()

# ------------------------------
# DISCOVER PAGE
# ------------------------------
if page == "🎯 Discover":
    st.header("Find Your Vibe")

    if df.empty:
        st.warning("No venues yet. Be the first to submit one!")
    else:
        # Vibe filters in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🎨 Vibe")
            all_vibes = ["All"] + sorted(df['primary_vibe'].unique().tolist())
            selected_vibe = st.selectbox("Primary vibe:", all_vibes, key="vibe")

        with col2:
            st.subheader("⏰ Energy")
            energy_filter = st.radio(
                "When are you going?",
                ["Any time", "☀️ Day energy", "🌙 Night energy"],
                key="energy"
            )

        with col3:
            st.subheader("👥 Scene")
            scene_filter = st.radio(
                "Who are you with?",
                ["Anyone", "👨‍👩‍👧 Family-friendly", "🎉 Social scene"],
                key="scene"
            )

        # Additional filters
        col4, col5 = st.columns(2)
        with col4:
            location_filter = st.selectbox(
                "📍 Neighborhood",
                ["All"] + sorted(df['location'].unique().tolist()),
                key="location"
            )
        with col5:
            show_founder_notes = st.checkbox("✍️ Show founder notes", value=True)

        # Filter logic
        filtered_df = df.copy()

        # Vibe filter
        if selected_vibe != "All":
            filtered_df = filtered_df[filtered_df['primary_vibe'] == selected_vibe]

        # Energy filter (threshold: 7+)
        if energy_filter == "☀️ Day energy":
            filtered_df = filtered_df[filtered_df['day_energy'] >= 7]
        elif energy_filter == "🌙 Night energy":
            filtered_df = filtered_df[filtered_df['night_energy'] >= 7]

        # Scene filter (threshold: 8+)
        if scene_filter == "👨‍👩‍👧 Family-friendly":
            filtered_df = filtered_df[filtered_df['family_friendly'] >= 8]
        elif scene_filter == "🎉 Social scene":
            filtered_df = filtered_df[filtered_df['social_scene'] >= 8]

        # Location filter
        if location_filter != "All":
            filtered_df = filtered_df[filtered_df['location'] == location_filter]

        # Display results
        st.markdown("---")
        st.subheader(f"Found {len(filtered_df)} spots")

        if filtered_df.empty:
            st.info("No venues match these filters. Try adjusting your search.")
        else:
            # Venue cards
            for _, venue in filtered_df.iterrows():
                with st.container():
                    col_a, col_b = st.columns([3, 1])

                    with col_a:
                        # Verified badge
                        verified_badge = "✓ " if venue.get('verified', False) else ""
                        st.markdown(f"### {verified_badge}{venue['name']}")
                        st.caption(f"📍 {venue['location']} · 🎨 {venue['primary_vibe']}")

                        # Description
                        st.write(venue['description'])

                        # When it shines
                        if venue.get('when_it_shines'):
                            with st.expander("✨ When it shines"):
                                st.write(venue['when_it_shines'])

                        # Founder notes
                        if show_founder_notes and venue.get('founder_notes'):
                            with st.expander("✍️ Founder's take"):
                                st.info(venue['founder_notes'])

                    with col_b:
                        # Energy bars
                        st.metric("☀️ Day", f"{venue.get('day_energy', 0)}/10")
                        st.metric("🌙 Night", f"{venue.get('night_energy', 0)}/10")
                        st.metric("👨‍👩‍👧 Family", f"{venue.get('family_friendly', 0)}/10")
                        st.metric("🎉 Social", f"{venue.get('social_scene', 0)}/10")

                    st.markdown("---")

            # Map view
            if not filtered_df.empty and all(pd.notna(filtered_df[['lat', 'lon']].values.flatten())):
                st.subheader("🗺️ Map View")

                # Create map centered on Culpeper
                map_center = [38.4732, -77.9967]
                m = folium.Map(location=map_center, zoom_start=14)

                # Add markers
                vibe_colors = {
                    'Chill': 'blue',
                    'Hype': 'red',
                    'Creative': 'purple',
                    'Social': 'orange',
                    'Family': 'green'
                }

                for _, venue in filtered_df.iterrows():
                    if pd.notna(venue['lat']) and pd.notna(venue['lon']):
                        popup_html = f"""
                        <b>{venue['name']}</b><br>
                        {venue['location']}<br>
                        <i>{venue['primary_vibe']}</i><br>
                        {venue['description'][:100]}...
                        """

                        folium.Marker(
                            location=[venue['lat'], venue['lon']],
                            popup=folium.Popup(popup_html, max_width=300),
                            tooltip=venue['name'],
                            icon=folium.Icon(
                                color=vibe_colors.get(venue['primary_vibe'], 'gray'),
                                icon='info-sign'
                            )
                        ).add_to(m)

                st_folium(m, width=1000, height=500)

# ------------------------------
# SUBMIT A VENUE PAGE
# ------------------------------
elif page == "➕ Submit a Venue":
    st.header("Submit a Venue")
    st.write("Know a spot that deserves to be on LoKey? Tell us about it.")

    with st.form("venue_submission"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Venue name *", placeholder="The Hidden Gem")
            location = st.text_input("Neighborhood *", placeholder="Downtown Culpeper")
            address = st.text_input("Address", placeholder="123 Main St, Culpeper, VA")

            primary_vibe = st.selectbox(
                "Primary vibe *",
                ["Chill", "Hype", "Creative", "Social", "Family"]
            )

            description = st.text_area(
                "Description * (What's the vibe?)",
                placeholder="Cozy coffee shop with killer pastries and local art on the walls...",
                height=100
            )

        with col2:
            when_it_shines = st.text_area(
                "When does it shine?",
                placeholder="Sunday mornings, date nights, rainy afternoon writing sessions...",
                height=100
            )

            st.write("**Energy levels** (1-10)")
            day_energy = st.slider("☀️ Day energy", 1, 10, 5)
            night_energy = st.slider("🌙 Night energy", 1, 10, 5)
            family_friendly = st.slider("👨‍👩‍👧 Family-friendly", 1, 10, 5)
            social_scene = st.slider("🎉 Social scene", 1, 10, 5)

            # Optional coordinates
            with st.expander("📍 Location coordinates (optional)"):
                lat = st.number_input("Latitude", value=38.4732, format="%.6f")
                lon = st.number_input("Longitude", value=-77.9967, format="%.6f")

        submitted = st.form_submit_button("Submit Venue", type="primary")

        if submitted:
            if not name or not location or not description:
                st.error("Please fill in all required fields (*)")
            else:
                new_venue = {
                    'name': name,
                    'location': location,
                    'address': address,
                    'lat': lat,
                    'lon': lon,
                    'primary_vibe': primary_vibe,
                    'secondary_vibes': [],
                    'description': description,
                    'when_it_shines': when_it_shines,
                    'day_energy': day_energy,
                    'night_energy': night_energy,
                    'family_friendly': family_friendly,
                    'social_scene': social_scene,
                    'game_on': False,
                    'founder_notes': ''
                }

                venue_id = add_venue(new_venue)
                st.success(f"✅ {name} has been submitted! (ID: {venue_id})")
                st.info("Your submission will be reviewed and added to the map soon.")
                st.balloons()

# ------------------------------
# MY LOKEY PAGE
# ------------------------------
elif page == "📍 My LoKey":
    st.header("My LoKey")
    st.info("🚧 Coming soon: Your saved spots, past vibes, and local calendar.")

    # Placeholder for future features
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💾 Saved Spots")
        st.write("Bookmark your favorite venues")

    with col2:
        st.subheader("📅 Local Calendar")
        st.write("Events and special nights")

    with col3:
        st.subheader("🏆 Your Referrals")
        st.write("Track spots you've shared")

# ------------------------------
# Sidebar Info
# ------------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("### About LoKey")
    st.write("Vibe-first discovery for Culpeper's culturally rich, overlooked businesses.")
    st.caption(f"📊 {len(venues)} venues in the database")
    st.caption("Built with ❤️ for Culpeper")

    # Quick stats
    if not df.empty:
        st.markdown("---")
        st.markdown("### Quick Stats")
        verified_count = df['verified'].sum() if 'verified' in df.columns else 0
        st.metric("Verified venues", verified_count)
        st.metric("Top vibe", df['primary_vibe'].mode()[0] if not df.empty else "N/A")
