====
mypolr
====
----
Simple python package for using the Polr Project REST API
----

Installation
====

Get package from `pip`:

    pip install mypolr

Usage
====

    from mypolr import UrlShorter

    # Replace with your values
    server_url = 'example.com'
    api_key = '1234567890abcdef'

    # Example url to shorten
    long_url = 'https://www.example.com/long/url'

    # Create UrlShorter instance
    url_shorter = UrlShorter(server_url, api_key)

    # Use
    shorted_url = url_shorter.get_shorturl(long_url)
    custom_url = url_shorter.get_shorturl(long_url, custom='myurl')
    secret_url = url_shorter.get_shorturl(long_url, is_secret=True)
