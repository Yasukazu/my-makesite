import pyhtml as h
#from pyhtml import *
meta = { 'title' : "How to write",
     'subtitle' : "Contents format" }
html = h.html(
      h.body(
        h.h2("Difference from original makesite"),
        h.ul(
            h.li("Originally, meta data <front matters> are set as comments of HTML."),
            h.li("In this fork, meta data in **markdown** files may be written in leading 3-hyphen separated part as YAML format(YAML format is like an intend format version JSON format). Like:")
        ),
        h.pre(
        """
        ---
        title: a title of an article
        ---
        """),
        h.h2("Headings(H2, H3, ... H6)"),
        h.ul(
            h.li("Headings start from", h.b("H2"), "tag since", h.b("H1"), "is set with _title_ metadeta in the front matter.")
        ),
        h.h2("Template")
      )
)
output = html.render()
print(output)