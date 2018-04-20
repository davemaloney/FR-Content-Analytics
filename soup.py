"""Beautiful Soup Commands"""

import re
import requests
from bs4 import BeautifulSoup
import nltk

def soup(url):
    """Make the soup
    Args:
        url: a fully-qualified URL
    """
    # query the website and return the html to the variable `page`
    full_page = requests.get(url, headers={'User-Agent': "Magic Browser"})
    # encode to ascii to avoid unicode errors
    page_text = full_page.text.encode('utf-8').decode('ascii', 'ignore')
    # parse the html using beautiful soup and store in variable `soup`
    parsed_soup = BeautifulSoup(page_text, 'html.parser')

    return parsed_soup


def blog_word_count(url):
    """Get a word count, cut off at London Stock Exchange Group plc
    Args:
        url: a fully-qualified URL
    """
    # isolate the blog content from the soup
    blog_content = soup(url).find('div', attrs={'class': 'post-body'}).text.strip()
    # trim the blog content at `London Stock Exchange Group plc`
    blog_trimmed = blog_content.split("London Stock Exchange Group plc")[0]
    tokens = nltk.word_tokenize(blog_trimmed)
    text = nltk.Text(tokens)
    # remove punctuation, count raw words
    non_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if non_punct.match(w)]
    raw_word_count = len(raw_words)

    return raw_word_count


def word_count(url):
    """Get a word count of a research article
    Args:
        url: a fully-qualified URL
    """
    # isolate the blog content from the soup
    research_content = soup(url).find(
        'div',
        attrs={'class': 'field-type-text-with-summary'}
    ).text.strip()
    tokens = nltk.word_tokenize(research_content)
    text = nltk.Text(tokens)
    # remove punctuation, count raw words
    non_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if non_punct.match(w)]
    raw_word_count = len(raw_words)

    return raw_word_count


def get_date(url):
    """Get a date from a tag in the form of
        <meta property="article:published_time" content="YYYY-MM-DDTHH:MM:SS+00:00">
    Args:
        url: a fully-qualified URL
    """
    blog_date = soup(url).find(
        'meta',
        attrs={'property': 'article:published_time'}
    )['content'].split('T')[0]

    return blog_date


def get_tags(url):
    """Get the tags from a tag in the form of
        <meta property="idio:topic" content="Topic">
    Args:
        url: a fully-qualified URL
    """
    blog_tags = soup(url).find_all(
        'meta',
        attrs={'property': 'idio:topic'}
    )
    tags = []
    for tag in blog_tags:
        tags.append((tag['content']))

    tags.sort()

    return tags
