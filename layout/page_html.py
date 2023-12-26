import htmlgenerator as hg
from htmlgenerator import mark_safe as safe
from htmlgenerator import render

import os
cwd = os.getcwd()
import sys
sys.path.insert(0, cwd) # append
# from module_util import imp_mod_fm_file_loc
import layout.body_html as body_mod
# body_mod = imp_mod_fm_file_loc('body_html', 'layout/body_html.py')

content_obj = hg.BaseElement(
    safe("<!DOCTYPE html>"),
    hg.HTML(
        hg.HEAD(
            hg.TITLE(
                "{{ title }} - {{ subtitle }}",
            ),
            hg.META(charset="UTF-8"),
            hg.META(name="viewport", content="width=device-width, initial-scale=1.0"),
            hg.META(name="description", content="makesite.py with HTML Generator test site"),
            hg.LINK(
                rel="stylesheet", type="text/css", href="{{ base_path }}/css/style.css"
            ),
        ),
        hg.BODY(body_mod.content_obj)
        # id="{{ slug }}"
    )
)

if __name__ == '__main__':
  from htmlgenerator import render
  content_txt = render(content_obj,{})
  print(content_txt)