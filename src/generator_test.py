import htmlgenerator as hg

head = hg.HEAD(
    hg.META(charset='utf-8'),
	hg.LINK(href='site_styles.css'),
    hg.TITLE("A test page for <",
             hg.B('HTML Generator'),
             ">")
)
my_page = hg.HTML(head, hg.BODY(hg.H1("It works!")))

print(hg.render(my_page, {}))