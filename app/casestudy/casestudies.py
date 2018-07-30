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

    @cached_property
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
BURLINGHAM = CaseStudy(
    slug='global-marketplaces-drive-burlingham-london-to-success',
    markdown_file_path=(
        'casestudy/markdown/burlingham.md')
)
RAREWAVES = CaseStudy(
    slug='chiswick-retailer-strikes-deal-with-amazon-australia',
    markdown_file_path=(
        'casestudy/markdown/rarewaves.md')
)

CASE_STUDIES = {
    RED_HERRING.slug: RED_HERRING,
    BURLINGHAM.slug: BURLINGHAM,
    RAREWAVES.slug: RAREWAVES
}
