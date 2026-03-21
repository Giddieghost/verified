const user = JSON.parse(localStorage.getItem('user') || '{}');
let currentTheme = localStorage.getItem('theme') || 'dark';
let currentPaymentData = null;

document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('token')) {
        window.location.href = '/frontend/user/login.html';
        return;
    }
    
    document.getElementById('username').textContent = user.username || 'User';
    document.getElementById('profile-pic').src = user.profile_picture || '/static/images/default-avatar.png';
    
    if (localStorage.getItem('theme') === 'light') {
        document.body.style.filter = 'invert(1) hue-rotate(180deg)';
        currentTheme = 'light';
    }
    
    loadMovies();
    loadSeries();
});

// Modal Helpers
function openModal(id) { document.getElementById(id).style.display = 'block'; }
function closeModal(id) { 
    document.getElementById(id).style.display = 'none'; 
    if (id === 'video-modal') {
        const player = document.getElementById('main-player');
        player.pause();
        player.src = "";
    }
}

// Data Loading
async function loadMovies() {
    try {
        const data = await getMovies(1);
        const container = document.getElementById('latest-movies');
        container.innerHTML = data.movies.map(m => renderMovieItem(m)).join('');
    } catch(err) { console.error(err); }
}

async function loadSeries() {
    try {
        const data = await getSeries(1);
        const container = document.getElementById('popular-series');
        container.innerHTML = data.series.map(s => renderSeriesItem(s)).join('');
    } catch(err) { console.error(err); }
}

function renderMovieItem(m) {
    return `
        <div class="carousel-item" onclick="showMovieDetails(${m.id})">
            <img src="${m.thumbnail_url || '/static/images/placeholder.png'}" alt="${m.title}">
            <div class="play-overlay">▶</div>
            <div class="video-info">
                <div class="video-title">${m.title}</div>
                <div class="countdown">Ksh ${m.price}</div>
            </div>
        </div>
    `;
}

function renderSeriesItem(s) {
    return `
        <div class="carousel-item" onclick="showSeriesDetails(${s.id})">
            <img src="${s.thumbnail_url || '/static/images/placeholder.png'}" alt="${s.title}">
            <div class="play-overlay">▶</div>
            <div class="video-info">
                <div class="video-title">${s.title}</div>
                <div style="font-size:12px;">${s.episodes_count || 0} Episodes</div>
            </div>
        </div>
    `;
}

// Detail Views
async function showMovieDetails(id) {
    try {
        const movie = await getMovie(id);
        const body = document.getElementById('modal-body');
        body.innerHTML = `
            <div class="details-flex">
                <img src="${movie.thumbnail_url || '/static/images/placeholder.png'}" class="details-img">
                <div class="details-info">
                    <h2>${movie.title}</h2>
                    <div class="details-meta">
                        <span>${movie.duration} mins</span>
                        <span>${movie.category}</span>
                        <span>⭐ ${movie.rating || 'N/A'}</span>
                    </div>
                    <p>${movie.description}</p>
                    <div style="margin-top: 30px; display: flex; gap: 15px;">
                        <button class="btn btn-primary" onclick="initiateFlow('movie', ${movie.id}, '${movie.title}', ${movie.price})">Stream now for Ksh ${movie.price}</button>
                        <button class="btn btn-secondary" onclick="openVideoPlayer('${movie.trailer_url}')">Watch Trailer</button>
                    </div>
                </div>
            </div>
        `;
        openModal('movie-modal');
    } catch(err) { alert('Failed to load movie details'); }
}

// Payment Flow
function initiateFlow(type, id, title, amount) {
    currentPaymentData = { type, id, title, amount };
    document.getElementById('payment-target').textContent = title;
    document.getElementById('payment-amount').textContent = `Ksh ${amount}`;
    document.getElementById('payment-status').style.display = 'none';
    closeModal('movie-modal');
    openModal('payment-modal');
}

async function processPayment() {
    const phone = document.getElementById('phone-number').value;
    const statusDiv = document.getElementById('payment-status');
    
    if (!phone) {
        showStatus('Enter phone number', 'error');
        return;
    }

    try {
        showStatus('Initiating M-Pesa push...', 'success');
        const res = await initiatePayment(
            currentPaymentData.type === 'movie' ? currentPaymentData.id : null,
            currentPaymentData.type === 'series' ? currentPaymentData.id : null,
            '', 
            currentPaymentData.amount, 
            phone
        );

        showStatus('Please enter PIN on your phone...', 'success');
        
        // Start polling for status
        let attempts = 0;
        const interval = setInterval(async () => {
            attempts++;
            const statusRes = await apiFetch(`/payments/query/${res.payment_id}`);
            if (statusRes.status === 'completed') {
                clearInterval(interval);
                showStatus('✓ Payment Successful!', 'success');
                setTimeout(() => {
                    closeModal('payment-modal');
                    // In a real app, unlock content here
                    alert('Content unlocked! You can now stream.');
                }, 2000);
            } else if (statusRes.status === 'failed' || attempts > 20) {
                clearInterval(interval);
                showStatus('Payment failed or timed out', 'error');
            }
        }, 3000);

    } catch(err) {
        showStatus('Error: ' + err.message, 'error');
    }
}

function showStatus(msg, type) {
    const statusDiv = document.getElementById('payment-status');
    statusDiv.textContent = msg;
    statusDiv.style.display = 'block';
    statusDiv.className = `status-msg status-${type}`;
}

// Video Player
function openVideoPlayer(url) {
    if (!url) {
        alert('No video URL available');
        return;
    }
    const player = document.getElementById('main-player');
    player.src = url;
    openModal('video-modal');
}

// General UI
function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', currentTheme);
    document.body.style.filter = currentTheme === 'light' ? 'invert(1) hue-rotate(180deg)' : 'none';
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/frontend/user/login.html';
}

async function loadSection(section) {
    const area = document.getElementById('content-area');
    area.innerHTML = `<h2>${section.charAt(0).toUpperCase() + section.slice(1)}</h2><p>Loading ${section} content...</p>`;
    
    if (section === 'home') {
        window.location.reload(); // Simple way to reset
    } else if (section === 'movies') {
        const data = await getMovies(1);
        area.innerHTML = `
            <div class="section-title">All Movies</div>
            <div class="grid">${data.movies.map(m => renderMovieItem(m)).join('')}</div>
        `;
    }
    // Add other sections as needed
}
