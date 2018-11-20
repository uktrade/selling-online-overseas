from django.utils.functional import cached_property

from casestudy import helpers


class CaseStudy:

    def __init__(self, markdown_file_path, slug):
        self.markdown_file_path = markdown_file_path
        self.slug = slug

    @cached_property
    def time_to_read(self):
        from casestudy import helpers
        seconds = helpers.time_to_read_in_seconds(self)
        return helpers.time_to_read_in_minutes(seconds)

    def html(self):
        html = helpers.markdown_to_html(
            markdown_file_path=self.markdown_file_path,
        )
        return html


RED_HERRING = CaseStudy(
    slug='red-herring-games-take-their-mysteries-overseas-through-amazon',
    markdown_file_path=(
        'casestudy/markdown/red-herring.md')
)
BUBBLEBUM = CaseStudy(
    slug=(
        'selling-online-overseas-sees-bubblebum-increase-export-'
        'sales-by-15-percent'),
    markdown_file_path=(
        'casestudy/markdown/bubblebum.md')
)
RAREWAVES = CaseStudy(
    slug='chiswick-retailer-strikes-deal-with-amazon-australia',
    markdown_file_path=(
        'casestudy/markdown/rarewaves.md')
)

CASE_STUDIES = {
    RED_HERRING.slug: RED_HERRING,
    BUBBLEBUM.slug: BUBBLEBUM,
    RAREWAVES.slug: RAREWAVES
}
