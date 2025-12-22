import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='lokey.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database with schema"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Places table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                what_it_feels_like TEXT,
                who_its_for TEXT,
                when_it_shines TEXT,
                address TEXT,
                phone TEXT,
                website TEXT,
                instagram TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Vibe tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vibe_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Place-vibe relationship table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS place_vibes (
                place_id INTEGER,
                vibe_id INTEGER,
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
                FOREIGN KEY (vibe_id) REFERENCES vibe_tags(id) ON DELETE CASCADE,
                PRIMARY KEY (place_id, vibe_id)
            )
        ''')

        # Energy types table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id INTEGER,
                energy TEXT NOT NULL,
                time_of_day TEXT,
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
            )
        ''')

        # Events table (optional overlay)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                event_date DATE,
                start_time TIME,
                end_time TIME,
                special_vibe TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def seed_vibe_tags(self):
        """Seed initial vibe tags"""
        conn = self.get_connection()
        cursor = conn.cursor()

        vibe_tags = [
            # Mood-based vibes
            ('quiet-focus', 'mood', 'Perfect for laptop work, reading, or deep conversation'),
            ('social-buzz', 'mood', 'Great for meeting people and lively conversation'),
            ('date-night', 'mood', 'Intimate, romantic atmosphere'),
            ('creative-energy', 'mood', 'Artistic vibe, inspiration flows'),
            ('chill-hangout', 'mood', 'Relaxed, no pressure, just vibes'),
            ('high-energy', 'mood', 'Loud, active, party atmosphere'),
            ('local-authentic', 'mood', 'Real Culpeper, no corporate feel'),

            # Activity-based vibes
            ('coffee-culture', 'activity', 'Quality coffee, cafe atmosphere'),
            ('craft-drinks', 'activity', 'Thoughtful cocktails or local beer'),
            ('live-music', 'activity', 'Regular performances, music scene'),
            ('outdoor-space', 'activity', 'Patio, garden, or outdoor seating'),
            ('food-focused', 'activity', 'The food is the main event'),
            ('game-day', 'activity', 'Sports on TV, game day energy'),

            # Time-based vibes
            ('early-bird', 'time', 'Morning coffee, breakfast crowd'),
            ('lunch-spot', 'time', 'Midday meal, quick or leisurely'),
            ('happy-hour', 'time', 'After work, wind down'),
            ('late-night', 'time', 'Night owl friendly, open late'),
            ('weekend-brunch', 'time', 'Weekend morning ritual'),

            # Crowd vibes
            ('family-friendly', 'crowd', 'Kids welcome, all ages'),
            ('solo-friendly', 'crowd', 'Great for going alone'),
            ('group-spot', 'crowd', 'Built for bigger groups'),
            ('regulars-bar', 'crowd', 'Neighborhood spot, familiar faces'),
        ]

        for tag_name, category, description in vibe_tags:
            cursor.execute('''
                INSERT OR IGNORE INTO vibe_tags (name, category, description)
                VALUES (?, ?, ?)
            ''', (tag_name, category, description))

        conn.commit()
        conn.close()

    def add_place(self, name, description, what_it_feels_like, who_its_for, when_it_shines,
                  address=None, phone=None, website=None, instagram=None, image_url=None):
        """Add a new place"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO places (name, description, what_it_feels_like, who_its_for,
                               when_it_shines, address, phone, website, instagram, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, what_it_feels_like, who_its_for, when_it_shines,
              address, phone, website, instagram, image_url))

        place_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return place_id

    def add_vibe_to_place(self, place_id, vibe_tag_name):
        """Add a vibe tag to a place"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get vibe_id from tag name
        cursor.execute('SELECT id FROM vibe_tags WHERE name = ?', (vibe_tag_name,))
        vibe = cursor.fetchone()

        if vibe:
            cursor.execute('''
                INSERT OR IGNORE INTO place_vibes (place_id, vibe_id)
                VALUES (?, ?)
            ''', (place_id, vibe['id']))
            conn.commit()

        conn.close()

    def add_energy_type(self, place_id, energy, time_of_day=None):
        """Add energy type to a place"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO energy_types (place_id, energy, time_of_day)
            VALUES (?, ?, ?)
        ''', (place_id, energy, time_of_day))

        conn.commit()
        conn.close()

    def get_all_places(self):
        """Get all places with their vibes"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM places ORDER BY name')
        places = [dict(row) for row in cursor.fetchall()]

        # Add vibes to each place
        for place in places:
            cursor.execute('''
                SELECT vt.name, vt.category, vt.description
                FROM vibe_tags vt
                JOIN place_vibes pv ON vt.id = pv.vibe_id
                WHERE pv.place_id = ?
            ''', (place['id'],))
            place['vibes'] = [dict(row) for row in cursor.fetchall()]

            # Add energy types
            cursor.execute('''
                SELECT energy, time_of_day FROM energy_types
                WHERE place_id = ?
            ''', (place['id'],))
            place['energy_types'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return places

    def get_place_by_id(self, place_id):
        """Get a single place by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM places WHERE id = ?', (place_id,))
        place_row = cursor.fetchone()

        if not place_row:
            conn.close()
            return None

        place = dict(place_row)

        # Add vibes
        cursor.execute('''
            SELECT vt.name, vt.category, vt.description
            FROM vibe_tags vt
            JOIN place_vibes pv ON vt.id = pv.vibe_id
            WHERE pv.place_id = ?
        ''', (place_id,))
        place['vibes'] = [dict(row) for row in cursor.fetchall()]

        # Add energy types
        cursor.execute('''
            SELECT energy, time_of_day FROM energy_types
            WHERE place_id = ?
        ''', (place_id,))
        place['energy_types'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return place

    def filter_places_by_vibes(self, vibe_names):
        """Filter places by vibe tags"""
        if not vibe_names:
            return self.get_all_places()

        conn = self.get_connection()
        cursor = conn.cursor()

        placeholders = ','.join('?' * len(vibe_names))
        query = f'''
            SELECT DISTINCT p.* FROM places p
            JOIN place_vibes pv ON p.id = pv.place_id
            JOIN vibe_tags vt ON pv.vibe_id = vt.id
            WHERE vt.name IN ({placeholders})
            ORDER BY p.name
        '''

        cursor.execute(query, vibe_names)
        places = [dict(row) for row in cursor.fetchall()]

        # Add vibes and energy to each place
        for place in places:
            cursor.execute('''
                SELECT vt.name, vt.category, vt.description
                FROM vibe_tags vt
                JOIN place_vibes pv ON vt.id = pv.vibe_id
                WHERE pv.place_id = ?
            ''', (place['id'],))
            place['vibes'] = [dict(row) for row in cursor.fetchall()]

            cursor.execute('''
                SELECT energy, time_of_day FROM energy_types
                WHERE place_id = ?
            ''', (place['id'],))
            place['energy_types'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return places

    def get_all_vibe_tags(self):
        """Get all vibe tags grouped by category"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM vibe_tags ORDER BY category, name')
        tags = [dict(row) for row in cursor.fetchall()]

        # Group by category
        grouped = {}
        for tag in tags:
            category = tag['category']
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(tag)

        conn.close()
        return grouped
