from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(password):
    """Hash a plain text password."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(hashed_password, password):
    """Verify a password against its hash."""
    return bcrypt.check_password_hash(hashed_password, password)
