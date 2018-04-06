"""Get Page Analytics

    Command line usage:
    $ python GetPerformance.py -i blog
    $ python GetPerformance.py -i press-releases
    $ python GetPerformance.py -i research
"""

import csv
from GoogleAPI90Days import initialize_api, get_report, print_response
from soup import word_count, blog_word_count, get_date

def main(page_key):
    """Uses Pages.csv to create Performance.csv

    Pages.csv assumes each line comes in the form of
        `/name-of-entry`
    Performance.csv will output each url in the form of
        `www.ftserussell.com/name-of-entry`
    """

    input_file = 'csv/' + page_key + 'Pages.csv'
    output_file = 'csv/' + page_key + 'Performance.csv'
    analytics = initialize_api()

    pages = []

    with open(input_file, 'rb') as csvfile:
        pageslist = csv.reader(csvfile)
        for row in pageslist:
            url = ', '.join(row)
            url = 'http://www.ftserussell.com' + url
            page = url.split('//')[1]

            # DATE
            date = get_date(url)

            # ANALYTICS
            response = get_report(analytics, page, date)

            page_data = print_response(response)
            page_data.insert(0, page)
            page_data.insert(1, date)
            if page_key == 'blog':
                page_data.insert(2, blog_word_count(url))
            else:
                page_data.insert(2, word_count(url))

            pages.append((page_data))

    with open(output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "URL",
            "Published Date",
            "Word Count"
        ])
        for page in pages:
            writer.writerow(page)

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
    main(MYARGS['-i'])