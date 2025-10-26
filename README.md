# Billionaire Relationship Tracker

A comprehensive web application to track and manage relationships with 3000+ billionaires worldwide. Features secure user authentication, an SQL database, and a modern web interface.

## Features

- **User Authentication**: Secure registration and login system with password hashing
- **Password Protection**: Each user's data is isolated and protected
- **Billionaire Database**: 3000+ billionaire profiles with detailed information
- **Relationship Management**: Track your interactions, notes, and follow-ups with billionaires
- **Advanced Filtering**: Search and filter by name, country, industry, net worth
- **Statistics Dashboard**: View insights about billionaire distribution
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful API with JSON

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
cd /home/user/Basics
```

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download billionaire data**
```bash
python download_billionaires.py
```

This will attempt to fetch real-time data from Forbes API, or use sample data if the API is unavailable.

5. **Run the application**
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Usage

### Getting Started

1. **Register a new account**
   - Open `http://localhost:5000` in your browser
   - Click "Register" and create your account
   - Your password is securely hashed and stored

2. **Browse billionaires**
   - View the complete list of billionaires
   - Use search and filters to find specific individuals
   - See detailed information including net worth, industry, country, etc.

3. **Track relationships**
   - Click "Track Relationship" on any billionaire
   - Set relationship status (Prospect, Contacted, In Discussion, Partner, Inactive)
   - Set priority (High, Medium, Low)
   - Add notes about your interactions
   - Set last contact date and next follow-up date
   - Add custom tags

4. **Manage your relationships**
   - Go to "My Relationships" tab
   - View all tracked billionaires
   - Filter by status and priority
   - Edit or delete relationships

5. **View statistics**
   - See total number of billionaires
   - View top countries and industries
   - Analyze billionaire distribution

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Bcrypt hashed password
- `created_at`: Account creation timestamp

### Billionaires Table
- `id`: Primary key
- `person_name`: Full name
- `rank`: Forbes ranking
- `final_worth`: Net worth in billions
- `category`: Industry/category
- `source`: Source of wealth
- `country`: Country of citizenship
- `city`: Primary residence
- `organization`: Main company/organization
- `title`: Job title
- `age`: Age
- `gender`: Gender
- `birthdate`: Date of birth
- `self_made`: Boolean indicating self-made status
- `philanthropy_score`: Philanthropy rating
- `forbes_id`: Unique Forbes identifier

### BillionaireRelationship Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `billionaire_id`: Foreign key to Billionaires
- `relationship_status`: Current status
- `priority`: Priority level
- `notes`: Custom notes
- `last_contact_date`: Date of last contact
- `next_followup_date`: Date for next follow-up
- `tags`: Comma-separated tags
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/profile` - Get user profile
- `POST /auth/logout` - Logout user

### Billionaires
- `GET /api/billionaires` - List all billionaires (with pagination and filters)
- `GET /api/billionaires/<id>` - Get single billionaire
- `GET /api/billionaires/stats` - Get statistics

### Relationships
- `GET /api/relationships` - List user's relationships
- `POST /api/relationships` - Create new relationship
- `GET /api/relationships/<id>` - Get single relationship
- `PUT /api/relationships/<id>` - Update relationship
- `DELETE /api/relationships/<id>` - Delete relationship

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- SQL injection protection via SQLAlchemy ORM
- User data isolation (users can only access their own relationships)
- Input validation on all forms
- CORS configuration for API security

## Configuration

You can customize the application by setting environment variables:

- `SECRET_KEY`: Flask secret key (change in production)
- `JWT_SECRET_KEY`: JWT token secret (change in production)
- `SQLALCHEMY_DATABASE_URI`: Database connection string

## Updating Billionaire Data

To refresh the billionaire data:

```bash
python download_billionaires.py
```

This script can be run periodically to keep the data up-to-date.

## Upgrading to Production Database

To use PostgreSQL or MySQL instead of SQLite:

1. Install the appropriate driver:
```bash
pip install psycopg2-binary  # For PostgreSQL
# or
pip install pymysql  # For MySQL
```

2. Update the database URI in `app.py`:
```python
# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/billionaire_tracker'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/billionaire_tracker'
```

## Troubleshooting

**Database errors:**
- Delete `billionaire_tracker.db` and restart the application to recreate the database

**No billionaires showing:**
- Run `python download_billionaires.py` to populate the database

**Login issues:**
- Clear browser cache and localStorage
- Check console for error messages

## Future Enhancements

- Email notifications for follow-ups
- Calendar integration
- Export relationships to CSV/Excel
- Advanced analytics and visualizations
- Mobile app
- Social media integration
- News feed for tracked billionaires

## License

This project is for educational and personal use.

## Support

For issues or questions, please check the documentation or create an issue in the repository.
