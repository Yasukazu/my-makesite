# -*- coding: utf-8 -*-
from markupy import Component, View
from markupy.elements import H1, Body, Footer, Head, Header, Html, Main, Title, B, Meta

LANG = 'ja'
global_href_dict = {'トップページ': 'home', 'このホームページについて': 'about'}

class BaseLayout(Component):
    def render_title(self) -> str:
        return "Markupy testing website"

    def render_main(self) -> View:
        return None

    def render(self) -> View:
        from navigation import Navigation
        return Html(lang=LANG)[
            Head[
                Meta(charset='utf-8'),
                Title[self.render_title()],
            ],
            Body[
                Header(".container")[
                    H1["Welcome to my ", B['markupy'], " testing website!"],
                    Navigation(global_href_dict, id='global-nav')
                ],
                Main(".container")[self.render_main()],
                Footer(".container")["© My Company"],
            ],
        ]

if __name__ == '__main__':
    base_layout = BaseLayout()
    print(base_layout)