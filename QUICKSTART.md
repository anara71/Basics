# Quick Start Guide

Get your Billionaire Relationship Tracker running in less than 2 minutes!

## Fastest Way to Run (Recommended)

### On Linux/Mac:
```bash
./start.sh
```

### On Windows:
```cmd
start.bat
```

That's it! The script handles everything automatically.

Open your browser to: **http://localhost:5000**

---

## Manual Installation (3 Steps)

If you prefer to run commands manually:

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Database
```bash
python download_billionaires.py
```

### Step 3: Run the App
```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## Using the Application

### 1. Register an Account
- Click "Register" on the login page
- Create your username, email, and password
- Your password is securely hashed with bcrypt

### 2. Browse Billionaires
- View 3000+ billionaire profiles (currently 10 in sample database)
- Search by name, company, or source of wealth
- Filter by country, industry, or net worth
- See detailed information about each billionaire

### 3. Track Relationships
- Click "Track Relationship" on any billionaire
- Set relationship status: Prospect, Contacted, In Discussion, Partner, Inactive
- Set priority: High, Medium, Low
- Add notes about your interactions
- Set last contact date and next follow-up reminder
- Add custom tags to organize your relationships

### 4. Manage Your Relationships
- Go to "My Relationships" tab
- View all billionaires you're tracking
- Filter by status and priority
- Edit or delete relationships
- Update notes and follow-up dates

### 5. View Statistics
- Go to "Statistics" tab
- See total billionaire count
- View distribution by country
- View distribution by industry

---

## Features

✅ **Secure Authentication**
- User registration and login
- Password hashing with bcrypt
- JWT token-based sessions
- Each user's data is completely private

✅ **Comprehensive Billionaire Database**
- 3000+ profiles (expandable)
- Net worth rankings
- Industry categories
- Geographic information
- Age, gender, self-made status
- Philanthropy scores

✅ **Relationship Management**
- Track multiple relationships
- Custom notes and tags
- Follow-up reminders
- Priority levels
- Status tracking

✅ **Advanced Features**
- Real-time search
- Multi-criteria filtering
- Pagination for large datasets
- Responsive design (mobile-friendly)
- RESTful API

---

## Default Database

The application includes 10 sample billionaires:
1. Elon Musk - $240.7B (Tesla, SpaceX)
2. Jeff Bezos - $170.3B (Amazon)
3. Bernard Arnault - $165.5B (LVMH)
4. Bill Gates - $128.4B (Microsoft)
5. Mark Zuckerberg - $120.1B (Meta)
6. Larry Ellison - $115.2B (Oracle)
7. Warren Buffett - $110.5B (Berkshire Hathaway)
8. Larry Page - $107.3B (Google)
9. Sergey Brin - $103.0B (Google)
10. Steve Ballmer - $101.2B (Microsoft)

---

## Adding More Billionaires

The `download_billionaires.py` script attempts to fetch real-time data from Forbes API. If the API is available, it will download 3000+ billionaire profiles automatically.

To refresh the data:
```bash
python download_billionaires.py
```

You can also import custom CSV data or integrate with other data sources.

---

## Architecture

**Backend:**
- Flask (Python web framework)
- SQLite database (upgradeable to PostgreSQL/MySQL)
- SQLAlchemy ORM
- JWT authentication
- Bcrypt password hashing

**Frontend:**
- HTML5
- CSS3 (responsive design)
- Vanilla JavaScript
- No external JavaScript libraries required

**API:**
- RESTful API with JSON
- Authentication endpoints
- Billionaire data endpoints
- Relationship management endpoints

---

## File Structure

```
Basics/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── auth.py                     # Authentication endpoints
├── api.py                      # API endpoints
├── download_billionaires.py   # Data download script
├── requirements.txt            # Python dependencies
├── static/
│   ├── index.html             # Frontend HTML
│   ├── styles.css             # Frontend CSS
│   └── app.js                 # Frontend JavaScript
├── instance/
│   └── billionaire_tracker.db # SQLite database (auto-created)
├── README.md                  # Full documentation
├── DEPLOYMENT.md              # Deployment guide
├── QUICKSTART.md              # This file
├── start.sh                   # Linux/Mac startup script
├── start.bat                  # Windows startup script
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
└── Procfile                   # Heroku deployment file
```

---

## Common Issues

**Port 5000 already in use:**
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>
```

**Module not found errors:**
```bash
pip install -r requirements.txt
```

**Permission denied (Linux/Mac):**
```bash
chmod +x start.sh
./start.sh
```

**Database not found:**
```bash
python download_billionaires.py
```

---

## Next Steps

1. **Customize the App**
   - Update the frontend styles
   - Add more features
   - Integrate with external APIs

2. **Deploy to Production**
   - See DEPLOYMENT.md for detailed deployment guides
   - Platforms: Heroku, DigitalOcean, AWS, Render, Railway
   - Deploy with Docker

3. **Upgrade Database**
   - Switch from SQLite to PostgreSQL for production
   - See DEPLOYMENT.md for migration guide

4. **Add More Data**
   - Import CSV files
   - Integrate with Forbes, Bloomberg APIs
   - Add custom billionaire profiles

---

## Documentation

- **README.md** - Comprehensive documentation
- **DEPLOYMENT.md** - Production deployment guide
- **QUICKSTART.md** - This file

---

## Support

If you encounter any issues:
1. Check the documentation
2. Review the error messages
3. Check application logs
4. Create an issue on GitHub

---

## Security Note

**For production deployments:**
1. Change `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`
2. Use a production database (PostgreSQL/MySQL)
3. Enable HTTPS
4. Set up proper firewall rules
5. Keep dependencies updated

---

Enjoy tracking your billionaire relationships! 🚀
