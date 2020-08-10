
def test_healthcheck(test_client):
    response = test_client.get('/healthcheck')
    assert response.status_code == 200
    assert b"OK" in response.data


def test_dashboard(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_create_note(test_client):
    response = test_client.get('/notes/create/c67adac17426430c96dcf4dc1fdfce4b')
    assert response.status_code == 200


# class TestRoutes(unittest.TestCase):
#
#     def test_config(self):
#         # assert not create_app()
#         assert create_app({'TESTING': True})
#
#     def test_healthcheck(self):
#         response = app.test_client().get('/healthcheck')
#         assert response.status_code == HTTPStatus.OK, 'Health check failed'
#
# def test_hello(client):
#     response = client.get('/hello')
#     assert response.data == b'Hello, World!'

