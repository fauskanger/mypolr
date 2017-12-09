import requests
import pytest
import responses


def test_pytest():
    x = "this"
    assert 'h' in x
    with pytest.raises(ValueError):
        raise ValueError('Pytest can test this')


@responses.activate
def test_responses_demo():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  json={'error': 'not found'}, status=404)

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.text == '{"error": "not found"}'


@responses.activate
def test_mocking():
    url = "http://ti.ny"

    # Multiple responses to the same url must be added before any request to it has been made
    responses.add(responses.GET, url, body='{"title": "Test Deal"}', content_type="application/json")
    responses.add(responses.GET, url, json=dict(a=10, b='foo'), status=401)
    responses.add(responses.GET, url, body=requests.HTTPError('Some HttpError'), status=500)
    responses.add(responses.GET, url, body=requests.Timeout('cannot do'), status=500)

    r = requests.get(url)
    assert r.json() == {"title": "Test Deal"}

    r = requests.get(url)
    assert r.json().get('a') == 10
    assert r.json().get('b') == 'foo'
    assert r.status_code == 401

    with pytest.raises(requests.HTTPError):
        requests.get(url)

    with pytest.raises(ValueError):
        try:
            requests.get(url)
        except requests.Timeout as e:
            raise ValueError(e)

    # Requests to url without a defined response will raise ConnectionError
    responses.add(responses.GET, 'http://www.google.com', body='OK')
    with pytest.raises(requests.ConnectionError):
        requests.get('http://nrk.no')

