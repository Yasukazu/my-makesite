---
title: Trying HTML builders for Python :HTMLビルダーを試している
---
## Current status 状況

Using `htmlgenerator` in _PyPi_ [HTML Generator in PyPi](https://pypi.org/project/htmlgenerator/).

## Causes of choice :選んだ理由

### Comes with a (HTML to script) reverse converter :逆変換機が付属する

 - Needs `pip install htmlgenerator[all]` to execute `convertfromhtml filename.html`
 - Generated Python script name is like: `*.html.py`. Rename it as `*_html.py` for use of python module.

### Iteration of tag objects was successfull :繰り返しによるタグの挿入ができる

- Make an iterator function to yield tag objects then call the iterator in the outside tag with exploded list comprehension :コルーチンとリスト内包表記

```python
def iter_a():
    for k, v in slug_title.items():
        yield hg.A(v + ' ' + k, href="{{ base_path }}/%s/"%k)

content_obj = hg.NAV(
    hg.A(
        index_title,
        href="{{ base_path }}/",
       _class="home-link"),
    *[a for a in iter_a()]
    )
```

### Import HTML tag object `content_obj` assigned in the imported module: 他のスクリプトで定義されたタグオブジェクトを取り込む 

```python
import htmlgenerator as hg
import os
cwd = os.getcwd()
import sys
sys.path.append(cwd)
from module_util import imp_mod_fm_file_loc
nav_mod = imp_mod_fm_file_loc('nav_html', 'layout/nav_html.py')
content_obj = hg.BODY(
    nav_mod.content_obj,
    "{{ content }}"
    )
```