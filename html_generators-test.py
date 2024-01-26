from pathlib import Path, PurePath
from typing import List
import html_generators as h
STATIC = 'css'
def my_static_file(s: str) -> str:
	EXT_DIR = {'.css': 'css', '.js': 'script', '.py': 'cgi-bin'}
	p = PurePath(s)
	ext = p.suffix.lower()
	dir = EXT_DIR[ext]
	return str(dir / p)
# A "page template"
def standard_page(title, *content, user=None, page_title=None):
	# h.Document just adds the DOCTYPE line
	return h.Document(
		# h.Title is just an HTML element
		# We have factories defined for all standard HTML elements
		h.Title(title),
		# Keyword arguments become element attributes
		h.Meta(charset='utf-8'),
		h.Link(href=my_static_file('site_styles.css')),
		# Setting an attribute to True will render it with no value
		h.Script(defer=True, src=my_static_file('site_script.js')),

		h.Nav(
			# Elements can have both content (positional args)
			# and attributes (keyword args)
			# At first, it looks odd that an element's attributes are listed 
			# after its content, but you get used to it quickly.
			# With decent syntax highlighting, the attributes stand out nicely
			h.A('Foo', href='/foo/'),
			h.A('Bar', href='/bar/'),

			# Any argument that is False or is None will be skipped.
			# This makes "conditional children" easy
			user and (
				h.A('My Profile', href='/profile/'),
				h.A('Log Out', href='/logout/'),
			)
		),

		h.Main(
			# If the user doesn't provide a custom page title,
			# generate one matching document title
			page_title or h.H1(title),

			content,
		),
	)

# A "chunk template"
class Book:
	def __init__(self, title: str, summary = '', published=False):
		self.title = title
		self.summary = summary
		self.published = published

def book_section(book: Book):
	return h.Section(
		h.H2(book.title),
		h.P(book.summary),
		# "class" is a reserved word in python, so add a trailing underscore
		# Trailing underscores are trimmed when converting to attribute names
		class_='book',
		# This will render a 'data-id' attribute
		# All underscores (other than trailing) will be converted to hyphens
		data_id=book.id,
	)
def get_user_books(user: str) -> List[Book]:
	return {
		'YM': [Book('Lost in Space', 'Science fiction drama of a family with an internal enemy'), Book('Johnny Got His Gun', 'Communication with Morse code in a situation without eyes, ears and hands ')]

	}[user]

# A particular page
def my_books_page(user: str):
	return standard_page(
		'My Books',
		h.P(h.A('Create new book', href='/books/add/')),
		# Join is not an element - it works like str.join
		# Here we're printing an <hr> between each book section
		h.Join(
			h.Hr(), 
			# This is a generator expression
			# We could also pass a list, but this reduces memory usage
			(
				book_section(book) for book in get_user_books(user)
				if book.published
			)
		),
	)

if __name__ == '__main__':
	my_page = my_books_page('YM')
	print(my_page)