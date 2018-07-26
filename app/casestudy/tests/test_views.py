import pytest
from django.template.loader import render_to_string
from casestudy.casestudies import CaseStudy


@pytest.mark.django_db(transaction=False)
def test_other_stories(client):
    template_name = 'case_study.html'
    article = CaseStudy(
        slug='test-slug',
        markdown_file_path=(
            'casestudy/markdown/test.md')
    )
    context = {
        'story': article
    }
    html = render_to_string(template_name, context)
    assert html == ''
