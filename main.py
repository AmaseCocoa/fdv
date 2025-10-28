from apkit.config import AppConfig
from apkit.server import ActivityPubServer
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import endpoints

config = AppConfig()
app = ActivityPubServer()
templates = Jinja2Templates(directory="templates")

app.include_router(endpoints.router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request, "fdv_host": f"{request.url.scheme}://{request.url.hostname}{':' + str(request.url.port) if request.url.port != 80 and request.url.port != 443 else ''}"}
    return templates.TemplateResponse("index.html", context, headers={"Cache-Control": "max-age=604800, public"})