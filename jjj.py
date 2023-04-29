import aspose.words as aw
from tools import *
from bs4 import BeautifulSoup as bs

doc = aw.Document("qwe (1).docx")
doc.save("Output.md")

with open("Output.md", 'r', encoding='utf-8') as file1:
    with HTMLRenderer() as renderer:
        doc = Document(file1)
        rendered = renderer.render(doc)
        lst = parseList(bs(rendered, 'lxml').ul)
        # lst = str(lst).replace("(", "[").replace(')', ']')
        # lst = eval(lst)
        print(lst)