import pytest
from casestudy import helpers, casestudies


@pytest.mark.parametrize('seconds,expected', (
    (59, 'Less than 1 minute'),
    (60, '1 min'),
    (61, '1 min'),
    (120, '2 mins'),
    (180, '3 mins'),
    (600, '10 mins'),
    (6000, '100 mins'),
))
def test_time_to_read(seconds, expected):
    assert helpers.time_to_read_in_minutes(seconds) == expected


def test_get_word_count():
    html = '<p>The quick brown fox jumps over the lazy dog.</p>'
    word_count = helpers.get_word_count(html)
    assert word_count == 9


def test_time_to_read_seconds():
    article = casestudies.CaseStudy(
        slug='test-slug',
        markdown_file_path=(
            'casestudy/markdown/test.md')
    )
    read_time = helpers.time_to_read_in_seconds(article)
    assert read_time == 8
