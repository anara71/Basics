from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Billionaire, BillionaireRelationship
from datetime import datetime
from sqlalchemy import or_, and_

api_bp = Blueprint('api', __name__)


@api_bp.route('/billionaires', methods=['GET'])
@jwt_required()
def get_billionaires():
    """Get all billionaires with optional filtering and search"""
    try:
        user_id = int(get_jwt_identity())

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search = request.args.get('search', '')
        country = request.args.get('country', '')
        category = request.args.get('category', '')
        min_worth = request.args.get('min_worth', type=float)
        max_worth = request.args.get('max_worth', type=float)

        # Build query
        query = Billionaire.query

        # Apply filters
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Billionaire.person_name.ilike(search_pattern),
                    Billionaire.organization.ilike(search_pattern),
                    Billionaire.source.ilike(search_pattern)
                )
            )

        if country:
            query = query.filter(Billionaire.country == country)

        if category:
            query = query.filter(Billionaire.category == category)

        if min_worth is not None:
            query = query.filter(Billionaire.final_worth >= min_worth)

        if max_worth is not None:
            query = query.filter(Billionaire.final_worth <= max_worth)

        # Order by rank
        query = query.order_by(Billionaire.rank.asc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'billionaires': [b.to_dict() for b in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/billionaires/<int:billionaire_id>', methods=['GET'])
@jwt_required()
def get_billionaire(billionaire_id):
    """Get a single billionaire by ID"""
    try:
        billionaire = Billionaire.query.get(billionaire_id)

        if not billionaire:
            return jsonify({'error': 'Billionaire not found'}), 404

        return jsonify({'billionaire': billionaire.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/billionaires/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get statistics about billionaires"""
    try:
        total = Billionaire.query.count()

        # Count by country
        countries = db.session.query(
            Billionaire.country,
            db.func.count(Billionaire.id)
        ).group_by(Billionaire.country).order_by(db.func.count(Billionaire.id).desc()).limit(10).all()

        # Count by category
        categories = db.session.query(
            Billionaire.category,
            db.func.count(Billionaire.id)
        ).group_by(Billionaire.category).order_by(db.func.count(Billionaire.id).desc()).limit(10).all()

        return jsonify({
            'total_billionaires': total,
            'top_countries': [{'country': c[0], 'count': c[1]} for c in countries],
            'top_categories': [{'category': c[0], 'count': c[1]} for c in categories]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== RELATIONSHIP MANAGEMENT ====================

@api_bp.route('/relationships', methods=['GET'])
@jwt_required()
def get_relationships():
    """Get all relationships for the current user"""
    try:
        user_id = int(get_jwt_identity())

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status', '')
        priority = request.args.get('priority', '')

        # Build query
        query = BillionaireRelationship.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(relationship_status=status)

        if priority:
            query = query.filter_by(priority=priority)

        # Order by updated_at
        query = query.order_by(BillionaireRelationship.updated_at.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'relationships': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/relationships', methods=['POST'])
@jwt_required()
def create_relationship():
    """Create or update a relationship with a billionaire"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        billionaire_id = data.get('billionaire_id')

        if not billionaire_id:
            return jsonify({'error': 'billionaire_id is required'}), 400

        # Check if billionaire exists
        billionaire = Billionaire.query.get(billionaire_id)
        if not billionaire:
            return jsonify({'error': 'Billionaire not found'}), 404

        # Check if relationship already exists
        existing = BillionaireRelationship.query.filter_by(
            user_id=user_id,
            billionaire_id=billionaire_id
        ).first()

        if existing:
            # Update existing relationship
            if 'relationship_status' in data:
                existing.relationship_status = data['relationship_status']
            if 'priority' in data:
                existing.priority = data['priority']
            if 'notes' in data:
                existing.notes = data['notes']
            if 'last_contact_date' in data:
                existing.last_contact_date = datetime.fromisoformat(data['last_contact_date']) if data['last_contact_date'] else None
            if 'next_followup_date' in data:
                existing.next_followup_date = datetime.fromisoformat(data['next_followup_date']) if data['next_followup_date'] else None
            if 'tags' in data:
                existing.tags = data['tags']

            existing.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Relationship updated successfully',
                'relationship': existing.to_dict()
            }), 200

        else:
            # Create new relationship
            new_relationship = BillionaireRelationship(
                user_id=user_id,
                billionaire_id=billionaire_id,
                relationship_status=data.get('relationship_status', ''),
                priority=data.get('priority', 'medium'),
                notes=data.get('notes', ''),
                last_contact_date=datetime.fromisoformat(data['last_contact_date']) if data.get('last_contact_date') else None,
                next_followup_date=datetime.fromisoformat(data['next_followup_date']) if data.get('next_followup_date') else None,
                tags=data.get('tags', '')
            )

            db.session.add(new_relationship)
            db.session.commit()

            return jsonify({
                'message': 'Relationship created successfully',
                'relationship': new_relationship.to_dict()
            }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/relationships/<int:relationship_id>', methods=['GET'])
@jwt_required()
def get_relationship(relationship_id):
    """Get a specific relationship"""
    try:
        user_id = int(get_jwt_identity())

        relationship = BillionaireRelationship.query.filter_by(
            id=relationship_id,
            user_id=user_id
        ).first()

        if not relationship:
            return jsonify({'error': 'Relationship not found'}), 404

        return jsonify({'relationship': relationship.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/relationships/<int:relationship_id>', methods=['PUT'])
@jwt_required()
def update_relationship(relationship_id):
    """Update a relationship"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        relationship = BillionaireRelationship.query.filter_by(
            id=relationship_id,
            user_id=user_id
        ).first()

        if not relationship:
            return jsonify({'error': 'Relationship not found'}), 404

        # Update fields
        if 'relationship_status' in data:
            relationship.relationship_status = data['relationship_status']
        if 'priority' in data:
            relationship.priority = data['priority']
        if 'notes' in data:
            relationship.notes = data['notes']
        if 'last_contact_date' in data:
            relationship.last_contact_date = datetime.fromisoformat(data['last_contact_date']) if data['last_contact_date'] else None
        if 'next_followup_date' in data:
            relationship.next_followup_date = datetime.fromisoformat(data['next_followup_date']) if data['next_followup_date'] else None
        if 'tags' in data:
            relationship.tags = data['tags']

        relationship.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'message': 'Relationship updated successfully',
            'relationship': relationship.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/relationships/<int:relationship_id>', methods=['DELETE'])
@jwt_required()
def delete_relationship(relationship_id):
    """Delete a relationship"""
    try:
        user_id = int(get_jwt_identity())

        relationship = BillionaireRelationship.query.filter_by(
            id=relationship_id,
            user_id=user_id
        ).first()

        if not relationship:
            return jsonify({'error': 'Relationship not found'}), 404

        db.session.delete(relationship)
        db.session.commit()

        return jsonify({'message': 'Relationship deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
