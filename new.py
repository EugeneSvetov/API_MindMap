import json
import zipfile
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as bs
from mistletoe import Document, HTMLRenderer
import yake

kw_extractor = yake.KeywordExtractor()


def format_list(lst):
    max_depth = 0
    for item in lst:
        if isinstance(item, list):
            depth = format_list(item)
            if depth > max_depth:
                max_depth = depth
    for i, item in enumerate(lst):
        if isinstance(item, str):
            if max_depth == 0:
                lst[i] = [it[0] for it in kw_extractor.extract_keywords(lst[i])[:5]]
            else:
                print(kw_extractor.extract_keywords(lst[i]))
                print(lst[i])
                lst[i] = kw_extractor.extract_keywords(lst[i])[0][0]

    return max_depth + 1


def translate(text, lang='en'):
    IAM_TOKEN = 't1.9euelZqMycmKkI6ans7NksyQl4-Oy-3rnpWaj5CZkorPip3Hzo-Zi8ady5zl8_cHaE5d-e8ifmhu_N3z90cWTF357yJ-aG78.aaM4NmCCK9fvSI6UlMS_XcZsPIpdqKOJRDXyIjGPydK8GzQxIsFivSO0xChME6fCwX4C4zSzvzq1tQO9kmr0AA'
    folder_id = 'b1gl6pn6u1gt8qocigvd'
    target_language = lang
    body = {
        "targetLanguageCode": target_language,
        "texts": [text],
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    rest = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate', json=body, headers=headers).json()
    return rest['translations'][0]['text']


def parseList(tag):
    if tag.name == 'ul':
        return [parseList(item)
                for item in tag.findAll('li', recursive=False)]
    elif tag.name == 'li':
        if tag.ul is None:
            return tag.text
        else:
            return (tag.contents[0].string.strip(), parseList(tag.ul))


def read_md(file):
    with open(file, 'r') as file1:
        file1 = translate(file1.read())
        print(file1)
        with HTMLRenderer() as renderer:
            doc = Document(file1)
            rendered = renderer.render(doc)
            lst = parseList(bs(rendered, 'lxml').ul)
            lst = str(lst).replace("(", "[").replace(')', ']')
            lst = eval(lst)
            format_list(lst)
            print(lst)
            return lst


def make_json(lst):
    themes = []
    for i, l in enumerate(lst):
        theme = {"name": l[0], "nested_nodes": []}
        if isinstance(l[1], list):
            for j, n in enumerate(l[1]):
                if isinstance(n, list):
                    print(translate(n, lang='ru'))
                    nested_node = {"name": translate(n, lang='ru'), "nested_nodes": [translate(n[1][0], lang='ru')]}
                else:
                    nested_node = {"name": translate(n, lang='ru'), "nested_nodes": []}
                theme["nested_nodes"].append(nested_node)
        themes.append(theme)
    return json.dumps({"root": "example", "themes": themes}, ensure_ascii=False)


print(make_json(read_md('WIN (2).md')))
