import pytest
# from django.template.loader import render_to_string
# from casestudy.casestudies import CaseStudy
from django.core.urlresolvers import reverse_lazy
from casestudy.casestudies import (
    BURLINGHAM,
    RAREWAVES,
)


@pytest.mark.django_db(transaction=False)
def test_other_stories(client):
    url = reverse_lazy(
        'markets:case_story',
        kwargs={'slug': (
            'red-herring-games-take-their-mysteries-overseas-through-amazon')
        })
    response = client.get(url)
    assert response.context['other_stories'] == [BURLINGHAM, RAREWAVES]
