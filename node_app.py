import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


def get_node_id() -> str:
    """
    Returns node identifier from env.

    Example: NODE_ID=1 => "1"
    """

    node_id = os.getenv("NODE_ID")
    return node_id.strip() if node_id else "?"


@app.get("/", response_class=HTMLResponse)
def index():
    node_id = get_node_id()
    return HTMLResponse(
        f"""<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Node</title>
  </head>
  <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 60px;">
    <h1>Нода {node_id}</h1>
  </body>
</html>"""
    )


@app.get("/health")
def health():
    return {"status": "ok", "node_id": get_node_id()}

