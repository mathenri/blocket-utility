import argparse
import urllib.request
import bs4

# default args
DEFAULT_SEARCH_WORD = 'volvo'
DEFAULT_AREA = 'goteborg'

URL = 'https://www.blocket.se/goteborg?ca=15'
OUTPUT_FILEPATH = './output.txt'
DIV_ELEMENT_TAG = 'div'
LIST_ITEM_CLASS = 'media-body desc'

def _setup_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--searchword", help="the word to search for", default=DEFAULT_SEARCH_WORD)
	parser.add_argument("-a", "--area", help="the area to search in", default=DEFAULT_AREA)
	return parser.parse_args()

def _create_url(searchword, area):
	""" Creates the url for the web page to scrape. """

	return 'https://www.blocket.se/{}?q={}&cg=0&w=1&st=s&c=&ca=15&is=1&l=0&md=th'.format(area, searchword)

def main():
	args = _setup_args_parser()
	print('Searching for word "{}" in area {}...'.format(args.searchword, args.area))

	print('Fetching content from blocket')
	webpage_content = urllib.request.urlopen(_create_url(args.searchword, args.area)).read()

	# use beautiful soup to scrape web page
	soup = bs4.BeautifulSoup(webpage_content)
	items_elements = soup.find_all(DIV_ELEMENT_TAG, class_=LIST_ITEM_CLASS)
	items = []
	for item_elem in items_elements:
		items.append(item_elem.h1.a.get_text() + ',' + item_elem.p.get_text())
	
	# print website content to file
	print('Printing web content to file: {}'.format(OUTPUT_FILEPATH))
	with open(OUTPUT_FILEPATH, 'w') as output_file:
		output_file.write('item,price\n')
		output_file.write('\n'.join(items))

if __name__ == "__main__":
	main()