import codecs
import os
import io
import re
import sys
from typing import List, Union, Tuple

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

class IndentStr:
    def __init__(self, s: str, indent: int=0, end: str=''):
        self.indent = indent
        self.s = s
        self.end = end

def join_ist(lt: List[Tuple[int, str]]) -> List[str]:
    ss = []
    for s in lt:
        ns = ' ' * s[0] + s[1] # + s.end
        ss.append(ns)
    return ss

INDENT = 2
spc = ' '
INDENTS = INDENT * spc


def do_with(do_list: List[Tuple[int, str]],
        subtag: Union[Tag, Comment, NavigableString], depth: int, indent=INDENT) -> None:

    def nprint(d: int, s: str, end='\n'):
        do_list.append((d * indent, s)) # , end)

    STN = ' \t\n'
    def do_text(tx: NavigableString, d: int):
        tx = tx.strip(STN).lstrip(STN)
        if not tx:
            return
        for t in tx.split('\n'):
            t = t.strip(STN).lstrip(STN)
            if t:
                nprint(d, f'text("{t}")', end='\n')

    def do_comment(tx: Comment, d: int):
        tx = tx.strip('\n').lstrip('\n')
        if not tx:
            return
        if tx.find('\n') >= 0: # multi line
            nprint(d, "'''Comment: ", end='')
            for t in tx.split('\n'):
                nprint(d, t)
            nprint(d, 3 * "'")
        else:
                nprint(d, f'# {tx}')

    DQT = '"'
    SQT = "'"

    def do_tag(tag: Tag, depth: int):
        attrs = [format_attrs(a, tag.attrs) for a in tag.attrs] if tag.attrs else None
        params = ", ".join(attrs) if attrs else None
        children = [c for c in tag.children]
        if len(children) == 0:
            code = f'doc.stag("{tag.name}"' + f', {params})' if params else ')'
            nprint(depth, code)
        elif len(children) == 1 and isinstance(children[0], NavigableString):
            code = f'line("{tag.name}", '
            code_end = f', {params})' if params else ')'
            child = children[0].lstrip('\n').strip('\n')
            if child.find('\n') > 0:
                cc = child.split('\n')
                code += 3 * SQT
                nprint(depth, code)
                for i, c in enumerate(cc):
                    if i == len(cc) - 1:
                        break
                    nprint(0, c)
                nprint(0, c + 3 * SQT + code_end)
            else:
                nprint(depth, code + f'"{child}"' + code_end)
        else:
            code = f'with tag("{tag.name}"'
            code += ', ' + params + '):' if params else '):'
            nprint(depth, code)
            for child in children:
                do_with(do_list, child, depth + 1)


    def format_attrs(a: str, attrs: dict) -> str:
        aa = attrs[a]
        if isinstance(aa, list):
            aa = ' '.join(aa)
        return f'("{a}", "{aa}")' #('klass' if a == 'class' else a) + f'="{aa}"'


    if isinstance(subtag, NavigableString) and only_spcs(subtag):
            return []
    # print(depth * INDENTS, end='') # + "with tag("
    if isinstance(subtag, Tag):
        do_tag(subtag, depth)
    elif isinstance(subtag, Comment):
        do_comment(subtag, depth)
    elif isinstance(subtag, NavigableString):
        do_text(subtag, depth)
    else: 
        raise ValueError("Unknown type:" + type(subtag))


def parsehtml(html: str, formatting, compact, tag) -> List[str]:
    parser = "html.parser"
    soup = BeautifulSoup(html, parser)
    main_tag = soup.find(tag) if tag else None
    contents = main_tag or soup.contents
    taglist: Tuple[int, str] = []
    for subtag in contents:
        if isinstance(subtag, NavigableString):
            if only_spcs(subtag):
                continue
        indent = 0
        tags = []
        do_with(tags, subtag, indent)
        if len(tags) > 0:
            taglist += tags
    # print("html = doc.getvalue()", file=out)
    return join_ist(taglist)

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        prog='Yattag Python code generator',
        description='Generates Yattag Python code from HTML',
        epilog='by Y.M 2024')
    parser.add_argument('-f', "--formatting") # formatflag 
    parser.add_argument('-c', "--compact") # compactflag 
    parser.add_argument('-t', '--tag') # extract a tag
    parser.add_argument('-e', "--encoding") # encodingflag 
    parser.add_argument("files", nargs='*')

    args = parser.parse_args()

    encoding = args.encoding or sys.getdefaultencoding()
    files = args.files # sys.argv[1:]
    formatting = args.formatting # formatflag not in files
    compact = args.compact # compactflag in files
    tag = args.tag # extract a tag

    if not files:
        ss = parsehtml(sys.stdin.read(), formatting, compact)
        print('\n'.join(ss))
    else:
        for _file in files:
            _rf = Path(_file)
            if not _rf.exists():
                print(f"{_rf} does not exist!")
                continue
            with _rf.open('r') as rf:
                _path, file = os.path.split(_file)
                node, ext = os.path.splitext(file)
                if ext.lower() not in {'.html', '.htm'}:
                    continue
                new_node = node.replace('.', '_') # periods in filename(without extension) are replaced with underscores
                path = Path(_path)
                new_file = path / Path(new_node + '.py')
                exx = True
                if new_file.exists():
                    yn = input(f"{new_file} exists. Replace?(yes/no):")
                    if yn.lower() != 'yes':
                        exx = False
                if exx:
                    with new_file.open('w+', encoding=encoding) as wf:
                        wf.write("from yattag import Doc\n")
                        wf.write("doc, tag, text, line = Doc().ttl()\n")
                        ss = parsehtml(rf.read(), formatting, compact, tag)
                        wf.write('\n'.join(ss))
                        wf.write('\n')


if __name__ == "__main__":
    main()
