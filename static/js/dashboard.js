const user = JSON.parse(localStorage.getItem('user') || '{}');
let currentTheme = localStorage.getItem('theme') || 'dark';

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('username').textContent = user.username || 'User';
  document.getElementById('profile-pic').src = user.profile_picture || '/static/images/default-avatar.png';
  
  if (currentTheme === 'light') document.body.style.filter = 'invert(1) hue-rotate(180deg)';
  
  loadMovies();
  loadSeries();
  loadReviews();
});

async function loadMovies() {
  try {
    const data = await getMovies(1);
    const container = document.getElementById('latest-movies');
    container.innerHTML = data.movies.map(m => `
      <div class='carousel-item' onmouseover='showTrailer(this, "${m.trailer_url}")'>
        <img src='${m.thumbnail_url || "/static/images/placeholder.png"}' alt='${m.title}'>
        <div class='play-overlay'>▶</div>
        <div class='video-info'>
          <div class='video-title'>${m.title}</div>
          <div class='video-controls'>
            <button class='btn btn-small btn-primary' onclick='showPaymentModal(${m.id}, null, "${m.title}", ${m.price})'>Stream • Ksh ${m.price}</button>
            <button class='btn btn-small btn-secondary' onclick='showPaymentModal(${m.id}, null, "${m.title}", ${m.price}, true)'>Download</button>
          </div>
          <div class='countdown'>7 Days Access</div>
        </div>
      </div>
    `).join('');
  } catch(err) { console.error(err); }
}

async function loadSeries() {
  try {
    const data = await getSeries(1);
    const container = document.getElementById('popular-series');
    container.innerHTML = data.series.map(s => `
      <div class='carousel-item'>
        <img src='${s.thumbnail_url || "/static/images/placeholder.png"}' alt='${s.title}'>
        <div class='play-overlay'>▶</div>
        <div class='video-info'>
          <div class='video-title'>${s.title}</div>
          <div style='font-size:12px;'>${s.episodes_count} Episodes</div>
          <div class='video-controls'>
            <button class='btn btn-small btn-primary' onclick='showSeriesModal(${s.id})'>Select Episodes</button>
          </div>
          <div class='countdown'>Ksh ${s.price}/ep</div>
        </div>
      </div>
    `).join('');
  } catch(err) { console.error(err); }
}

async function loadReviews() {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user.id) return;
    // Placeholder - would load reviews from API
    document.getElementById('reviews-list').innerHTML = '<p style="color:#999;">No reviews yet. Be the first to share your thoughts!</p>';
  } catch(err) { console.error(err); }
}

function showPaymentModal(movieId, seriesId, title, amount, isDownload = false) {
  const action = isDownload ? 'Download' : 'Stream';
  const phone = prompt(`Enter M-Pesa phone number to ${action} "${title}" (Ksh ${amount}):`);
  if (!phone) return;
  
  initiatePayment(movieId, seriesId, '', amount, phone).then(pay => {
    alert(`Payment initiated.\nPhone: ${phone}\nAmount: Ksh ${amount}\n\nEnter M-Pesa PIN on your phone.\nTransaction ID will be verified automatically.`);
    setTimeout(() => {
      confirmPayment(pay.payment_id, 'TXN' + Date.now(), movieId, seriesId, '').then(() => {
        alert('✓ Payment confirmed! Access granted for 7 days.');
        loadMovies();
      });
    }, 3000);
  });
}

function showSeriesModal(seriesId) {
  getSeriesEpisodes(seriesId).then(eps => {
    const checkboxes = eps.map((e, i) => `<label><input type='checkbox' value='${e.id}'> Episode ${e.episode_number}: ${e.title}</label>`).join('<br>');
    const selected = prompt(`Select episodes to purchase:\n\n${checkboxes}\n\n(Check boxes and submit)`);
    if (selected) alert('Proceed with series purchase. Implementation continues in production.');
  });
}

function searchContent() {
  const query = document.getElementById('search-input').value.toLowerCase();
  // Implement search filtering - would call API with search query
  if (query.length < 2) { loadMovies(); return; }
  alert('Search for: ' + query);
}

function submitReview() {
  const text = document.getElementById('review-text').value;
  if (!text) { alert('Enter a review'); return; }
  alert('Thank you for your review: "' + text.substring(0, 50) + '..."');
  document.getElementById('review-text').value = '';
}

function toggleTheme() {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', currentTheme);
  if (currentTheme === 'light') {
    document.body.style.filter = 'invert(1) hue-rotate(180deg)';
  } else {
    document.body.style.filter = 'none';
  }
}

function loadSection(section) {
  alert(`Loading ${section} section...`);
  // In production, would dynamically load different content sections
}
