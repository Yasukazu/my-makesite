from markupy.elements import *
from markupy import Fragment
from base_layout import BaseLayout

md_text = '''
## *PHP* との併用

 レンタルサーバーでウェブページを表示するのに, (*Python* を *CGI* で動かす方法に失敗したので), *PHP* から *Python* を外部プログラム実行により返される文字列を得る方式にしています。
'''
from markupy._private.html_to_markupy.parser import to_markupy

from markdown import markdown # just for an example

md_html = markdown(md_text)
md_py = to_markupy(md_html).split('\n')[2] #, no_import=True) # python code
md_comp = eval(md_py) # Component object
md_main = Div[md_comp] # wrap with 'Main' element

class IndexPage(BaseLayout):
    def render_main(self):
        return Fragment[P['このページは', B['HTML'], '文書を', B['Python'], 'スクリプト言語により生成する方法を試すために作りました。'],
            P['テンプレートで部分的に内容を追加する方法とは別のやり方です。'],
            P[I['Markupy'], 'という', B['Python'], 'のライブラリを試しています。'],
            md_main
            ]

if __name__ == '__main__':
    index_page = IndexPage()
    print(index_page)