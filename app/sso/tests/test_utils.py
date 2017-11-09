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
