from casestudy import casestudies
from django.template import Context, Template


def test_case_study_time_to_read():
    article = casestudies.CaseStudy(
        slug='test-slug',
        markdown_file_path=(
            'casestudy/markdown/test.md')
    )
    assert article.time_to_read == 'Less than 1 minute'


def test_case_study_html():
    article = casestudies.CaseStudy(
        slug='test-slug',
        markdown_file_path=(
            'casestudy/markdown/test.md')
    )
    template = Template(
        '{% spaceless %}{{ article.html|safe }}{% endspaceless %}')
    context = Context({'article': article})
    html = template.render(context)
    exp_html = (
        '<p>Lorem ipsum dolor sit amet.</p>'
        '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>'
        )
    print(html)
    assert html == exp_html
