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

def render_a():
    """every double bracket becomes single"""
    list = []
    for k, v in slug_title.items():
        list.append(hg.A(v + ' ' + k, href="{{ base_path }}/%s/"%k))
    return list

class DoA:
  def __init__(self, given_render):
     self.given_render = given_render
  
  def render(self, params={}):
    """every double bracket becomes single"""
    for k, v in slug_title.items():
      yield  self.given_render(hg.A(v + ' ' + k, href="{{ base_path }}/%s/"%k), params)
# class version: fail: 

nav_obj = hg.NAV(
    hg.A(
        index_title,
        href="{{ base_path }}/",
        _class="home-link"),
        DoA(render)
        #*render_a()#(a for a in render_a({}))
    )
nav_txt = render(nav_obj,{})
print(nav_txt)