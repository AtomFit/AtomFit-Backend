from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenPairSchema(AccessToken, RefreshToken):
    token_transport: str = "cookies"
