import aiohttp
from fastapi import FastAPI
import yake
from pydantic import BaseModel
import base64
from tools import read_md, make_json
import os

kw_extractor = yake.KeywordExtractor()


class Item(BaseModel):
    file: str


app = FastAPI()


async def translate(text):
    IAM_TOKEN = 't1.9euelZqckcuPncbNk5iUks2Wz47Hxu3rnpWaj5CZkorPip3Hzo-Zi8ady5zl8_duWFRd-e8GGgU5_N3z9y4HUl357wYaBTn8.A0pi5_nyoOrZ3Fg7NcOJjnfKVDNx_ck5TM9sEp6zPFBe6B8_gmSjPfCm8k_PQf42S2IlUle-AYhBnEYw_y9rBg'
    folder_id = 'b1gl6pn6u1gt8qocigvd'
    target_language = 'en'
    body = {
        "targetLanguageCode": target_language,
        "texts": [text],
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://translate.api.cloud.yandex.net/translate/v2/translate', json=body, headers=headers) as resp:
            a = await resp.json()
            return a['translations'][0]['text']


@app.post("/")
async def root(item: Item):
        return make_json(read_md(item.file))

