from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from database import Database
import qrcode
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)
db = Database()

# Initialize database with vibe tags on first run
if not os.path.exists('lokey.db'):
    db.seed_vibe_tags()

# ==================== WEB ROUTES ====================

@app.route('/')
def index():
    """Main discovery page"""
    return render_template('index.html')

@app.route('/place/<int:place_id>')
def place_detail(place_id):
    """Place detail page"""
    return render_template('place.html', place_id=place_id)

@app.route('/admin')
def admin():
    """Admin interface for managing places"""
    return render_template('admin.html')

# ==================== API ROUTES ====================

@app.route('/api/places')
def api_get_places():
    """Get all places or filter by vibes"""
    vibe_filter = request.args.get('vibes', '')

    if vibe_filter:
        vibe_names = [v.strip() for v in vibe_filter.split(',')]
        places = db.filter_places_by_vibes(vibe_names)
    else:
        places = db.get_all_places()

    return jsonify(places)

@app.route('/api/place/<int:place_id>')
def api_get_place(place_id):
    """Get a single place by ID"""
    place = db.get_place_by_id(place_id)
    if place:
        return jsonify(place)
    return jsonify({'error': 'Place not found'}), 404

@app.route('/api/vibes')
def api_get_vibes():
    """Get all vibe tags grouped by category"""
    vibes = db.get_all_vibe_tags()
    return jsonify(vibes)

@app.route('/api/admin/place', methods=['POST'])
def api_add_place():
    """Add a new place (admin)"""
    data = request.json

    place_id = db.add_place(
        name=data['name'],
        description=data.get('description', ''),
        what_it_feels_like=data.get('what_it_feels_like', ''),
        who_its_for=data.get('who_its_for', ''),
        when_it_shines=data.get('when_it_shines', ''),
        address=data.get('address'),
        phone=data.get('phone'),
        website=data.get('website'),
        instagram=data.get('instagram'),
        image_url=data.get('image_url')
    )

    # Add vibes
    if 'vibes' in data:
        for vibe in data['vibes']:
            db.add_vibe_to_place(place_id, vibe)

    # Add energy types
    if 'energy_types' in data:
        for energy_data in data['energy_types']:
            db.add_energy_type(
                place_id,
                energy_data['energy'],
                energy_data.get('time_of_day')
            )

    return jsonify({'success': True, 'place_id': place_id})

