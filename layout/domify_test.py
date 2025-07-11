from domify import html_elements as e
html = e.Html(lang="ja")
with html:
	with e.Head():
		e.Meta(charset='utf-8')
		e.Title("Domify testing")
	with e.Body():
		e.H1('<', e.B('Domify'), '>テスト用のホームページへようこそ!')
		e.P(e.B('Domify'), ' is an HTML builder library of ', e.B('Python'), ' scripting language.')
		with e.Select() as select:
			e.Option("Option 1", value=1)
print(html)