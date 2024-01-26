from pydantic import BaseModel

class UserInfo(BaseModel):
    email: str
    name: str

class GoogleToken(BaseModel):
    access_token: str
    token_type: str
    id_token: str
    expires_at: int
    userinfo: UserInfo