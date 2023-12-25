import htmlgenerator as hg
from htmlgenerator import mark_safe as safe
from htmlgenerator import render
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
if __name__ == '__main__':
  content_txt = render(content_obj,{})
  print(content_txt)