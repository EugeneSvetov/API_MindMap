import requests
import json
import base64


files = {"file": base64.b64encode(open('WIN.md', 'rb').read()).decode()}
r = requests.post('http://127.0.0.1:8000/', data=json.dumps(files))
print(r.json())