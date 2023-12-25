---
title: Trial of HTML builder Python libraries
---
## Current status

Using `htmlgenerator` in _PyPi_ [html generator in pypi](https://pypi.org/project/htmlgenerator/).

## Causes of choice:

### HTML to script converter

Needs `pip install htmlgenerator[all]` for `convertfromhtml filename.html`

### Iteration of tag objects was successfull althoug it uses all-capitalized HTML tags.

- Make an iterator function to yield tag objects then call the iterator in the outside tag with exploded list comprehension

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

### Import enclosing HTML tag object

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