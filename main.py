import argparse
import urllib.request

DEFAULT_SEARCH_WORD = 'volvo'
URL = 'http://www.blocket.se'

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
	print('Received content:\n{}'.format(webpage_content))

if __name__ == "__main__":
	main()