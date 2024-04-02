from flask import Blueprint, request, jsonify, current_app
import uuid
from app import db
from app.models import User, Invitation, ProfilePicture
from app.auth import create_user, verify_password, get_user_by_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/invite', methods=['POST'])
def invite():
    unique_id = str(uuid.uuid4())
    invitation = Invitation(unique_id=unique_id)
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'unique_id': invitation.unique_id}), 201

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ['name', 'email', 'phone', 'password', 'unique_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'A user with this email already exists.'}), 409

    unique_id = data['unique_id']
    invitation = Invitation.query.filter_by(unique_id=unique_id, user_id=None).first()
    if not invitation:
        return jsonify({'message': 'Invalid or expired invitation.'}), 400

    user = create_user(data['name'], data['email'], data['phone'], data['password'])
    invitation.user_id = user.id
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_email(data.get('email'))
    if user and verify_password(user.password_hash, data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid email or password.'}), 401

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'You have been logged out.'}), 200

@bp.route('/edit_user', methods=['POST'])
@jwt_required()
def edit_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    try:
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.alternate_email = data.get('alternate_email', user.alternate_email)

        if 'profile_picture' in data:
            if data['profile_picture']:
                profile_picture = ProfilePicture.query.filter_by(user_id=user.id).first()
                if profile_picture:
                    profile_picture.picture_url = data['profile_picture']
                else:
                    new_profile_picture = ProfilePicture(user_id=user.id, picture_url=data['profile_picture'])
                    db.session.add(new_profile_picture)
            else:
                profile_picture = ProfilePicture.query.filter_by(user_id=user.id).first()
                if profile_picture:
                    db.session.delete(profile_picture)

        db.session.commit()
        return jsonify({'message': 'User details updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"An error occurred updating user details: {str(e)}")
        return jsonify({'error': 'An error occurred updating the user details. Please try again later.'}), 500
