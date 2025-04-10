from fastapi import FastAPI,Path,Query,HTTPException,status
import uvicorn
from bs4 import BeautifulSoup
import re 
from aiohttp import ClientSession
import asyncio
from requests_html import HTMLSession,AsyncHTMLSession
import requests

app = FastAPI()

@app.get("/find/{tag}")
def find_text(
    tag: str = Path(..., description="p"),
    url: str = Query(..., description="https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0"),
    text: str = Query(..., description="Украї́на (МФА: [ʊkrɐˈjinɐ]ⓘ) — держава у Східній та")
):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Не вдалося завантажити сторінку")

    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(tag)

    for element in elements:
      if re.search(text, element.get_text()):
        return {"found": element.get_text(strip=True)}

    raise HTTPException(status_code=404, detail="Текст не знайдено")



