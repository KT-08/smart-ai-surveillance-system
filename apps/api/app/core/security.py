
from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
from jose import jwt, JWTError

from apps.api.app.core.config import settings


# -------------------------------
# Password Hashing (Argon2)
# -------------------------------

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure Argon2 hash.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Check whether the entered password matches the stored hash.
    """
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# -------------------------------
# JWT Authentication
# -------------------------------

ALGORITHM = "HS256"



def create_access_token(data: dict) -> str:
    """
    Generate a signed JWT access token.
    """

    to_encode = data.copy()

    if "exp" not in to_encode:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode["exp"] = expire

    encoded_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_token



def decode_access_token(token: str):
    """
    Verify a JWT token and return its payload.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None
