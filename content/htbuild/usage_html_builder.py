#import os
#import sys

#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import htbuilder as h
#from htmlBuilder.tags import *
#from htmlBuilder.attributes import Class, Id
#from simple import div, h1, h2, span, render, p, strong

title = "Front matter in HTML comment"
subtitle = "Front matter as markdown header i.e. YAML format part separated with 3 hyphens('---') before and after the header part"

content = h.div(_class='content')(
    h.h1(_id='title')(title),
    h.h2(_id='subtitle')(subtitle),
       h.h3(_class='item')("Difference from original",
        h.b("makesite")),
         h.ul(_class='diff')(
           h.li("Originally, meta data (aka front matters) are set as comments of HTML."),
           h.li("In this fork, meta data are written in leading 3-hyphen separated part as YAML format(YAML format is like a simplified JSON format).")
         ),

        h.h3("Notice:"),
        h.ul(
            h.li("Headings start from H2 aka double crosshatches Since H1 is set with `title` in the front matter.")
          )
    )
#html = render(node)
#print(html)