from models.user import User
from database.db import db
from logger_config import get_logger

logger = get_logger(__name__)


class AuthService:
    """Signup / login using the User model and werkzeug password hashing."""

    def signup(self, data):
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        if not username or not password:
            raise ValueError('Username and password are required')

        if User.query.filter_by(username=username).first():
            raise ValueError('Username already taken')

        # User.name and email are required by the model. We derive sensible
        # placeholders from username so signup needs only username+password.
        user = User(
            name=data.get('name') or username,
            email=data.get('email') or f'{username}@example.com',
            username=username,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"Auth: user signed up - {username}")
        return user

    def authenticate(self, data):
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return None
        return user
