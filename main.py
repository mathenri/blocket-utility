import argparse
import urllib.request
import bs4
import sys

# default args
DEFAULT_SEARCH_WORD = 'volvo'
DEFAULT_AREA = 'goteborg'
DEFAULT_UPPER_PRICE_LIMIT = sys.maxsize
DEFAULT_LOWER_PRICE_LIMIT = 0

OUTPUT_FILEPATH = './output.txt'
DIV_ELEMENT_TAG = 'div'
LIST_ITEM_CLASS = 'media-body desc'

def _setup_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--searchword", help="the word to search for", default=DEFAULT_SEARCH_WORD)
	parser.add_argument("-a", "--area", help="the area to search in", default=DEFAULT_AREA)
	parser.add_argument("-u", "--upperpricelimit", help="items with a higher price than this will not be considered", 
		default=DEFAULT_UPPER_PRICE_LIMIT, type=int)
	parser.add_argument("-l", "--lowerpricelimit", help="items with a lower price than this will not be considered",
		default=DEFAULT_LOWER_PRICE_LIMIT, type=int)

	return parser.parse_args()


def _create_url(searchword, area):
	""" Creates the url for the web page to scrape. """

	return 'https://www.blocket.se/{}?q={}&cg=0&w=1&st=s&c=&ca=15&is=1&l=0&md=th'.format(area, searchword)


def _format_price_str(price_string):
	""" Takes a string on the format '17 000:-' and returns it on the format '17000'. """

	return price_string[:-2].replace(" ", "")


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
		title = item_elem.h1.a.get_text()
		if title is None or title == '':
			print('Error: Found item with no title! Skipping this item.')
			continue

		price = item_elem.p.get_text()
		if price is None or price == '':
			print('Error: Found item with no price! Skipping this item.')
			continue

		price = _format_price_str(item_elem.p.get_text())
	
		# if this item fulfils the conditions to be considered, add it to the output file
		if int(price) < args.upperpricelimit and int(price) > args.lowerpricelimit:
			items.append(title + ',' + price)

	# print website content to file
	print('Printing web content to file: {}'.format(OUTPUT_FILEPATH))
	with open(OUTPUT_FILEPATH, 'w') as output_file:
		output_file.write('item,price\n')
		output_file.write('\n'.join(items))


if __name__ == "__main__":
	main()