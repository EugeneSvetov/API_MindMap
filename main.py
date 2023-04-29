import aiohttp
from fastapi import FastAPI
import yake
from pydantic import BaseModel
from tools import read_md, make_json

kw_extractor = yake.KeywordExtractor()


class Item(BaseModel):
    file: str


app = FastAPI()


@app.post("/")
async def root(item: Item):
    return make_json(read_md(item.file))
