from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Response model for the authenticate_user endpoint, which contains the access token on successful authentication.
    """

    token: str
    expires_in: int


class Settings(BaseModel):
    secret_key: str = "a_very_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = Settings()


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain-text password matches its hashed version.

    Args:
        plain_password: Plaintext password to verify.
        hashed_password: Hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates a user and returns an access token.

    Args:
        email (str): The email of the user trying to authenticate. This field can also be used for username in systems where email and username are interchangeable.
        password (str): The password of the user trying to authenticate. It will be compared against the hashed password stored in the database for validation.

    Returns:
        AuthenticateUserResponse: Response model for the authenticate_user endpoint, which contains the access token on successful authentication.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not await verify_password(password, user.password):
        raise Exception("Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token_expires = datetime.utcnow() + access_token_expires
    to_encode = {"exp": token_expires, "sub": str(user.id)}
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return AuthenticateUserResponse(
        token=token, expires_in=access_token_expires.total_seconds()
    )
