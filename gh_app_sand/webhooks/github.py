import hmac

from aiohttp import web
import os

import logging
logger = logging.getLogger(__name__)

secret = open(os.path.join(
    os.path.dirname(__file__), "../../secrets/webhooks/github"), "rb").read()

async def handler(req: web.Request):
    # Get and validate signature
    sig = req.headers.get('x-hub-signature')
    if sig:
        raw_body = await req.read()

        mac = hmac.new(b"compassion_is_a_virtue", msg=raw_body, digestmod='sha1')
        local_sig = "sha1=" + mac.hexdigest()

        logger.info("x-hub-sig: %s", sig)
        logger.info("payload-sig: %s", local_sig)

        if not sig == local_sig:
            return web.Response(status=401, text="invalid x-hub-signature")

    # Get body (and raw body for validation), unpack content type
    logger.info("content-type: %s", req.headers["content-type"])
    if req.headers["content-type"] == "application/x-www-form-urlencoded":
        body = (await req.post())["payload"]
    else:
        body = await req.json()

    name = req.headers['x-github-event']
    logger.info("name: %s", name)

    # emitter.emit(name, body)
    return web.Response(status=200)
