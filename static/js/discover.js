// State management
let allVibes = {};
let selectedVibes = new Set();
let allPlaces = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadVibes();
    await loadPlaces();
});

// Load vibe tags from API
async function loadVibes() {
    try {
        const response = await fetch('/api/vibes');
        allVibes = await response.json();
        renderVibeFilters();
    } catch (error) {
        console.error('Error loading vibes:', error);
        document.getElementById('vibe-filters').innerHTML = '<p class="text-muted">Error loading filters</p>';
    }
}

// Render vibe filter UI
function renderVibeFilters() {
    const container = document.getElementById('vibe-filters');
    container.innerHTML = '';

    // Order categories for better UX
    const categoryOrder = ['mood', 'activity', 'time', 'crowd'];
    const categoryLabels = {
        'mood': 'What\'s the vibe?',
        'activity': 'What are you into?',
        'time': 'When?',
        'crowd': 'Who\'s coming?'
    };

    categoryOrder.forEach(category => {
        if (!allVibes[category]) return;

        const section = document.createElement('div');
        section.className = 'vibe-section';

        const title = document.createElement('div');
        title.className = 'vibe-category-title';
        title.textContent = categoryLabels[category] || category;
        section.appendChild(title);

        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'vibe-tags';

        allVibes[category].forEach(vibe => {
            const tag = document.createElement('div');
            tag.className = 'vibe-tag';
            tag.textContent = formatVibeName(vibe.name);
            tag.title = vibe.description;
            tag.dataset.vibeName = vibe.name;

            tag.addEventListener('click', () => toggleVibe(vibe.name, tag));
            tagsContainer.appendChild(tag);
        });

        section.appendChild(tagsContainer);

        // Add clear button if this category has selected vibes
        if (hasSelectedVibesInCategory(category)) {
            const clearBtn = document.createElement('button');
            clearBtn.className = 'clear-filters';
            clearBtn.textContent = 'Clear';
            clearBtn.addEventListener('click', () => clearCategory(category));
            section.appendChild(clearBtn);
        }

        container.appendChild(section);
    });

    // Add global clear button if any vibes selected
    if (selectedVibes.size > 0) {
        const globalClear = document.createElement('button');
        globalClear.className = 'btn btn-secondary btn-block mt-2';
        globalClear.textContent = 'Clear all filters';
        globalClear.addEventListener('click', clearAllFilters);
        container.appendChild(globalClear);
    }
}

// Toggle vibe selection
function toggleVibe(vibeName, element) {
    if (selectedVibes.has(vibeName)) {
        selectedVibes.delete(vibeName);
        element.classList.remove('active');
    } else {
        selectedVibes.add(vibeName);
        element.classList.add('active');
    }
    filterPlaces();
}

// Clear category filters
function clearCategory(category) {
    allVibes[category].forEach(vibe => {
        selectedVibes.delete(vibe.name);
    });
    renderVibeFilters();
    filterPlaces();
}

// Clear all filters
function clearAllFilters() {
    selectedVibes.clear();
    renderVibeFilters();
    filterPlaces();
}

// Check if category has selected vibes
function hasSelectedVibesInCategory(category) {
    return allVibes[category].some(vibe => selectedVibes.has(vibe.name));
}

// Format vibe name for display
function formatVibeName(name) {
    return name.split('-').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// Load places from API
async function loadPlaces() {
    try {
        const response = await fetch('/api/places');
        allPlaces = await response.json();
        renderPlaces(allPlaces);
    } catch (error) {
        console.error('Error loading places:', error);
        document.getElementById('places-grid').innerHTML = '<p class="text-muted">Error loading places</p>';
    }
}

// Filter places based on selected vibes
function filterPlaces() {
    if (selectedVibes.size === 0) {
        renderPlaces(allPlaces);
        return;
    }

    const filtered = allPlaces.filter(place => {
        const placeVibeNames = place.vibes.map(v => v.name);
        // Place must have at least one of the selected vibes
        return Array.from(selectedVibes).some(vibe => placeVibeNames.includes(vibe));
    });

    renderPlaces(filtered);
}

// Render places grid
function renderPlaces(places) {
    const container = document.getElementById('places-grid');
    const resultsInfo = document.getElementById('results-info');
    const resultsCount = document.getElementById('results-count');

    if (places.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🤷</div>
                <p>No places match that vibe yet.<br>Try different filters or check back soon.</p>
            </div>
        `;
        resultsInfo.style.display = 'none';
        return;
    }

    // Show results count
    resultsInfo.style.display = 'block';
    resultsCount.textContent = `${places.length} ${places.length === 1 ? 'place' : 'places'} ${selectedVibes.size > 0 ? 'match your vibe' : 'in Culpeper'}`;

    container.innerHTML = places.map(place => createPlaceCard(place)).join('');
}

// Create place card HTML
function createPlaceCard(place) {
    const vibesHTML = place.vibes.slice(0, 4).map(vibe =>
        `<span class="place-vibe-tag">${formatVibeName(vibe.name)}</span>`
    ).join('');

    return `
        <a href="/place/${place.id}" class="place-card">
            <div class="place-name">${place.name}</div>
            <div class="place-description">${place.what_it_feels_like || place.description}</div>
            <div class="place-vibes">${vibesHTML}</div>
        </a>
    `;
}
