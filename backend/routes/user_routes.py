from flask import Blueprint, jsonify, request
from services.user_service import UserService
from database.db import db
from logger_config import get_logger

user_bp = Blueprint('users', __name__)
user_service = UserService()
logger = get_logger(__name__)


# CREATE - Add a new user
@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        logger.info(f"Creating user with email: {data.get('email')}")

        if not data or not all(key in data for key in ['name', 'email']):
            logger.warning("Missing required fields in create user request")
            return jsonify({'error': 'Missing required fields: name, email'}), 400

        user = user_service.create_user(data)
        logger.info(
            f"User created successfully with ID: {user.id}, Email: {user.email}")
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    except ValueError as e:
        logger.warning(f"Validation error during user creation: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(
            f"Unexpected error during user creation: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# READ - Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        logger.debug("Fetching all users")
        users = user_service.get_all_users()
        logger.info(f"Retrieved {len(users)} users")
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# READ - Get a specific user by ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        logger.debug(f"Fetching user with ID: {user_id}")
        user = user_service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        logger.info(f"User retrieved: {user.email}")
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# UPDATE - Update a user
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        data = request.get_json()
        logger.info(f"Updating user with ID: {user_id}")
        user = user_service.update_user(user_id, data)
        if not user:
            logger.warning(f"User not found for update with ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        logger.info(f"User updated successfully: {user.email}")
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except ValueError as e:
        logger.warning(f"Validation error during user update: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# DELETE - Delete a user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        success = user_service.delete_user(user_id)
        if not success:
            logger.warning(f"User not found for deletion with ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        logger.info(f"User deleted successfully with ID: {user_id}")
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# Health check endpoint
@user_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.debug("Health check requested")
