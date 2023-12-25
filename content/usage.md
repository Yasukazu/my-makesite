Difference from original makesite
---------------------------------

*   Originally, meta data (aka front matters) are set as comments of HTML.
*   In this fork, meta data in **markdown** files may be written in leading 3-hyphen separated part as YAML format(YAML format is like an intend format version JSON format). Like:
    
        ---
        title: a title of an article
        ---
      
    

Headings(H2, H3, ... H6)
------------------------

*   Headings start from **H2** tag since **H1** is set with _title_ metadeta in the front matter.

Template
--------