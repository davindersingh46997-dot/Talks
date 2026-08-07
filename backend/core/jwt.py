from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

SECRET_KEY = "your_super_secret_key_change_this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -------------------------------------------------------------------
# Create Access Token
# -------------------------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


# -------------------------------------------------------------------
# Decode Access Token
# -------------------------------------------------------------------

from jose import JWTError

def decode_access_token(token: str):

    print("=" * 60)
    print("SECRET_KEY:", SECRET_KEY)
    print("TOKEN:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        print("Decoded payload:", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR:", repr(e))
        return None