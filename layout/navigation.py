from markupy.elements import Nav, Ul, Li, A
from markupy import Component, View

class Navigation(Component):
    def __init__(self, name_to_path: dict[str, str], id: str='nav') -> None:
        super().__init__()
        self.id = id
        self.name_to_path = name_to_path

    def render(self) -> View:
        return Nav(".header", id=self.id)[#self.render_content()]
            Ul(".nav")[
                (Li[A(href=f'/{v}')[k.strip('/')]] for k, v in self.name_to_path.items())
            ]
        ]

if __name__ == '__main__':
    from markupy.elements import A

    global_href_dict = {'Home': 'home', 'About us': 'about'}
    global_navigation = Navigation(global_href_dict, id='global-nav')

    print(global_navigation)

