import requests


def is_valid_url(url):
    """Validates if the URL is valid and accessible."""

    imdb_url = 'https://www.imdb.com/chart/top/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.status_code == 200 and url == imdb_url
    except requests.exceptions.HTTPError:
        return False
    except requests.exceptions.RequestException:
        return False
