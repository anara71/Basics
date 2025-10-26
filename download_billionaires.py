"""
Script to download and populate billionaire data.
This script fetches billionaire data from multiple sources and populates the database.
"""

import requests
from bs4 import BeautifulSoup
import json
from app import create_app
from models import db, Billionaire
from datetime import datetime


def fetch_forbes_realtime_billionaires():
    """
    Fetch billionaire data from Forbes Real-Time Billionaires API
    Forbes provides a public API endpoint for their billionaire data
    """
    print("Fetching billionaire data from Forbes Real-Time Billionaires...")

    try:
        # Forbes Real-Time Billionaires API endpoint
        url = "https://www.forbes.com/forbesapi/person/rtb/0/position/true.json"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        billionaires_data = []

        if 'personList' in data and 'personsLists' in data['personList']:
            persons = data['personList']['personsLists']

            for person in persons:
                try:
                    billionaire_info = {
                        'person_name': person.get('personName', ''),
                        'rank': person.get('rank'),
                        'final_worth': person.get('finalWorth', 0) / 1000.0,  # Convert to billions
                        'category': person.get('category', ''),
                        'source': person.get('source', ''),
                        'country': person.get('countryOfCitizenship', ''),
                        'city': person.get('city', ''),
                        'organization': person.get('organization', ''),
                        'title': person.get('title', ''),
                        'age': person.get('age'),
                        'gender': person.get('gender', ''),
                        'birthdate': person.get('birthDate', ''),
                        'self_made': person.get('selfMade', False),
                        'philanthropy_score': person.get('philanthropyScore'),
                        'forbes_id': person.get('uri', '')
                    }

                    billionaires_data.append(billionaire_info)

                except Exception as e:
                    print(f"Error processing person data: {e}")
                    continue

        print(f"Successfully fetched {len(billionaires_data)} billionaires from Forbes")
        return billionaires_data

    except requests.RequestException as e:
        print(f"Error fetching Forbes data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def fetch_sample_billionaires():
    """
    Returns sample billionaire data as fallback
    This includes some of the world's most well-known billionaires
    """
    print("Using sample billionaire data...")

    sample_data = [
        {
            'person_name': 'Elon Musk',
            'rank': 1,
            'final_worth': 240.7,
            'category': 'Technology',
            'source': 'Tesla, SpaceX',
            'country': 'United States',
            'city': 'Austin',
            'organization': 'Tesla, SpaceX',
            'title': 'CEO',
            'age': 52,
            'gender': 'M',
            'birthdate': '1971-06-28',
            'self_made': True,
            'philanthropy_score': 3,
            'forbes_id': 'elon-musk'
        },
        {
            'person_name': 'Jeff Bezos',
            'rank': 2,
            'final_worth': 170.3,
            'category': 'Technology',
            'source': 'Amazon',
            'country': 'United States',
            'city': 'Medina',
            'organization': 'Amazon',
            'title': 'Executive Chairman',
            'age': 60,
            'gender': 'M',
            'birthdate': '1964-01-12',
            'self_made': True,
            'philanthropy_score': 4,
            'forbes_id': 'jeff-bezos'
        },
        {
            'person_name': 'Bernard Arnault',
            'rank': 3,
            'final_worth': 165.5,
            'category': 'Fashion & Retail',
            'source': 'LVMH',
            'country': 'France',
            'city': 'Paris',
            'organization': 'LVMH',
            'title': 'Chairman & CEO',
            'age': 75,
            'gender': 'M',
            'birthdate': '1949-03-05',
            'self_made': False,
            'philanthropy_score': 2,
            'forbes_id': 'bernard-arnault'
        },
        {
            'person_name': 'Bill Gates',
            'rank': 4,
            'final_worth': 128.4,
            'category': 'Technology',
            'source': 'Microsoft',
            'country': 'United States',
            'city': 'Medina',
            'organization': 'Microsoft',
            'title': 'Co-Founder',
            'age': 68,
            'gender': 'M',
            'birthdate': '1955-10-28',
            'self_made': True,
            'philanthropy_score': 5,
            'forbes_id': 'bill-gates'
        },
        {
            'person_name': 'Mark Zuckerberg',
            'rank': 5,
            'final_worth': 120.1,
            'category': 'Technology',
            'source': 'Facebook/Meta',
            'country': 'United States',
            'city': 'Palo Alto',
            'organization': 'Meta',
            'title': 'CEO',
            'age': 39,
            'gender': 'M',
            'birthdate': '1984-05-14',
            'self_made': True,
            'philanthropy_score': 4,
            'forbes_id': 'mark-zuckerberg'
        },
        {
            'person_name': 'Larry Ellison',
            'rank': 6,
            'final_worth': 115.2,
            'category': 'Technology',
            'source': 'Oracle',
            'country': 'United States',
            'city': 'Lanai',
            'organization': 'Oracle',
            'title': 'CTO & Founder',
            'age': 79,
            'gender': 'M',
            'birthdate': '1944-08-17',
            'self_made': True,
            'philanthropy_score': 3,
            'forbes_id': 'larry-ellison'
        },
        {
            'person_name': 'Warren Buffett',
            'rank': 7,
            'final_worth': 110.5,
            'category': 'Finance & Investments',
            'source': 'Berkshire Hathaway',
            'country': 'United States',
            'city': 'Omaha',
            'organization': 'Berkshire Hathaway',
            'title': 'CEO',
            'age': 93,
            'gender': 'M',
            'birthdate': '1930-08-30',
            'self_made': True,
            'philanthropy_score': 5,
            'forbes_id': 'warren-buffett'
        },
        {
            'person_name': 'Larry Page',
            'rank': 8,
            'final_worth': 107.3,
            'category': 'Technology',
            'source': 'Google',
            'country': 'United States',
            'city': 'Palo Alto',
            'organization': 'Alphabet',
            'title': 'Co-Founder',
            'age': 50,
            'gender': 'M',
            'birthdate': '1973-03-26',
            'self_made': True,
            'philanthropy_score': 3,
            'forbes_id': 'larry-page'
        },
        {
            'person_name': 'Sergey Brin',
            'rank': 9,
            'final_worth': 103.0,
            'category': 'Technology',
            'source': 'Google',
            'country': 'United States',
            'city': 'Los Altos',
            'organization': 'Alphabet',
            'title': 'Co-Founder',
            'age': 50,
            'gender': 'M',
            'birthdate': '1973-08-21',
            'self_made': True,
            'philanthropy_score': 3,
            'forbes_id': 'sergey-brin'
        },
        {
            'person_name': 'Steve Ballmer',
            'rank': 10,
            'final_worth': 101.2,
            'category': 'Technology',
            'source': 'Microsoft',
            'country': 'United States',
            'city': 'Hunts Point',
            'organization': 'Los Angeles Clippers',
            'title': 'Owner',
            'age': 67,
            'gender': 'M',
            'birthdate': '1956-03-24',
            'self_made': True,
            'philanthropy_score': 3,
            'forbes_id': 'steve-ballmer'
        }
    ]

    return sample_data


def populate_database(billionaires_data):
    """Populate the database with billionaire data"""
    if not billionaires_data:
        print("No billionaire data to populate")
        return

    app = create_app()

    with app.app_context():
        print(f"Populating database with {len(billionaires_data)} billionaires...")

        added_count = 0
        updated_count = 0

        for data in billionaires_data:
            try:
                # Check if billionaire already exists
                existing = None
                if data.get('forbes_id'):
                    existing = Billionaire.query.filter_by(forbes_id=data['forbes_id']).first()

                if existing:
                    # Update existing record
                    for key, value in data.items():
                        setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                else:
                    # Create new record
                    billionaire = Billionaire(**data)
                    db.session.add(billionaire)
                    added_count += 1

            except Exception as e:
                print(f"Error adding billionaire {data.get('person_name', 'Unknown')}: {e}")
                continue

        try:
            db.session.commit()
            print(f"Successfully added {added_count} new billionaires")
            print(f"Successfully updated {updated_count} existing billionaires")
            print(f"Total billionaires in database: {Billionaire.query.count()}")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to database: {e}")


def main():
    """Main function to download and populate billionaire data"""
    print("=" * 60)
    print("Billionaire Data Download Script")
    print("=" * 60)

    # Try to fetch from Forbes API
    billionaires_data = fetch_forbes_realtime_billionaires()

    # If Forbes API fails, use sample data
    if not billionaires_data:
        print("\nForbes API unavailable, using sample data...")
        billionaires_data = fetch_sample_billionaires()

    # Populate database
    if billionaires_data:
        populate_database(billionaires_data)
        print("\nDatabase population complete!")
    else:
        print("\nFailed to fetch billionaire data")

    print("=" * 60)


if __name__ == '__main__':
    main()
