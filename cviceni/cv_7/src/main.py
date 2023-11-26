import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse('''
<body>
    <a href="/auth/login">Log In</a>
</body>'''
)

# @app.get("/token")
# async def token(request: Request):
#     return request.headers

# OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Set up OAuth
config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID, 
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET
}

from starlette.config import Config
starlette_config = Config(environ=config_data)

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

oauth = OAuth(starlette_config)
# Zaregistrujeme auth objekt, s nimz budeme pracovat, coz je OAuth. Plus, aby aplikace mohla pracovat s token
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Potrebujeme vytvorit session
from starlette.middleware.sessions import SessionMiddleware

# secrets.token_urlsafe - vygeneruje ti nahodny retezec; pozor: musis po kazde generovat novy!
# Jinak - Internal Server Error
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(30))

# Kliknu na login link v html, presmeruje se na tento endpoint a ja pak presmeruji na Google OAuth
# Budeme potrebovat Google credentials (secret key a client id, viz nahore, config_data)
@app.get("/auth/login")
async def login(request: Request):
    # Vracime si metodu od Google, pouzijeme ji a presmerujeme na stranku /token
    return await oauth.google.authorize_redirect(request, "http://localhost:8000/token")

@app.get("/token")
async def token(request: Request):
    # try:
    access_token = await oauth.google.authorize_access_token(request)
    #except OAuthError:
        # raise
    # print("access_token", access_token)

    # user_data = await oauth.google.parse_id_token(request, access_token)
    # print(user_data)

    # Vrati se ti JSON, v nemz jedna property, id_token, je prave hodnota JWT tokenu
    # Na webu https://jwt.io si muzes ten token overit, zda je validni (Signature Verified musi byt)
    # Pokud zmenis jeden znak, tak uz ten token neni validni
    return access_token