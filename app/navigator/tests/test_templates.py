from django.template.loader import render_to_string

from bs4 import BeautifulSoup


def test_homepage_case_studies_cms():
    context = {
        'success_stories': [
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
    }

    html = render_to_string('markets/homepage.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    case_studies = soup.find(id='featured-case-studies').find_all('article')
    assert len(case_studies) == 2


def test_homepage_case_studies_cms_empty():
    context = {
        'success_stories': []
    }

    html = render_to_string('markets/homepage.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    assert not soup.find(id='featured-case-studies')
