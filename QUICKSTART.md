# LoKey Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install & Run

```bash
pip install -r requirements.txt
python app.py
```

Visit: `http://localhost:5000`

### 2. Load Sample Data

Two options:

**Option A: Via Web Interface**
- Go to `http://localhost:5000/admin`
- Click "Load Sample Places"
- Done! 10 Culpeper venues loaded

**Option B: Via Python**
```bash
python -c "from database import Database; db = Database(); db.seed_vibe_tags(); exec(open('app.py').read().split('sample_places = [')[1].split('for place_data in sample_places:')[0])"
```

### 3. Experience the Journey

Visit `http://localhost:5000/demo` to see the complete user journey explained, or jump straight to discovery at `http://localhost:5000`

---

## 📱 User Experience Flow

### Scenario 1: Friday Night Out

**User thinks:** "I want somewhere fun and social for my group of friends"

**User does:**
1. Opens LoKey on phone
2. Taps vibe tags: **Social Buzz**, **High Energy**, **Group Spot**
3. Instantly sees 3 matching places

**Results shown:**
- **Throwbacks Arcade Bar** - "Pure nostalgia with a grown-up twist. Blinking screens, 8-bit soundtracks..."
- **Far Gohn Brewing Company** - "Industrial-cool meets neighborhood hangout. Craft beer talk and laughter..."
- **Zandra's** - "Lively, unpretentious. Booths that have seen countless margarita nights..."

**User taps "Throwbacks"** → Sees full context:
- What it feels like: "The kind of place that makes you feel like a kid with better taste in drinks"
- Who it's for: "Gamers, groups looking for something different, date nights with a playful edge"
- When it shines: "Weekend nights, when you want fun over fancy"

**Decision made in 30 seconds.**

---

### Scenario 2: Saturday Morning Coffee

**User thinks:** "Need coffee and quiet to work on my laptop"

**User does:**
1. Selects: **Quiet Focus**, **Coffee Culture**, **Solo Friendly**
2. Sees 1 perfect match

**Result:**
- **Piedmont Coffee House** - "The living room Culpeper needed. Smells like fresh roasted beans, sounds like friendly chatter and laptop keyboards. Baristas who remember your order."

**User knows immediately:** This is the spot.

---

### Scenario 3: Date Night

**User thinks:** "Somewhere intimate for a date, good drinks, not too loud"

**User does:**
1. Selects: **Date Night**, **Craft Drinks**, **Chill Hangout**
2. Gets 2 options

**Results:**
- **Culpeper Cheese Company** - "Intimate, cultured, a little European. Small tables, good wine, cheese that makes you slow down..."
- **Flavor on Main** - "Elevated but not stuffy. You can taste the intention in every dish..."

**User picks one** → Shares link with date → Done.

---

## 🎯 What Makes This Different

### Traditional Search (Google/Yelp):
```
User searches: "bars near me"
Gets: 47 results, sorted by distance
Clicks: "Joe's Bar" → 4.2⭐ (183 reviews)
Reads: Generic reviews, "great place!", "meh"
Decision: Confused, picks randomly
```

### LoKey Discovery:
```
User selects: Social Buzz + High Energy
Gets: 3 places that match the vibe
Reads: "Pure nostalgia with grown-up twist..."
Decision: Clear, confident, immediate
```

---

## 📊 Real Places Loaded

When you seed the database, you get these 10 real Culpeper spots:

1. **Zandra's** - Mexican restaurant/bar, social buzz, game day energy
2. **Far Gohn Brewing** - Craft brewery, community hangout, dog-friendly
3. **Throwbacks Arcade Bar** - Retro gaming + cocktails, high energy, playful
4. **Piedmont Coffee House** - Coffee roaster, laptop-friendly, local hub
5. **Flavor on Main** - Farm-to-table, date nights, elevated dining
6. **Grass Rootes** - Live music venue, electric nights, community spot
7. **Baby Jim's** - Dive bar, late night, regulars-only vibe
8. **Foti's Restaurant** - Classic diner since 1956, breakfast tradition
9. **It's About Thyme** - Garden cafe, peaceful lunches, hidden gem
10. **Culpeper Cheese Company** - Wine bar, intimate, date-night perfect

Each has:
- Rich "what it feels like" description
- Clear "who it's for" context
- Specific "when it shines" timing
- 3-6 vibe tags
- Real address

---

## 🔍 Try These Vibe Combinations

**"I want to work on my laptop"**
- Quiet Focus + Coffee Culture + Solo Friendly
- → Piedmont Coffee House

**"Game day with the crew"**
- Social Buzz + Game Day + Group Spot
- → Zandra's

**"Fun night out, something different"**
- High Energy + Social Buzz + Creative Energy
- → Throwbacks Arcade Bar

**"Chill beer with friends"**
- Craft Drinks + Chill Hangout + Local Authentic
- → Far Gohn Brewing

**"Romantic date night"**
- Date Night + Craft Drinks
- → Culpeper Cheese Company or Flavor on Main

**"Weekend brunch with family"**
- Family Friendly + Weekend Brunch + Early Bird
- → Foti's Restaurant

---

## 📱 Mobile Experience

The entire UI is optimized for mobile:

1. **Fast loading** - No heavy frameworks, vanilla JS
2. **Tap-friendly** - Vibe tags are big, easy to tap
3. **Readable** - Large text, good contrast
4. **Shareable** - Native share API support
5. **QR ready** - Every place gets a QR code

**Perfect for:**
- QR codes on tables at venues
- Instagram story shares
- Text message recommendations
- Tourist discovery

---

## 🎨 Pages Available

- `/` - Main discovery (vibe filtering)
- `/demo` - User journey walkthrough
- `/place/{id}` - Place detail page
- `/admin` - Founder interface for managing places
- `/api/qr/{id}` - QR code for any place

---

## 💡 Philosophy in Action

**Traditional platforms answer:** "Where can I get Mexican food?"

**LoKey answers:** "What vibe am I looking for right now?"

The difference:
- Google shows you every Mexican restaurant
- LoKey shows you the one that matches your **current energy**

**That's the power of vibe-based discovery.**

---

## Next Steps

1. **Try it yourself**: `python app.py` → `http://localhost:5000/demo`
2. **Add your places**: Go to `/admin` and add real spots
3. **Share it**: Send the link to locals, get feedback
4. **Deploy it**: Put it online, print QR codes, spread the word

**Welcome to LoKey. Discovery that gets it.**
