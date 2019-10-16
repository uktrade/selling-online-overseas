import requests
import pytest

from unittest import mock

from django.urls import reverse


def create_response(json_body={}, status_code=200, content=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_body
    response._content = content
    return response


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_case_studies_cms(mock_cms_page, client):
    mock_cms_page.return_value = create_response({
        'child_pages': [
            {
                'meta': {'slug': 'the-slug-one'},
                'hero_image_thumbnail': {'url': 'hero.png'},
                'title': 'Title one',
                'teaser': 'Lorem ipsum one',
            },
            {
                'meta': {'slug': 'the-slug-two'},
                'hero_image_thumbnail': {'url': 'hero.png'},
                'title': 'Title two',
                'teaser': 'Lorem ipsum two',
            },
        ]
    })

    response = client.get(reverse('home'))

    assert response.status_code == 200

    assert 'Title one' in str(response.content)
    assert 'Title two' in str(response.content)
