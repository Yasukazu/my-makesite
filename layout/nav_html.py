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

def iter_a():
    for k, v in slug_title.items():
        yield hg.A(v + ' ' + k, href="{{ base_path }}/%s/"%k)

content_obj = hg.NAV(
    hg.A(
        index_title,
        href="{{ base_path }}/",
       _class="home-link"),
    *[a for a in iter_a()]
    )

if __name__ == '__main__':
  body_obj = hg.BODY(content_obj, hg.MAIN("In main."))
  body_txt = render(body_obj,{})
  print(body_txt)