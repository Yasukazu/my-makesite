import codecs
import os
import re

import black  # type: ignore
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag  # type: ignore

# be aware: attributes with the empty string as value will be converted
# to empty attributes which is okay since it does not alter behaviour
# (https://html.spec.whatwg.org/multipage/syntax.html#attributes-2)

INDENT = "    "


def multiline(s):
    if '"""' not in s:
        if s.endswith('"'):
            s = s[:-1] + "\\" + s[-1]  # this will likely not work well...
        return f'"""{s}"""'
    if "'''" not in s:
        if s.endswith('"'):
            s = s[:-1] + "\\" + s[-1]  # this will likely not work well...
        return f"'''{s}'''"
    raise RuntimeError(
        f"""
The following string could not be escaped.
Please open an issue on https://github.com/basxsoftwareassociation/htmlgenerator/issues
{s}
"""
    )


def marksafestring(func):
    def wrapper(s):
        ret = func(s)
        if ret and len(ret) > 2 and any([c in ret[1:-1] for c in "&<>'\""]):
            return f"s({ret})"
        return ret

    return wrapper


@marksafestring
def escapestring(s):
    # s = s.replace("\\", "\\\\")  # escape backslashes
    s = codecs.encode(s, "unicode_escape").decode()
    if not s:
        return ""
    if "\n" in s:
        return multiline(s)
    if '"' not in s:
        return f'"{s}"'
    if "'" not in s:
        return f"'{s}'"
    return multiline(s)


def convert(tag, level, compact, parent=None):
    indent = INDENT * level
    if isinstance(tag, Doctype):
        return [indent + f's("<!DOCTYPE {tag}>")']
    elif isinstance(tag, Comment):
        if tag.strip() and not compact:
            ret = []
            for line in tag.splitlines():
                if line.split():
                    ret.append(indent + f"# {line}")
            return ret
        return []
    elif isinstance(tag, NavigableString):
        if parent and isinstance(parent, Tag):
            breakpoint()
        escaped = escapestring(tag)
        if escaped == '"\\n"':
            return []
        return [indent + escaped]
    elif isinstance(tag, Tag):
        ret = [indent + f"hg.{tag.name.upper()}("]
        attrs = []
        for key, value in tag.attrs.items():
            if isinstance(
                value, list
            ):  # for multivalued attributes, see beautifullsoup docs
                value = ' + " " + '.join(escapestring(v) for v in value)
            elif value == "":
                value = "True"
            else:
                value = escapestring(value)
            if key in (
                "class",
                "for",
                "async",
            ):  # handling reserved python keywords, see htmlgenerator docs
                key = "_" + key
            key = key.replace("-", "_")
            attrs.append(f"{key}={value}")
        for subtag in tag.children:
            subcontent = convert(subtag, level + 1, compact, parent=tag)
            if subcontent:
                if subcontent[-1].strip():
                    subcontent[-1] += ","
                ret.extend(subcontent)
        ret.append(indent + INDENT + ", ".join(attrs))

        ret.append(indent + ")")
        return ret
    else:
        raise RuntimeError(f"Unknown element type: {tag}")


def parsehtml2object(html):
    """
    Helper function to get directly a htmlgenerator.BaseElement back,
    should be rather slow
    """
    _locals = {}
    # should not be used in production, however the code should be escaped correctly
    exec(parsehtml(html, False, True), {}, _locals)  # nosec
    return _locals["html"]

def only_spcs(s: str):
    for c in s:
        if c not in {' ', '\n', '\t'}:
            return False
    return True

INDENT = 2
spc = ' '
INDENTS = INDENT * spc
def format_attrs(a: str, attrs: dict) -> str:
    return ('klass' if a == 'class' else a) + '="' + " ".join(attrs[a]) + '"'
from typing import Union
def do_with(subtag: Union[Tag, Comment, NavigableString], depth: int): # , outlist: list):
    print(depth * INDENTS, end='') # + "with tag("

    def do_text(txt: NavigableString):
        print(depth * INDENTS + f'text("{txt}")')

    def do_comment(cmt: Comment):
        print(depth * INDENTS + f'#{cmt}')

    def do_tag(tag: Tag, depth: int):
        code = "tag(" + f'"{tag.name}"'
        attrs = [format_attrs(a, tag.attrs) for a in tag.attrs] if tag.attrs else None
        params = ", ".join(attrs) if attrs else None
        if tag.children:
            children = [c for c in tag.children]
            if len(children) == 1 and isinstance(children[0], NavigableString):
                code = f'line("{tag.name}", "{children[0]}"' 
                code += params + ')' if params else ')'
                print(depth * INDENTS + code)
            else:
                print(depth * INDENTS + 'with ' + code + ":")
                for child in children:
                    do_with(child, depth + 1)
        else:
            print("doc.s" + code)

    if isinstance(subtag, Tag):
        do_tag(subtag, depth)
    elif isinstance(subtag, NavigableString):
        if not only_spcs(subtag):
            text = subtag
            pre = re.search(r'^[\n\s\t]+', text)
            if pre:
                text = subtag[len(pre[0]):]
            post = re.search(r'[\n\s\t]+$', text)
            if post:
                text = subtag[:len(post[0])]
            if text:
                do_text(text)
    else:
        do_comment(subtag)


def parsehtml(html: str, formatting, compact):
    out = [ "from yattag import Doc",
"doc, tag, text, line = Doc().ttl()" ]
    parser = "html.parser"
    soup = BeautifulSoup(html, parser)
    for subtag in soup.contents:
        indent = 0
        outlist = []
        do_with(subtag, indent)
    breakpoint()


    separator = " " if compact else "\n"
    htmlstr = separator.join(filter(lambda line: bool(line.strip()), out))
    if not formatting:
        return htmlstr
    return black.format_file_contents(htmlstr, fast=True, mode=black.FileMode())


def main():
    import sys

    formatflag = "--no-formatting"
    compactflag = "--compact"
    encodingflag = "--encoding"
    encoding = sys.getdefaultencoding()

    files = sys.argv[1:]
    formatting = formatflag not in files
    compact = compactflag in files
    if formatflag in files:
        files.remove(formatflag)
    if compactflag in files:
        files.remove(compactflag)
    if encodingflag in files:
        encoding = files[files.index(encodingflag) + 1]
        files.remove(encodingflag)
        files.remove(encoding)

    if not files:
        print(parsehtml(sys.stdin.read(), formatting, compact), end="")
    for _file in files:
        with open(_file, encoding=encoding) as rf:
            with open(_file + ".yat.py", "w") as wf:
                wf.write(parsehtml(rf.read(), formatting, compact))


if __name__ == "__main__":
    main()
