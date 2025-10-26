# Deployment Guide

This guide covers multiple ways to deploy and run the Billionaire Relationship Tracker application.

## Quick Start (Local Development)

### Option 1: Using Startup Scripts (Easiest)

**On Linux/Mac:**
```bash
./start.sh
```

**On Windows:**
```cmd
start.bat
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Set up the database
- Start the application at http://localhost:5000

### Option 2: Manual Setup

**Step 1: Install Dependencies**
```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

# Install packages
pip install -r requirements.txt
```

**Step 2: Set Up Database**
```bash
# Download and populate billionaire data
python download_billionaires.py
```

**Step 3: Run the Application**
```bash
python app.py
```

Open your browser to: http://localhost:5000

---

## Production Deployment

### Prerequisites for Production

1. **Change Secret Keys**

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` and set secure random keys:
```env
SECRET_KEY=your-very-long-random-secret-key-here
JWT_SECRET_KEY=another-very-long-random-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

Generate secure keys with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Upgrade Database (Optional but Recommended)**

For production, use PostgreSQL or MySQL instead of SQLite.

---

## Production Deployment Options

### Option 1: Deploy to Heroku (Free Tier Available)

**Step 1: Install Heroku CLI**
```bash
# Install from https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Create Heroku App**
```bash
heroku login
heroku create your-app-name
```

**Step 3: Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

**Step 4: Create Procfile**
Already created (see below), just commit and push:
```bash
git add Procfile
git commit -m "Add Procfile for Heroku"
git push heroku main
```

**Step 5: Initialize Database**
```bash
heroku run python download_billionaires.py
```

**Step 6: Open App**
```bash
heroku open
```

---

### Option 2: Deploy to DigitalOcean App Platform

**Step 1: Push to GitHub**
```bash
git push origin main
```

**Step 2: Create App on DigitalOcean**
- Go to https://cloud.digitalocean.com/apps
- Click "Create App"
- Connect your GitHub repository
- Select the repository

**Step 3: Configure Build Settings**
- Build Command: `pip install -r requirements.txt`
- Run Command: `gunicorn app:app`

**Step 4: Add Database**
- Add a PostgreSQL database component
- Update environment variable: `SQLALCHEMY_DATABASE_URI`

**Step 5: Deploy**
- Click "Deploy"

---

### Option 3: Deploy to AWS EC2

**Step 1: Launch EC2 Instance**
- Ubuntu Server 22.04 LTS
- t2.micro (free tier eligible)
- Open ports 22 (SSH) and 80 (HTTP)

**Step 2: SSH into Server**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**Step 3: Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

**Step 4: Clone Repository**
```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

**Step 5: Set Up Application**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
python download_billionaires.py
```

**Step 6: Create Systemd Service**
```bash
sudo nano /etc/systemd/system/billionaire-tracker.service
```

Add:
```ini
[Unit]
Description=Billionaire Tracker
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/yourrepo
Environment="PATH=/home/ubuntu/yourrepo/venv/bin"
ExecStart=/home/ubuntu/yourrepo/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

**Step 7: Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/billionaire-tracker
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and start:
```bash
sudo ln -s /etc/nginx/sites-available/billionaire-tracker /etc/nginx/sites-enabled/
sudo systemctl restart nginx
sudo systemctl start billionaire-tracker
sudo systemctl enable billionaire-tracker
```

---

### Option 4: Deploy to Render.com (Easy & Free)

**Step 1: Push to GitHub**
```bash
git push origin main
```

**Step 2: Create Web Service on Render**
- Go to https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository

**Step 3: Configure Service**
- Name: `billionaire-tracker`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

**Step 4: Add Environment Variables**
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-key
```

**Step 5: Add PostgreSQL Database**
- Create a PostgreSQL database on Render
- Copy the Internal Database URL
- Add environment variable: `SQLALCHEMY_DATABASE_URI`

**Step 6: Deploy**
- Click "Create Web Service"
- Wait for deployment
- Run shell command: `python download_billionaires.py`

---

### Option 5: Deploy to Railway.app (Very Easy)

**Step 1: Push to GitHub**
```bash
git push origin main
```

**Step 2: Deploy on Railway**
- Go to https://railway.app
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository

**Step 3: Add PostgreSQL**
- Click "New" → "Database" → "PostgreSQL"
- Railway automatically sets `DATABASE_URL`

**Step 4: Configure Environment**
Railway auto-detects Python. Add environment variables:
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-key
```

**Step 5: Initialize Database**
- Open the web service shell
- Run: `python download_billionaires.py`

---

### Option 6: Docker Deployment

**Step 1: Build Docker Image**
```bash
docker build -t billionaire-tracker .
```

**Step 2: Run Container**
```bash
docker run -d -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-key \
  billionaire-tracker
```

**Step 3: Initialize Database**
```bash
docker exec -it <container-id> python download_billionaires.py
```

---

## Database Migration (SQLite to PostgreSQL)

**Step 1: Install PostgreSQL Driver**
```bash
pip install psycopg2-binary
```

**Step 2: Update Database URI**
In `app.py` or `.env`:
```python
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/billionaire_tracker
```

**Step 3: Migrate Data**
```bash
# Export from SQLite
sqlite3 instance/billionaire_tracker.db .dump > backup.sql

# Import to PostgreSQL (requires manual conversion)
# Or use a migration tool like Flask-Migrate
```

---

## Monitoring and Maintenance

### View Logs
```bash
# Heroku
heroku logs --tail

# AWS EC2
sudo journalctl -u billionaire-tracker -f

# Docker
docker logs -f <container-id>
```

### Update Billionaire Data
Run periodically:
```bash
python download_billionaires.py
```

### Backup Database
```bash
# SQLite
cp instance/billionaire_tracker.db backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

---

## Security Checklist for Production

- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
- [ ] Use HTTPS (SSL certificate via Let's Encrypt)
- [ ] Use a production database (PostgreSQL/MySQL)
- [ ] Set up regular database backups
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up firewall rules
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Use environment variables for sensitive data

---

## Troubleshooting

**Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

**Module not found errors:**
```bash
pip install -r requirements.txt
```

**Database locked (SQLite):**
- SQLite doesn't handle concurrent writes well
- Upgrade to PostgreSQL for production

**Permission errors:**
```bash
chmod +x start.sh
```

---

## Support

For issues, check:
1. Application logs
2. Database connectivity
3. Environment variables
4. File permissions

For questions or bug reports, create an issue on GitHub.
