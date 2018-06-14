import pytest
import os
import hmac

from aiohttp import web
from ..main import Main


@pytest.fixture
def test_ping_body():
    with open(os.path.dirname(__file__) + "/test_ping.json", "rb") as inf:
        return inf.read()


@pytest.fixture
def test_ping_secret():
    return open(
        os.path.join(
            os.path.dirname(__file__), "../../secrets/webhooks/github"),
        "rb").read()


@pytest.fixture
def test_ping_sig(test_ping_secret, test_ping_body):
    return ('sha1=' + hmac.new(
        test_ping_secret, msg=test_ping_body, digestmod='sha1').hexdigest())


async def test_zen(test_client, test_ping_body, test_ping_sig):
    client = await test_client(
        lambda loop: Main(web.Application(loop=loop)).app)

    resp = await client.get('/')
    assert resp.status == 404

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "The mind is a blank canvas."

    resp = await client.post(
        "/webhooks/github",
        headers={
            "X-GitHub-Event": "ping",
            "X-Hub-Signature": test_ping_sig,
            "content-type": "application/json",
        },
        data=test_ping_body)
    assert resp.status == 200

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "Practicality beats purity."
