from models import GoogleToken

def get_google_token_from_json(json: str) -> GoogleToken | None:
    try:
        return GoogleToken.model_validate_json(json)
    except ValueError:
        return None