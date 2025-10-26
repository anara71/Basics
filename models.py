from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication and data isolation"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user's billionaire relationships
    relationships = db.relationship('BillionaireRelationship', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Billionaire(db.Model):
    """Billionaire data model - shared across all users"""
    __tablename__ = 'billionaires'

    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.Integer)
    final_worth = db.Column(db.Float)  # Net worth in billions
    category = db.Column(db.String(100))  # Industry/category
    source = db.Column(db.String(200))  # Source of wealth
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    title = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    birthdate = db.Column(db.String(50))
    self_made = db.Column(db.Boolean)
    philanthropy_score = db.Column(db.Integer)

    # External IDs
    forbes_id = db.Column(db.String(100), unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to user relationships
    relationships = db.relationship('BillionaireRelationship', backref='billionaire', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'person_name': self.person_name,
            'rank': self.rank,
            'final_worth': self.final_worth,
            'category': self.category,
            'source': self.source,
            'country': self.country,
            'city': self.city,
            'organization': self.organization,
            'title': self.title,
            'age': self.age,
            'gender': self.gender,
            'birthdate': self.birthdate,
            'self_made': self.self_made,
            'philanthropy_score': self.philanthropy_score
        }

    def __repr__(self):
        return f'<Billionaire {self.person_name}>'


class BillionaireRelationship(db.Model):
    """User-specific relationship tracking with billionaires"""
    __tablename__ = 'billionaire_relationships'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    billionaire_id = db.Column(db.Integer, db.ForeignKey('billionaires.id'), nullable=False)

    # Relationship tracking fields
    relationship_status = db.Column(db.String(50))  # e.g., 'contacted', 'in-discussion', 'partner', etc.
    priority = db.Column(db.String(20))  # 'high', 'medium', 'low'
    notes = db.Column(db.Text)
    last_contact_date = db.Column(db.Date)
    next_followup_date = db.Column(db.Date)
    tags = db.Column(db.String(500))  # Comma-separated tags

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: one relationship per user-billionaire pair
    __table_args__ = (db.UniqueConstraint('user_id', 'billionaire_id', name='unique_user_billionaire'),)

    def to_dict(self):
        return {
            'id': self.id,
            'billionaire': self.billionaire.to_dict(),
            'relationship_status': self.relationship_status,
            'priority': self.priority,
            'notes': self.notes,
            'last_contact_date': self.last_contact_date.isoformat() if self.last_contact_date else None,
            'next_followup_date': self.next_followup_date.isoformat() if self.next_followup_date else None,
            'tags': self.tags,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Relationship User:{self.user_id} Billionaire:{self.billionaire_id}>'
