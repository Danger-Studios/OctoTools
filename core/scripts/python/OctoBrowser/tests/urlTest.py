

import requests
import shutil
url = 'https://octoboards.danger.studio/?controller=FileViewerController&action=image&task_id=19&file_id=2'
filename = "ass.png"


r = requests.get(url, stream=True)
if r.status_code == 200:
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)


import requests
import re


weburl = (
    "https://octoboards.danger.studio/?controller=FileViewerController&action=image&task_id=19&file_id=2"
)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
response = requests.get(weburl, verify=False, headers=headers)

source = response.content.decode("utf-8")

imagen_eco = re.search("imagen_eco((.*?));", source)
if not imagen_eco:
    exit("Not found")

image_name = re.search(r"([\w-]+)\.png", imagen_eco.group(0))
if not image_name:
    exit("Not found")
print(image_name.group(0))
print(
    f"https://octoboards.danger.studio/?controller=FileViewerController&action=image&task_id=19&file_id=2{image_name.group(0)}"
)