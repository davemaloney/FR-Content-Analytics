# FTSE Russell Content Analytics

A program to get pageview counts for blogs, press releases, and research papers on ftserussell.com over the first 90 days from their initial publication.

## Prerequisites

### Check platform

Ensure Python and Pip ar installed and available

```shell
$ which python
usr/bin/python
$ which pip
usr/bin/pip
```


### Install dependencies

Install `requests`, `BeautifulSoup4`, `nltk`, `google-api-python-client` to the `user` account.

```shell
$ bash analytics.sh
```

### API Key
Make sure Google Analytics API Key is available at [secrets/client-secrets.json](secrets/client-secrets.json), or get a new key through the [Google API Console](https://console.developers.google.com/apis/credentials).

## Get Started

### Get List of Pages

Get the list of pages, using `-i` to provide the page partial. E.g., for http://www.ftserussell.com/blog use `blog`

```shell
$ python GetPages.py -i blog
$ python GetPages.py -i press-releases
$ python GetPages.py -i research
```

### Get the Performance Data

```shell
$ python GetPerformance.py -i blog
$ python GetPerformance.py -i press-releases
$ python GetPerformance.py -i research
```

Creates
- [csv/blogPerformance.csv](csv/blogPerformance.csv)
- [csv/press-releasePerformance.csv](csv/press-releasePerformance.csv)
- [csv/researchPerformance.csv](csv/researchPerformance.csv)
