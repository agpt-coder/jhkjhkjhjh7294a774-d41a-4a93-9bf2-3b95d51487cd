from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    """
    Response model providing a new access token.
    """

    access_token: str
    token_type: str
    expires_in: int


async def refresh_token(refresh_token: str) -> AccessTokenResponse:
    """
    Refreshes an access token using a refresh token.

    Args:
        refresh_token (str): The refresh token provided by the user for renewing their access token.

    Returns:
        AccessTokenResponse: Response model providing a new access token.
    """
    new_access_token = "newlyGeneratedAccessToken"
    token_type = "Bearer"
    expires_in = 3600
    return AccessTokenResponse(
        access_token=new_access_token, token_type=token_type, expires_in=expires_in
    )
