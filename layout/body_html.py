import htmlgenerator as hg
from htmlgenerator import mark_safe
import os
cwd = os.getcwd()
import sys
sys.path.insert(0, cwd) # append
# from module_util import imp_mod_fm_file_loc
import layout.nav_html as nav_mod
# nav_mod = imp_mod_fm_file_loc('nav_html', 'layout/nav_html.py')
content_obj = hg.BODY(
        nav_mod.content_obj,
        hg.MAIN(
            "\n{{ content }}\n",
        ),
        hg.FOOTER(
            hg.P(
              mark_safe("&copy;"),
              "{{ current_year }} Yskz", #"\xa9
            ),
            hg.P(
                hg.A(
                    hg.B(
                        "GitHub",
                    ),
                    " repository page",
                    href="https://github.com/Yasukazu/my-makesite",
                ),
            ),
        ),
        id="{{ slug }}",
)

if __name__ == '__main__':
  from htmlgenerator import render
  content_txt = render(content_obj,{})
  print(content_txt)