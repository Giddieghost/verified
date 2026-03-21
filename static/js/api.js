const API_BASE = '/api';
const token = localStorage.getItem('token');

async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers.Authorization = `Bearer ${token}`;
  
  const res = await fetch(API_BASE + path, { ...options, headers });
  if (res.status === 401) { logout(); return null; }
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

// Movies  
async function getMovies(page = 1) { return apiFetch(`/movies?page=${page}`); }
async function getMovie(id) { return apiFetch(`/movies/${id}`); }
async function getMovieReviews(id) { return apiFetch(`/movies/${id}/reviews`); }

// Series
async function getSeries(page = 1) { return apiFetch(`/series?page=${page}`); }
async function getSeriesEpisodes(id) { return apiFetch(`/series/${id}/episodes`); }

// Auth
async function login(email, password) { return apiFetch('/auth/login', { method: 'POST', body: JSON.stringify({email, password}) }); }
async function register(email, username, password, full_name) { return apiFetch('/auth/register', { method: 'POST', body: JSON.stringify({email, username, password, full_name}) }); }
async function adminLogin(email, password) { return apiFetch('/auth/admin/login', { method: 'POST', body: JSON.stringify({email, password}) }); }

// User
async function getProfile() { return apiFetch('/users/profile'); }
async function updateProfile(data) { return apiFetch('/users/profile', { method: 'PUT', body: JSON.stringify(data) }); }
async function changePassword(old_password, new_password) { return apiFetch('/users/change-password', { method: 'POST', body: JSON.stringify({old_password, new_password}) }); }

// Payments
async function initiatePayment(movie_id, series_id, episode_ids, amount, phone_number) { return apiFetch('/payments/initiate', { method: 'POST', body: JSON.stringify({movie_id, series_id, episode_ids, amount, phone_number}) }); }
async function confirmPayment(payment_id, transaction_id, movie_id, series_id, episode_ids) { return apiFetch(`/payments/${payment_id}/confirm`, { method: 'POST', body: JSON.stringify({transaction_id, movie_id, series_id, episode_ids}) }); }
async function getPaymentHistory() { return apiFetch('/payments/history'); }

// Downloads & History
async function getDownloadHistory() { return apiFetch('/downloads/history'); }
async function getPurchasedContent() { return apiFetch('/downloads/purchased'); }

// Reviews
async function addReview(movie_id, series_id, rating, comment) { return apiFetch('/reviews/user-reviews', { method: 'POST', body: JSON.stringify({movie_id, series_id, rating, comment}) }); }

// Analytics (Admin)
async function getAnalyticsOverview() { return apiFetch('/analytics/overview'); }
async function getRevenue7Days() { return apiFetch('/analytics/revenue/7days'); }
async function getUserRegistrations() { return apiFetch('/analytics/users/registrations'); }

// Admin
async function createMovie(data) { return apiFetch('/movies', { method: 'POST', body: JSON.stringify(data) }); }
async function createSeries(data) { return apiFetch('/series', { method: 'POST', body: JSON.stringify(data) }); }
async function addEpisode(series_id, data) { return apiFetch(`/series/${series_id}/episodes`, { method: 'POST', body: JSON.stringify(data) }); }

function logout() { localStorage.removeItem('token'); localStorage.removeItem('user'); window.location.href = '/frontend/user/login.html'; }
