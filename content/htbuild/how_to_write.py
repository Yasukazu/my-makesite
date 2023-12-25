#import htbuilder as h
from htbuilder import main, h1, h2, ul, li, pre, b
#from pyhtml import *
import datetime
date = datetime.date.fromisoformat("2023-12-25")
tag = main(
    h1("Formats of documents"),
        h2("Difference from original makesite"),
        ul(
            li("Originally, meta data <front matters> are set as comments of HTML."),
            li("In this fork, meta data in **markdown** files may be written in leading 3-hyphen separated part as YAML format(YAML format is like an intend format version JSON format). Like:")
        ),
        pre(
        """
        ---
        title: a title of an article
        ---
        """),
        h2("Headings(H2, H3, ... H6)"),
        ul(
            li("Headings start from", b("H2"), "tag since", b("H1"), "is set with _title_ metadeta in the front matter.")
        ),
        h2("Template")
      )
#output = html.render()
#print(output)