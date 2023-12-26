import htmlgenerator as hg
from htmlgenerator import mark_safe as safe
from htmlgenerator import render
import yaml

index_title = "トップページ Home"
slug_title = yaml.load("""
    blog: 日誌 
    news: お知らせ
    contact: 連絡先
    about: このサイトについて
    how-to-write: 書きかた
    usage-html-builder: HTMLビルダーの使いかた
 """, Loader=yaml.CLoader)

html = hg.BaseElement(
    safe("<!DOCTYPE html>"),
    hg.HTML(
        hg.HEAD(
            hg.TITLE(
                "{{ title }} - {{ subtitle }}",
            ),
            hg.META(charset="UTF-8"),
            hg.META(name="viewport", content="width=device-width, initial-scale=1.0"),
            hg.LINK(
                rel="stylesheet", type="text/css", href="{{ base_path }}/css/style.css"
            ),
        ),
        hg.BODY(
            hg.NAV(
                hg.SECTION(
                    hg.SPAN(
                        hg.A(
                            "\u30c8\u30c3\u30d7\u30da\u30fc\u30b8 ",
                            hg.SPAN("Home", lang="en"),
                            href="{{ base_path }}/",
                        ),
                        _class="home",
                    ),
                    hg.SPAN(
                        hg.A(
                            "\u65e5\u8a8c",
                            hg.SPAN("Blog", lang="en"),
                            href="{{ base_path }}/blog/",
                        ),
                        hg.A(
                            "\u304a\u77e5\u3089\u305b",
                            hg.SPAN("News", lang="en"),
                            href="{{ base_path }}/news/",
                        ),
                        hg.A(
                            "\u9023\u7d61\u5148",
                            hg.SPAN("Contact", lang="en"),
                            href="{{ base_path }}/contact/",
                        ),
                        hg.A(
                            "\u3053\u306e\u30b5\u30a4\u30c8\u306b\u3064\u3044\u3066",
                            hg.SPAN("About", lang="en"),
                            href="{{ base_path }}/about/",
                        ),
                        hg.A(
                            "\u66f8\u304d\u304b\u305f",
                            hg.SPAN("How to write", lang="en"),
                            href="{{ base_path }}/how-to-write/",
                        ),
                        hg.A(
                            "HTML\u30d3\u30eb\u30c0\u30fc\u306e\u4f7f\u3044\u304b\u305f",
                            hg.SPAN("How to use HTML builder", lang="en"),
                            href="{{ base_path }}/usage-html/",
                        ),
                        _class="links",
                    ),
                ),
            ),
            hg.MAIN(
                "\n{{ content }}\n",
            ),
            hg.FOOTER(
                hg.SECTION(
                    hg.P(
                        "\xa9 {{ current_year }} Yskz",
                    ),
                    hg.P(
                        hg.A(
                            hg.B(
                                "GitHub",
                            ),
                            " repository page",
                            href="https://github.com/Yasukazu/my-makesite",
                        ),
                    ),
                ),
            ),
            id="{{ slug }}",
        ),
    ),
)
