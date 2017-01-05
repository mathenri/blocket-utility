import argparse

DEFAULT_SEARCH_WORD = 'volvo'

def _setup_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--searchword", help="the word to search for", 
		default=DEFAULT_SEARCH_WORD)
	return parser.parse_args()

def main():
	args = _setup_args_parser()

	# read xml and find the applicable test case element
	print('Searching for word "{}" ...'.format(args.searchword))

if __name__ == "__main__":
	main()