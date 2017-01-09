import argparse
import urllib.request
import bs4

DEFAULT_SEARCH_WORD = 'volvo'
URL = 'https://www.blocket.se/goteborg?ca=15'
OUTPUT_FILEPATH = './output.html'
DIV_ELEMENT_TAG = 'div'
LIST_ITEM_CLASS = 'media-body desc'

def _setup_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--searchword", help="the word to search for", 
		default=DEFAULT_SEARCH_WORD)
	return parser.parse_args()

def main():
	args = _setup_args_parser()
	print('Searching for word "{}" ...'.format(args.searchword))

	print('Fetching content from blocket')
	webpage_content = urllib.request.urlopen(URL).read()

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