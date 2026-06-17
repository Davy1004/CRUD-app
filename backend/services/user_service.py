from models.user import User
from database.db import db
from logger_config import get_logger
import re

logger = get_logger(__name__)


class UserService:
    """Service class for user CRUD operations"""

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def create_user(self, data):
        """Create a new user"""
        logger.debug(f"Service: Creating user with data: {data}")

        # Validate required fields
        if not data.get('name') or not data.get('email'):
            logger.warning(
                "Service: Missing required fields for user creation")
            raise ValueError('Name and email are required')

        # Validate email format
        if not self.validate_email(data['email']):
            logger.warning(f"Service: Invalid email format: {data['email']}")
            raise ValueError('Invalid email format')

        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            logger.warning(f"Service: Email already exists: {data['email']}")
            raise ValueError('Email already exists')

        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )

        db.session.add(user)
        db.session.commit()
        logger.info(
            f"Service: User created successfully - ID: {user.id}, Email: {user.email}")
        return user

    def get_all_users(self):
        """Get all users"""
        logger.debug("Service: Fetching all users")
        users = User.query.all()
        logger.debug(f"Service: Found {len(users)} users")
        return users

    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        logger.debug(f"Service: Fetching user by ID: {user_id}")
        user = User.query.get(user_id)
        if user:
            logger.debug(f"Service: User found - {user.email}")
        else:
            logger.debug(f"Service: User not found - ID: {user_id}")
        return user

    def get_user_by_email(self, email):
        """Get a user by email"""
        logger.debug(f"Service: Fetching user by email: {email}")
        return User.query.filter_by(email=email).first()

    def update_user(self, user_id, data):
        """Update a user"""
        logger.debug(f"Service: Updating user - ID: {user_id}")
        user = User.query.get(user_id)
        if not user:
            logger.warning(
                f"Service: User not found for update - ID: {user_id}")
            return None

        # Update fields if provided
        if 'name' in data:
            logger.debug(f"Service: Updating name for user {user_id}")
            user.name = data['name']

        if 'email' in data:
            # Validate email format
            if not self.validate_email(data['email']):
                logger.warning(
                    f"Service: Invalid email format for update: {data['email']}")
                raise ValueError('Invalid email format')

            # Check if email is already used by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                logger.warning(
                    f"Service: Email already exists: {data['email']}")
                raise ValueError('Email already exists')

            logger.debug(
                f"Service: Updating email for user {user_id} to {data['email']}")
            user.email = data['email']

        if 'phone' in data:
            logger.debug(f"Service: Updating phone for user {user_id}")
            user.phone = data['phone']

        if 'address' in data:
            logger.debug(f"Service: Updating address for user {user_id}")
            user.address = data['address']

        db.session.commit()
        logger.info(f"Service: User updated successfully - ID: {user_id}")
        return user

    def delete_user(self, user_id):
        """Delete a user"""
        logger.debug(f"Service: Deleting user - ID: {user_id}")
        user = User.query.get(user_id)
        if not user:
            logger.warning(
                f"Service: User not found for deletion - ID: {user_id}")
            return False

        db.session.delete(user)
        db.session.commit()
        logger.info(f"Service: User deleted successfully - ID: {user_id}")
