from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from json import JSONDecodeError

app = FastAPI()
api_gateway_urls = {
    "base": "http://127.0.0.1:8000",
    "home": "http://127.0.0.1:8000/home",
    "process_token": "http://127.0.0.1:8000/process_token"
}
auth_service_urls = {
    "base": "http://127.0.0.1:8001",
    "login": "http://127.0.0.1:8001/login"
}
auth_data = {}

@app.get("/")
async def root():
    return HTMLResponse(f'''<a href="{auth_service_urls["login"]}">Log In</a>''')

@app.get("/home")
async def home():
    if "id_token" not in auth_data.keys():
        return RedirectResponse(url=api_gateway_urls["base"])

    return HTMLResponse(f'''
        <h1>Simple Travel Itinerary</h1>
        <ul>
            <li><a href="#">Travel plans</a></li>
            <li><a href="#">Profile</a></li>
        </ul>
    ''')

@app.post(
    path="/process_token", 
    include_in_schema=False
)
async def process_token(request: Request):
    try:
        token_data = await request.json()
        auth_data.update(token_data)
    except JSONDecodeError:
        raise HTTPException(status_code=401, detail="Cannot process token")