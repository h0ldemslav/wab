import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

def setup_auth(app: FastAPI):
    dotenv_path = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    MIDDLEWARE_SECRET_KEY = os.getenv("MIDDLEWARE_SECRET_KEY")

    config_data = {
        "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET
    }

    starlette_config = Config(environ=config_data)
    oauth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

    app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_SECRET_KEY)

    return oauth