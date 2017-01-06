import argparse
import urllib.request
import bs4

DEFAULT_SEARCH_WORD = 'volvo'
URL = 'https://www.blocket.se/goteborg?ca=15'

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
	print(soup.prettify()[0:1000])

if __name__ == "__main__":
	main()