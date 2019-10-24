import pytest

from unittest import mock

from django.urls import reverse

from helpers import create_response


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_home_page(mock_cms_page, client):
    mock_cms_page.return_value = create_response({'child_pages': []})
    response = client.get(reverse('home'))

    assert response.status_code == 200
    assert response.context_data['page_type'] == 'LandingPage'
    assert 'Selling online overseas' in str(response.content)


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_case_studies_cms(mock_cms_page, client):
    mock_cms_page.return_value = create_response({
        'featured_case_studies': [
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
