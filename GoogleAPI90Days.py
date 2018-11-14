"""Blog Analytics"""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'secrets/client-secrets.json'
VIEW_ID = '112635098'


def initialize_api():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, page, date):
    """Queries the Analytics Reporting API V4.

    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
        page: A url that will satisfy a search in the given view
        date: A date string in the form YYYY-MM-DD
    Returns:
        Page Views by day for all pages that match the regular expression,
        up to 90 days from the start date to today"""
    return analytics.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate': date, 'endDate': 'today'}],
                'metrics': [
                    {'expression': 'ga:pageviews'},
                    {'expression': 'ga:avgTimeOnPage'}
                ],
                'dimensions': [{
                    'name': 'ga:pagePath',
                    'name': 'ga:date'
                }],
                'dimensionFilterClauses': [{
                    'filters': [{
                        'dimensionName': 'ga:pagePath',
                        'operator': 'REGEXP',
                        'expressions': page
                    }]
                }],
                'includeEmptyRows': 'true',
                'pageSize': 90
            }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.

    Returns:
        a list of page view numbers
    """

    pageviews = []

    for row in response.get('reports', [])[0].get('data', {}).get('rows', []):
        date_range_values = row.get('metrics', [])

        for values in date_range_values:
            value = values.get('values')[0]
            pageviews.append(value)

    time = response.get('reports', [])[0].get(
        'data', {}).get('totals', [])[0].get('values', [])[1]

    response = {
        'pageviews': pageviews,
        'time': time
    }

    return response
