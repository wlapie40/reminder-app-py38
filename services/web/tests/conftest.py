import pytest
from services.web.src import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app, logging = create_app(test_config=True)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client
    ctx.pop()



# @pytest.fixture(scope='module')
# def new_user():
#     user = Users('c67adac17426430c96dcf4dc1fdfce4b',
#                  'Ryan',
#                  "ryan_89@kakao_mail.com",
#                  "super-secret-password",
#                  True,
#                 "2020-05-22 11:57:50.536741",
#                 "2020-05-29 11:57:50.536747")
#     return user
