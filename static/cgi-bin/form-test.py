<<<<<<< HEAD
#!/usr/bin/python3
=======
#!/usr/local/bin/python3
#/usr/bin/python
>>>>>>> ec372197f0c05bf5a91bb0127ca1429aa924f071
# -*- coding: utf-8 -*-
# Reference: https://qiita.com/TSKY/items/b041de0572e6586c889c
import cgi
import cgitb
cgitb.enable() # debug on
form = cgi.FieldStorage() # generate a cgi object
v1 = form.getfirst('value1') # name = value1
v2 = form.getfirst('value2') # name = value2

def times(a, b):
    """returns the culculated value"""
    try:
        a = float(a)
        b = float(b)
        return str(a * b)
    except ValueError:
        return('Value Error(>_<)')

# ブラウザに戻すHTMLのデータ
print("Content-Type: text/html")
print()
result = times(v1, v2)
htmlText = """
<!DOCTYPE html>
<html>
    <head><meta charset="utf-8" /></head>
<body bgcolor="lightyellow">
    <h1>Helo,</h1>
    <p>Multiplied value is: &nbsp; {}<br/></p>
    <hr/>
    <a href="/">Return to home</a>　
</body>
</html>
""".format(result)
#%(times(v1,v2)) # embed result at placeholder
print( htmlText) #.encode("cp932", 'ignore').decode('cp932') )
