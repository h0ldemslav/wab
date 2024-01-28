from fastapi import Request
from models import GoogleToken

def get_google_token_from_cookie(request: Request, cookie_key: str = "google_token") -> GoogleToken | None:
    google_token_json = request.cookies.get(cookie_key)

    try:
        return GoogleToken.model_validate_json(google_token_json)
    except ValueError:
        return None