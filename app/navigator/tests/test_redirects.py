import pytest
import http

from django.core.urlresolvers import reverse

# the first element needs to end with a slash
redirects = [
    (
        '/markets/story/global-marketplaces-drive-burlingham-london-to-success/', # noqa
        '/'
    ),
    (
        '/markets/story/online-marketplaces-propel-freestyle-xtreme-sales/',
        '/'
    ),
    (
        '/markets/story/hello-babys-rapid-online-growth/',
        '/'
    ),
    (
        '/markets/story/york-bag-retailer-goes-global-via-e-commerce/',
        '/'
    ),
    (
        '/markets/story/incorrect-case-study-slug/',
        '/'
    ),
]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)

    assert response.status_code == http.client.FOUND
    if not expected.startswith('http') and not expected.startswith('/'):
        expected = reverse(expected)

    assert response.url == expected
