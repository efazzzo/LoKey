# LoKey - Culpeper

A mobile-first local discovery platform that uses vibe/mood filters instead of star ratings to help people find places worth knowing about in Culpeper, VA.

## What Makes LoKey Different

Traditional platforms (Google, Yelp) show generic categories and ratings but fail to communicate what a place actually feels like, who it's for, and when it shines. LoKey fixes this with:

- **Vibe-based filtering** - Find places by mood/energy instead of categories
- **Rich contextual descriptions** - Know what a place feels like, who it's for, when it shines
- **Mobile-first design** - Fast, clean interface optimized for QR code scanning
- **Anti-algorithm approach** - Culturally oriented, human-curated discovery

## Features

- ✅ Vibe-based place filtering (mood, activity, time, crowd)
- ✅ Rich place detail pages with contextual descriptions
- ✅ Mobile-optimized, responsive design
- ✅ Shareable links and QR code generation
- ✅ Admin interface for managing places
- ✅ Clean, minimal UI (anti-Yelp)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

The app will be available at `http://localhost:5000`

### 3. Seed Sample Data

Visit `http://localhost:5000/admin` and click "Load Sample Places" to populate the database with 8 curated Culpeper venues.

## Project Structure

```
LoKey/
├── app.py                 # Flask backend with API routes
├── database.py            # Database schema and queries
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main discovery page
│   ├── place.html        # Place detail page
│   └── admin.html        # Admin interface
└── static/
    ├── css/
    │   └── style.css     # Mobile-first styles
    └── js/
        └── discover.js    # Discovery page logic
```

## Usage

### For Users (Discovery)

1. **Browse places** - Visit the homepage to see all places
2. **Filter by vibe** - Select vibe tags to find places that match your mood
3. **View details** - Click any place to see rich contextual information
4. **Share** - Use the share button or QR code to share places

### For Admins (Content Management)

1. Visit `/admin`
2. **Add new places** with:
   - Basic info (name, description)
   - Contextual descriptions (what it feels like, who it's for, when it shines)
   - Vibe tags (mood, activity, time, crowd)
   - Contact info (address, phone, website, Instagram)
3. **Seed sample data** to get started quickly

## Vibe Tag Categories

### Mood
- quiet-focus, social-buzz, date-night, creative-energy, chill-hangout, high-energy, local-authentic

### Activity
- coffee-culture, craft-drinks, live-music, outdoor-space, food-focused, game-day

### Time
- early-bird, lunch-spot, happy-hour, late-night, weekend-brunch

### Crowd
- family-friendly, solo-friendly, group-spot, regulars-bar

## API Endpoints

- `GET /api/places` - Get all places (optional: `?vibes=tag1,tag2`)
- `GET /api/place/<id>` - Get single place by ID
- `GET /api/vibes` - Get all vibe tags grouped by category
- `POST /api/admin/place` - Add new place (admin)
- `POST /api/admin/seed` - Seed sample data (admin)
- `GET /api/qr/<id>` - Generate QR code for place

## Deployment

### Production Checklist

1. Set `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up proper authentication for `/admin`
4. Configure HTTPS
5. Set up proper database backups

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Customization

### Adding Your Own Places

1. Visit `/admin`
2. Fill out the form with rich, contextual descriptions
3. Select appropriate vibe tags
4. Submit

### Modifying Vibe Tags

Edit the `seed_vibe_tags()` method in `database.py` to add/remove/modify vibe tags.

## Philosophy

LoKey is built on the belief that discovery should be:

- **Contextual** - Know what a place feels like, not just what it serves
- **Human** - Curated descriptions over algorithmic recommendations
- **Accessible** - Mobile-first, fast, frictionless
- **Local** - Focused on real community connection

Traditional platforms optimize for scale. LoKey optimizes for truth.

## Future Features (Not in MVP)

- Event overlay system (temporal markers on static discovery)
- User accounts and saved places
- Community contributions
- Multi-city expansion
- Native mobile apps

## License

MIT

## Built With

- Flask - Web framework
- SQLite - Database
- Vanilla JavaScript - Frontend interactivity
- QR Code - QR code generation
