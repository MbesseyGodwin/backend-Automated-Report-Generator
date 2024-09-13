import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def generate_jwt_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({"sub": user_id, "exp": expiration}, SECRET_KEY, algorithm="HS256")
