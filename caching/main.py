from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import requests
import requests_cache

# create our app and setup the "Patching" cache, for ALL requests
app = FastAPI()
requests_cache.install_cache("charactercache", backend="sqlite")
templates = Jinja2Templates(directory="templates")


# form template index.html 
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#same template used here but a post request and request to the external API
@app.post("/", response_class=HTMLResponse)
async def char_id_get(request: Request, char_id: int = Form()):
    resp = requests.get("https://rickandmortyapi.com/api/character/" + str(char_id))

    # whats in the cache?
    print(requests_cache.get_cache())
    print("Cached URLS:")
    print("\n".join(requests_cache.get_cache().urls))
    char_name = resp.json().get("name")
    return templates.TemplateResponse(
        "index.html", {"request": request, "char_name": char_name}
    )
