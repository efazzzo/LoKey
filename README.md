# 🔑 LoKey

**Vibe-first local discovery for Culpeper, VA**

LoKey surfaces culturally rich, overlooked businesses that traditional platforms ignore. Instead of star ratings and ad spend, we use mood filters, energy levels, and authentic founder-written context.

## What Makes LoKey Different

- **Vibe-based discovery**: Chill, Hype, Creative, Social vibes instead of generic categories
- **Energy filters**: Day/night energy, family/social scene metrics
- **"When it shines"**: Context for when each spot is at its best
- **Founder voice**: Curated descriptions based on local feedback and personal experience
- **Cultural over transactional**: We highlight soul, not volume

## Features

- 🎯 **Discover**: Filter by vibe, energy, scene, and neighborhood
- ➕ **Submit venues**: Community-driven submissions
- 🗺️ **Map view**: Visual discovery with vibe-coded markers
- ✍️ **Founder notes**: Authentic, opinionated context
- 💾 **Persistent database**: JSON-based storage

## Tech Stack

- **Framework**: Streamlit
- **Maps**: Folium
- **Database**: JSON (simple, portable, version-controllable)
- **Deployment**: [Coming soon]

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Database Structure

Venues are stored in `lokey_venues.json` with the following schema:

```json
{
  "id": 1,
  "name": "Venue Name",
  "location": "Neighborhood",
  "primary_vibe": "Chill|Hype|Creative|Social|Family",
  "day_energy": 1-10,
  "night_energy": 1-10,
  "family_friendly": 1-10,
  "social_scene": 1-10,
  "description": "What's the vibe?",
  "when_it_shines": "Context for peak experiences",
  "founder_notes": "Opinionated take",
  "verified": true|false
}
```

## Roadmap

- [ ] QR code generation for frictionless scanning
- [ ] Social referral tracking
- [ ] User accounts and saved spots
- [ ] Local events calendar
- [ ] Seasonal vibe updates
- [ ] Mobile app

## Philosophy

LoKey is culturally oriented, not transaction-focused. We're building an intelligence layer that captures overlooked demand patterns, vibe mismatches, and what makes small businesses special.

**Starting hyperlocal in Culpeper. Scaling the ethos, not just the tech.**

---

Built with AI tools, founder intuition, and local love.
