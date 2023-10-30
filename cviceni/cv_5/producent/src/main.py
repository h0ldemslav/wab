from fastapi import FastAPI
from .rabbitmq import publish
from logging import basicConfig

basicConfig(
    filename="logFile.txt",
    filemode="a",
    format="%(arctime)s %(levelname)s-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI()



@app.get("/")
def read_root(name: str = "World"):
    msg = f"Hello {name}"
    publish(msg)
    return msg