@app.route('/api/qr/<int:place_id>')
def api_generate_qr(place_id):
    """Generate QR code for a place"""
    place = db.get_place_by_id(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # Generate URL for the place
    base_url = request.host_url.rstrip('/')
    place_url = f"{base_url}/place/{place_id}"

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(place_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

# ==================== SEED DATA ====================

@app.route('/api/admin/seed', methods=['POST'])
def api_seed_data():
    """Seed database with sample Culpeper venues"""
    # Sample places for Culpeper, VA
    sample_places = [
        {
            'name': 'Flavor on Main',
            'description': 'Farm-to-table dining in historic downtown',
            'what_it_feels_like': 'Warm, welcoming, elevated but not stuffy. The kind of place where you can taste the intention in every dish.',
            'who_its_for': 'Foodies, date nights, anyone who appreciates thoughtful cooking and local ingredients',
            'when_it_shines': 'Dinner service, special occasions, when you want something memorable without the pretense',
            'address': '101 E Davis St, Culpeper, VA 22701',
            'vibes': ['date-night', 'food-focused', 'local-authentic'],
            'energy_types': [{'energy': 'low-key', 'time_of_day': 'evening'}]
        },
        {
            'name': 'Piedmont Coffee House',
            'description': 'Local coffee roaster and community hub',
            'what_it_feels_like': 'The living room Culpeper needed. Smells like fresh roasted beans, sounds like friendly chatter and laptop keyboards.',
            'who_its_for': 'Laptop workers, book readers, conversation havers, anyone who treats coffee like a ritual',
            'when_it_shines': 'Weekday mornings, weekend slow-downs, anytime you need to reset',
            'address': '201 E Davis St, Culpeper, VA 22701',
            'vibes': ['quiet-focus', 'coffee-culture', 'solo-friendly', 'local-authentic'],
            'energy_types': [
                {'energy': 'calm', 'time_of_day': 'morning'},
                {'energy': 'social', 'time_of_day': 'afternoon'}
            ]
        },
        {
            'name': 'Foti\'s Restaurant',
            'description': 'Classic American diner serving Culpeper since 1956',
            'what_it_feels_like': 'Time capsule comfort. Formica counters, regulars who know your order, the kind of place that makes you believe in breakfast again.',
            'who_its_for': 'Early risers, families, anyone who appreciates diners that have earned their place in town',
            'when_it_shines': 'Weekend brunch, weekday breakfast, when you want food that feels like home',
            'address': '219 E Davis St, Culpeper, VA 22701',
            'vibes': ['family-friendly', 'early-bird', 'weekend-brunch', 'local-authentic', 'regulars-bar'],
            'energy_types': [{'energy': 'bustling', 'time_of_day': 'morning'}]
        },
        {
            'name': 'Culpeper Cheese Company',
            'description': 'Wine bar and cheese shop',
            'what_it_feels_like': 'Intimate, cultured, a little European. Small tables, good wine, cheese that makes you slow down.',
            'who_its_for': 'Wine lovers, cheese enthusiasts, couples, small groups who like to linger',
            'when_it_shines': 'Happy hour, date nights, when conversation is the main course',
            'address': '107 E Davis St, Culpeper, VA 22701',
            'vibes': ['date-night', 'craft-drinks', 'chill-hangout', 'happy-hour'],
            'energy_types': [{'energy': 'intimate', 'time_of_day': 'evening'}]
        },
        {
            'name': 'Grass Rootes',
            'description': 'Live music venue and restaurant',
            'what_it_feels_like': 'Where Culpeper comes alive. Music that matters, crowd that listens, energy that reminds you why live shows exist.',
            'who_its_for': 'Music lovers, social butterflies, anyone who misses when venues felt like community',
            'when_it_shines': 'Show nights, weekends, when you want the night to feel like an event',
            'address': '309 S Main St, Culpeper, VA 22701',
            'vibes': ['live-music', 'high-energy', 'social-buzz', 'creative-energy', 'late-night'],
            'energy_types': [
                {'energy': 'electric', 'time_of_day': 'night'},
                {'energy': 'chill', 'time_of_day': 'afternoon'}
            ]
        },
        {
            'name': 'Culpeper Downtown Farmers Market',
            'description': 'Saturday morning market with local vendors',
            'what_it_feels_like': 'The whole town shows up. Fresh produce, homemade everything, the kind of Saturday ritual that makes you feel connected.',
            'who_its_for': 'Early risers, families, anyone who likes to know where their food comes from',
            'when_it_shines': 'Saturday mornings 7am-noon, especially peak summer season',
            'address': '133 W Davis St, Culpeper, VA 22701',
            'vibes': ['family-friendly', 'early-bird', 'local-authentic', 'outdoor-space', 'social-buzz'],
            'energy_types': [{'energy': 'vibrant', 'time_of_day': 'morning'}]
        },
        {
            'name': 'Baby Jim\'s',
            'description': 'Dive bar with character',
            'what_it_feels_like': 'No pretense, all personality. Cold beer, good people, the kind of place where stories happen.',
            'who_its_for': 'Night owls, pool players, anyone tired of bars that try too hard',
            'when_it_shines': 'Late nights, weekends, when you want real over polished',
            'address': '703 N Main St, Culpeper, VA 22701',
            'vibes': ['regulars-bar', 'late-night', 'chill-hangout', 'local-authentic'],
            'energy_types': [{'energy': 'laid-back', 'time_of_day': 'night'}]
        },
        {
            'name': 'It\'s About Thyme',
            'description': 'Garden cafe and culinary school',
            'what_it_feels_like': 'Hidden gem energy. Tucked away, garden seating, food that surprises you in the best way.',
            'who_its_for': 'Lunch seekers, garden lovers, people who appreciate places that feel like secrets',
            'when_it_shines': 'Lunch service, nice weather days, when you want to escape without leaving town',
            'address': '128 N Main St, Culpeper, VA 22701',
            'vibes': ['outdoor-space', 'lunch-spot', 'food-focused', 'quiet-focus', 'local-authentic'],
            'energy_types': [{'energy': 'peaceful', 'time_of_day': 'afternoon'}]
        }
    ]

    for place_data in sample_places:
        vibes = place_data.pop('vibes', [])
        energy_types = place_data.pop('energy_types', [])

        place_id = db.add_place(**place_data)

        for vibe in vibes:
            db.add_vibe_to_place(place_id, vibe)

        for energy_data in energy_types:
            db.add_energy_type(place_id, **energy_data)

    return jsonify({'success': True, 'message': f'Seeded {len(sample_places)} places'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
