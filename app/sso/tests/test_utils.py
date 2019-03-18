from django.views.generic import TemplateView
from django.urls import reverse

from sso import utils


def test_sso_login_required_mixin_redirect_to_sso():
    instance = utils.SSOLoginRequiredMixin()
    instance.sso_redirect_url = 'http://www.login.com'

    response = instance.redirect_to_sso(next_url='/thing')

    assert response.get('Location') == 'http://www.login.com?next=/thing'


def test_sso_signup_required_mixin_redirect_to_sso():
    instance = utils.SSOSignUpRequiredMixin()
    instance.sso_redirect_url = 'http://www.signup.com'

    response = instance.redirect_to_sso(next_url='/thing')

    assert response.get('Location') == 'http://www.signup.com?next=/thing'


def test_sso_account_state_required(rf):
    class TestView(utils.SSOLoginRequiredMixin, TemplateView):
        template_name = 'markets/homepage.html'

    request = rf.get(reverse('home'))
    request.sso_user = None
    view = TestView.as_view()

    response = view(request)

    assert response.status_code == 302
    assert response.url == (
        'http://sso.trade.great:8004/accounts/login/?next=http%3A//testserver/selling-online-overseas/'
    )
