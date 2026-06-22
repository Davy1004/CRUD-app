from flask import Blueprint, jsonify, request, session
from services.auth_service import AuthService
from logger_config import get_logger

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
logger = get_logger(__name__)


@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() or {}
        user = auth_service.signup(data)
        session['username'] = user.username
        return jsonify({
            'message': 'Signup successful',
            'username': user.username
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        user = auth_service.authenticate(data)
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        session['username'] = user.username
        return jsonify({
            'message': 'Login successful',
            'username': user.username
        }), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/auth/me', methods=['GET'])
def me():
    """Lets the frontend check login status on page load."""
    username = session.get('username')
    if not username:
        return jsonify({'logged_in': False}), 200
    return jsonify({'logged_in': True, 'username': username}), 200
