from django.views.generic import TemplateView
from django.shortcuts import redirect

from thumber.decorators import thumber_feedback
from casestudy.casestudies import CASE_STUDIES


@thumber_feedback
class CaseStudyView(TemplateView):
    """
    The simple view for a case story page
    """

    comment_placeholder = "We are sorry to hear that. Would you tell us why?"
    submit_wording = "Send feedback"
    template_name = 'case_study.html'

    def dispatch(self, *args, **kwargs):
        try:
            self.story = CASE_STUDIES[self.kwargs['slug']]
            return super().dispatch(*args, **kwargs)
        except:
            return redirect('/')

    def get_other_stories(self):
        other_stories = []
        for key, value in CASE_STUDIES.items():
            if key != self.kwargs['slug']:
                other_stories.append(value)
        return other_stories

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            story=self.story,
            other_stories=self.get_other_stories(),
            *args, **kwargs
        )
