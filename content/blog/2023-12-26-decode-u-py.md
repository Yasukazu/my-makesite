## A Python script to decode unicode encoded text generated by `convertfromhtml` of <b>HTML Generator</b>

`convertfromhtml` generates Python script from HTML although it converts non-ascii characters into `\uxxxx` codes.

Countermeasure to convert using `codecs.decode`

```python
dcd = codecs.decode(txt, 'unicode-escape')
```
But, decoded non-ascii strings are added unwanted newlines and space chars in double quoted parts!
So, I wrote a Python script to remove such chars: `decode-u.py`
