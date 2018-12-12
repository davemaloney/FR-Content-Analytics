"""Get Page Analytics

    Command line usage:
    $ python GetIndexContent.py
"""

import unicodecsv as csv
from soup import get_index_content


def main():
    """Uses indexPages.csv to create indexContent.csv

    IndexPages.csv assumes each line comes in the form of
        `name-of-entry`
    IndexContent.csv will output each url in the form of
        `www.ftse.com/product/indices/name-of-entry`
    """

    input_file = 'csv/indexPages.csv'
    output_file = 'csv/indexContent.csv'

    print(input_file)

    pages = []

    with open(input_file, 'rb') as csvfile:
        pageslist = csv.reader(csvfile)
        for row in pageslist:
            url = ', '.join(row)
            page = 'https://www.ftse.com/products/indices/' + url
            if url == 'geis-series':
                url = 'https://www.ftse.com/products/indices/home/IndexHomeGeis/?indexName=GEISAC&currency=USD&rtn=CAPITAL&ctry=Regions'
            else:
                url = 'https://www.ftse.com/products/indices/home/GetIndexData/?indexName=' + url
            print(url)

            page_data = []

            # CONTENT
            page_content = get_index_content(url)
            # page_content = ', '.join(get_index_content(url))

            # Insert the URL at postion 0
            page_data.insert(0, page)
            # Insert the content at position 1
            page_data.insert(1, page_content[2])
            page_data.insert(2, page_content[0])
            page_data.insert(3, page_content[1])

            pages.append((page_data))

    with open(output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "URL",
            "Title",
            "HTML",
            "Content in English",
            "Content in Japanese"
        ])
        for page in pages:
            writer.writerow(page)


if __name__ == '__main__':
    main()
