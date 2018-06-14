from aiohttp import web
from ..main import Main


async def test_hello(test_client):
    client = await test_client(
        lambda loop: Main(web.Application(loop=loop)).app)

    resp = await client.get('/')
    assert resp.status == 404

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "The mind is a blank canvas."
