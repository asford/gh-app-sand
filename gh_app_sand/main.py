import logging

import attr
import asyncio
from aiohttp import web

from .mind import Mind
from .webhooks.github import handler


@attr.s(slots=True, auto_attribs=True)
class Main:
    app: web.Application
    mind: Mind = attr.Factory(Mind)

    async def get_mind(self, req: web.Request):
        return web.Response(body=self.mind.thought)

    def __attrs_post_init__(self):
        self.app.router.add_get("/zen", self.get_mind)
        self.app.router.add_post("/webhooks/github", handler)


def main(argv):
    return Main(web.Application(loop=asyncio.get_event_loop())).app


def create_app(loop):
    async def set_verbose_logging(*_):
        logging.root.setLevel(logging.DEBUG)
        logging.info("debug")

    app = Main(web.Application(loop=loop)).app
    app.on_startup.append(set_verbose_logging)

    return app
