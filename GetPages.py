""" Get a list of page URLs

    Command line usage:
    $ python GetPages.py -i blog
    $ python GetPages.py -i press-releases
    $ python GetPages.py -i research
"""

import csv
from soup import soup

def get_pages(page):
    """ Outputs a list of blogs to `pagePages.csv` """
    url = 'http://www.ftserussell.com/' + page
    print(url)

    filename = 'csv/' + page + 'Pages.csv'
    print(filename)

    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        while url:
            page_text = soup(url)

            for link in page_text.select('h3 a[href]'):
                paperlink = link['href']
                print(paperlink)
                writer.writerow([paperlink])

            # next page url
            url = page_text.find('li', {'class': 'pager-current'}).find_next_sibling('li')
            if url:
                url = url.find('a')['href']
                url = 'http://www.ftserussell.com' + url
            else:
                break

def getopts(arg):
    """taken from https://gist.github.com/dideler/2395703"""
    opts = {}  # Empty dictionary to store key-value pairs.
    while arg:  # While there are arguments left to parse...
        if arg[0][0] == '-':  # Found a "-name value" pair.
            opts[arg[0]] = arg[1]  # Add key and value to the dictionary.
        arg = arg[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    from sys import argv
    MYARGS = getopts(argv)
    if '-i' in MYARGS:  # Example usage.
        print(MYARGS['-i'])
    get_pages(MYARGS['-i'])
