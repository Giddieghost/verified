# Get Movies - Premium Video Streaming Platform

A complete, production-ready video streaming platform built with Flask, SQLAlchemy, and modern JavaScript. Features user/admin authentication, payment integration (M-Pesa), video streaming, and comprehensive analytics.

## 🎯 Features

### User Features
- 🔐 Secure authentication with hashed passwords and JWT tokens
- 🎬 Browse and search for movies and series
- ▶️ Stream trailers and full videos
- 💾 Download videos for offline viewing
- 💳 Secure payment with M-Pesa integration
- ⏱️ 7-day access countdown for purchased content
- 📊 Watch history tracking
- ⭐ Rate and review content
- 🌓 Dark/Light theme toggle
- 📥 Manage downloads
- 👤 Profile management and password change

### Admin Features
- 📤 Upload movies and series with thumbnails
- 🎞️ Manage multiple episodes for series
- 👥 View user management dashboard
- 💰 Track payment records and revenue
- 📈 Analytics with revenue growth charts (7-day, monthly, yearly)
- 📊 User registration trends
- 📥 Download statistics
- 🔐 Secure admin authentication

## 🏗️ Project Structure

```
get-movies/
├── backend/
│   ├── app.py                 # Flask app factory
│   ├── config.py              # Environment configuration
│   ├── requirements.txt        # Python dependencies
│   ├── models/                # Database models
│   ├── routes/                # API endpoints
│   ├── services/              # Business logic
│   ├── utils/                 # Helpers & middleware
│   ├── database/              # Database setup
│   └── uploads/               # File storage
├── frontend/
│   ├── user/                  # User-facing templates
│   ├── admin/                 # Admin panel templates
│   └── components/            # Shared components
├── static/
│   ├── css/                   # Stylesheets
│   ├── js/                    # Client-side scripts
│   └── images/               # Assets
├── database/                  # Database schema & seed
├── config/                    # Environment configs
├── tests/                     # Test suite
├── docs/                      # Documentation
└── run.py                     # Entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- SQLite (development) or PostgreSQL (production)

### Installation

1. **Clone and setup environment**
   ```bash
   cd get_movies_project
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file
   echo SECRET_KEY=your-super-secret-key >> .env
   echo DATABASE_URL=sqlite:///app.db >> .env
   echo FLASK_ENV=development >> .env
   ```

4. **Initialize database**
   ```bash
   python -c "from backend.app import create_app; from backend.database.db import db; app = create_app(); 
   with app.app_context(): db.create_all(); print('Database initialized!')"
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the platform**
   - User: http://127.0.0.1:5000/frontend/user/login.html
   - Admin: http://127.0.0.1:5000/frontend/admin/login.html

## 🔐 Authentication

### Default Test Accounts
**Admin:**
- Email: admin@getmovies.com
- Password: Admin@123456

**User:**
- Email: user@getmovies.com
- Password: User@123456

### How It Works
1. User submits credentials
2. Password verified with bcrypt
3. JWT token generated (30-day expiry)
4. Token stored in localStorage
5. All requests include `Authorization: Bearer <token>`
6. Middleware validates token and loads user context

## 💳 Payment Integration (M-Pesa)

### Payment Flow
1. User selects content and initiates payment
2. M-Pesa STK Push sent to phone
3. User enters M-Pesa PIN
4. Payment status checked
5. Purchase automatically added to user account
6. 7-day access countdown starts

### Configuration
```python
# backend/services/daraja_service.py
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
```

## 🎥 External Storage Integration

Video files are stored on external cloud storage (S3, Firebase, etc.)

### Video URLs
- Videos: `https://storage.example.com/videos/{movie_id}.mp4`
- Thumbnails: `https://storage.example.com/thumbnails/{movie_id}.jpg`
- Trailers: `https://storage.example.com/trailers/{movie_id}.mp4`

### Upload Process
1. Admin uploads video
2. File sent to external storage
3. URL stored in database
4. Frontend retrieves and streams video

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/admin/login` - Admin login

### Movies
- `GET /api/movies` - List movies (paginated)
- `GET /api/movies/:id` - Get movie details
- `POST /api/movies` - Create movie (admin only)
- `GET /api/movies/:id/reviews` - Get reviews

### Series
- `GET /api/series` - List series
- `GET /api/series/:id/episodes` - Get episodes
- `POST /api/series` - Create series (admin)
- `POST /api/series/:id/episodes` - Add episode (admin)

### Payments
- `POST /api/payments/initiate` - Start payment
- `POST /api/payments/:id/confirm` - Confirm payment
- `GET /api/payments/history` - User's payment history
- `GET /api/payments/admin/revenue` - Admin revenue (admin)

### Analytics
- `GET /api/analytics/overview` - Dashboard stats (admin)
- `GET /api/analytics/revenue/7days` - 7-day revenue
- `GET /api/analytics/users/registrations` - User registrations

## 🎨 UI/UX Design

### Theme
- **Color Scheme**: Dark background (#141414) with red accents (#e50914)
- **Typography**: Segoe UI, Tahoma, Verdana
- **Layout**: Netflix-inspired carousel with hover effects
- **Responsive**: Mobile-first, works on all devices

### Dark/Light Theme
Toggle button in navigation - stored in localStorage

## 🔒 Security Features

1. **Password Hashing**: bcrypt with salt rounds
2. **JWT Tokens**: Signed with SECRET_KEY, 30-day expiry
3. **CORS**: Enabled for trusted origins
4. **SQL Injection**: Protected by SQLAlchemy ORM
5. **XSS Protection**: Jinja2 autoescaping
6. **CSRF**: Token validation on forms
7. **Admin-only routes**: `@admin_required` decorator
8. **User scoping**: Users can only access their own data

## 📱 Responsive Design

- Desktop: Full navigation, carousel view
- Tablet: Optimized grid layout
- Mobile: Hamburger menu, single column

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Coverage
pytest --cov=backend tests/
```

## 📈 Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set strong `SECRET_KEY`
- [ ] Configure M-Pesa credentials
- [ ] Setup external storage (S3/Firebase)
- [ ] Enable database backups
- [ ] Setup error logging (Sentry)
- [ ] Configure CDN for static files
- [ ] Setup monitoring & alerts

### Gunicorn Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run.py
```

## 🛠️ Troubleshooting

**Database Issues**
```bash
python -c "from backend.app import create_app; from backend.database.db import db; 
app = create_app(); 
with app.app_context(): db.drop_all(); db.create_all(); print('Reset complete!')"
```

**Port Already in Use**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

## 📚 Documentation

- [API Documentation](docs/api_documentation.md)
- [System Architecture](docs/system_architecture.md)
- [Setup Guide](docs/setup_guide.md)

## 🤝 Contributing

Pull requests welcome! Please:
1. Create a feature branch
2. Add tests
3. Follow PEP 8 style guide
4. Update documentation

## 📄 License

MIT License - See LICENSE file for details

## 📧 Support

- Email: support@getmovies.com
- Issues: GitHub Issues
- Docs: https://getmovies.docs

---

**Get Movies** © 2026 | Premium Video Streaming Platform
