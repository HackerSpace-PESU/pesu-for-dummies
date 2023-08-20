import requests

page_code = '''---
order: -10
label: Contribute
---

# CONTRIBUTE
Found some mistakes in the pages, or want to contribute your own content to this guide? This project is open-source under PESU Hackerspace Club, and you can contribute to it through [this repository](https://github.com/HackerSpace-PESU/pesu-for-dummies)

<br><br>

## Guidelines
* Before starting to work on any changes, please ping SilicoFlare on the `#pesu-for-dummies` channel in the [HackerSpace Discord](https://hackerlinks.vercel.app/discord) because there are many local changes made and your changes could interfere with them.

* Make sure the information added is verified to be true by trusted sources, because several students refer to this guide for information.

<br><br>

## Stuff to add

'''

with open('tools/to_do_list.txt', 'r') as file:
    for ln in file.readlines():
        page_code += f"{ln}\n"

page_code += '''
<br><br>

## Contributors
'''

url = f'https://api.github.com/repos/HackerSpace-PESU/pesu-for-dummies/contributors'
response = requests.get(url)
contributors = response.json()

for cont in contributors:
    page_code += f'''<a href="{cont['html_url']}">
    <img src="{cont['avatar_url']}" alt="GitHub Avatar" width="50" height="50" style="border-radius: 50%">
</a>&emsp;\n
'''

with open('contributors.md', 'w') as file:
    file.write(page_code)
