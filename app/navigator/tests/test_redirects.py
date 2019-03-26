import pytest
import http

from django.core.urlresolvers import reverse

# the first element needs to end with a slash
redirects = [
    (
        '/selling-online-overseas/markets/story/global-marketplaces-drive-burlingham-london-to-success/',  # noqa
        '/'
    ),
    (
        '/selling-online-overseas/markets/story/online-marketplaces-propel-freestyle-xtreme-sales/',
        '/'
    ),
    (
        '/selling-online-overseas/markets/story/hello-babys-rapid-online-growth/',
        '/'
    ),
    (
        '/selling-online-overseas/markets/story/york-bag-retailer-goes-global-via-e-commerce/',
        '/'
    ),
    (
        '/selling-online-overseas/markets/story/incorrect-case-study-slug/',
        '/'
    ),
]


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)

    assert response.status_code == http.client.FOUND
    if not expected.startswith('http') and not expected.startswith('/'):
        expected = reverse(expected)

    assert response.url == expected
