#import os
#import sys

#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Id
#from simple import div, h1, h2, span, render, p, strong

title = "Front matter in HTML comment"
subtitle = "Front matter as markdown header i.e. YAML format part separated with 3 hyphens('---') before and after the header part"

body = Body(
    H1([Id('title')], title),
    H2([Id('subtitle')], subtitle),
       H3([Class('item')], "Difference from original",
        Strong("makesite")),
         Ul([Class('diff')],
           Li("Originally, meta data (aka front matters) are set as comments of HTML."),
           Li("In this fork, meta data are written in leading 3-hyphen separated part as YAML format(YAML format is like a simplified JSON format).")
         ),

        H3("Notice:"),
        Ul(
            Li("Headings start from H2 aka double crosshatches Since H1 is set with `title` in the front matter.")
          )
    )
#html = render(node)
#print(html)