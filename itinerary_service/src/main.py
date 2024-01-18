from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
auth_service_url = "http://127.0.0.1:8001" 

@app.get("/")
async def root():
    return HTMLResponse(f'''<a href="{auth_service_url}/login">Log In</a>''')