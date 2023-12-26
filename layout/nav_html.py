import htmlgenerator as hg
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
        text = v + ' ' + k.title().replace('-', ' ') # title() capitalizes the 1st char of every words
        yield hg.A(text, href="{{ base_path }}/%s/"%k)

content_obj = hg.BaseElement(
    hg.A(
        index_title,
        href="{{ base_path }}/",
       _class="home-link"),
    *[a for a in iter_a()]
    )

if __name__ == '__main__':
  #body_obj = hg.BODY(hg.NAV(content_obj), hg.MAIN("In main."))
  from htmlgenerator import render
  html = render(content_obj,{})
  print(html)