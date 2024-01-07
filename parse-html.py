# import requests
import html5lib
from domonic.ext.html5lib_ import getTreeBuilder


# r = requests.get("http://localhost:8000")
import sys
from pathlib import Path
ifile = Path('/home/yasukazu/make-site/content/contact.html')
if not ifile.exists():
    print(f"No file: {ifile}")
    sys.exit(1)
html = ''
with ifile.open('r') as rf:
    html = rf.read()

parser = html5lib.HTMLParser(tree=getTreeBuilder())
page = parser.parse(html) # r.content.decode("utf-8"))

# print the page with formatting
# print(f'{page}')

'''
links = page.getElementsByTagName('a')
for l in links:
    try:
        print(l.href)
    except Exception as e:
        # no href on this tag
        pass
'''

# turn the downloaded site into .pyml ;)
print(page.__pyml__())