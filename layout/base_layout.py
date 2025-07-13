# -*- coding: utf-8 -*-
from typing import Sequence
from dataclasses import dataclass
from markupy import Component, View
from markupy.elements import H1, Body, Footer, Head, Header, Html, Main, Title, B, Meta, P, I, Base
from markupy import Fragment

from navig import Navig

class BaseLayout(Component):
    LANG = 'ja'
    global_href_dict = {'トップページ': 'home', 'このホームページについて': 'about'}

    def __init__(self, main: View = Fragment[
        P['このウエブサイト（ホームページ）は', B['HTML'], '文書を', B['Python'], 'スクリプト言語から生成（変換)して作ってあります。'],
        P['テンプレート方式(',B['HTML'],'を基に部分的に内容を追加する)とは別のやり方です。'],
        P[I['Markupy'], 'という', B['Python'], 'のライブラリを利用しています。']]):
        super().__init__()
        self.main = main

    def render_title(self) -> str:
        return "Markupy testing website"

    def render_main(self) -> View:
        return self.main

    def render(self) -> View:
        return Html(lang=self.LANG)[
            Head[
                Meta(charset='utf-8'),
                Title[self.render_title()],
                Base(target="_blank"), # Open link as a new tab
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            ],
            Body[
                Header(".container")[
                    H1["私の", B['Markupy'], "テスト用のホームページにようこそ！"],
                    Navig(self.global_href_dict, id='global-nav')
                ],
                Main(".container")[self.render_main()],
                Footer(".container")["© My Company"],
            ],
        ]

if __name__ == '__main__':
    from logging import getLogger, INFO
    logger = getLogger(__file__)
    from markupy.elements import P, I
    from sys import argv, stdin, stdout
    from codecs import getreader, getwriter
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pos_arg", nargs="?")
    parser.add_argument("--encoding", help="encoding like utf-8, euc-jp, sjis, cp932", default='utf8') #parserに引数を追加
    parser.add_argument("--output-to", help="output file", default='--') #parserに引数を追加
    args = parser.parse_args()
    arg = None
    if not stdin.isatty():
        stdin = getreader(args.encoding)(stdin)
        arg = stdin.read() #.decode(args.encoding) # if not stdin.isatty() else None #len(argv)>1 and argv[1] == '--' else None
    elif args.pos_arg:
        arg = open(args.pos_arg, encoding=args.encoding).read()
        logger.info("%s is opened as encoding=%s", args.pos_arg, args.encoding)
    index_page = BaseLayout(eval(arg)) if arg else BaseLayout()
    #import sys, codecs
    # if args.encoding: stdout = getwriter(encoding=args.encoding)(stdout)
    if args.output_to == '--':
        print(index_page)
    else:
        with open(args.output_to, 'w', encoding=args.encoding) as out:
            out.write(str(index_page)) #).encode('cp932', 'strict')) #ing=args.encoding)