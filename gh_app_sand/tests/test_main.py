from ..main import Main

def create_main(loop):
    return Main.setup(loop).app

async def test_hello(test_client):
    client = await test_client(create_main)
    resp = await client.get('/')
    assert resp.status == 404

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "The mind is a blank canvas."
