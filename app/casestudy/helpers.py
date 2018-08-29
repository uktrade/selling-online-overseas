from bs4 import BeautifulSoup
import markdown2
from django.template.loader import render_to_string


WORDS_PER_SECOND = 1.5  # Average word per second on screen


def markdown_to_html(markdown_file_path, context={}):
    content = render_to_string(markdown_file_path, context)
    return markdown2.markdown(content, extras=['metadata'])


def get_word_count(html):
    soup = BeautifulSoup(html.replace('\n', ''), 'html.parser')
    words = ''.join(soup.findAll(text=True)).strip()
    return len(words.split(' '))


def time_to_read_in_seconds(article):
    html = markdown_to_html(article.markdown_file_path)
    return round(get_word_count(html) / WORDS_PER_SECOND)


def time_to_read_in_minutes(value):
    if value <= 59:
        return 'Less than 1 minute'
    minutes = int(round(value / 60))
    unit = 'min' if minutes == 1 else 'mins'
    return '{minutes} {unit}'.format(minutes=minutes, unit=unit)
