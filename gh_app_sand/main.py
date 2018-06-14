import attr
import asyncio
from aiohttp import web

from .mind import Mind

@attr.s(slots=True, auto_attribs=True)
class Main:
    app: web.Application
    mind: Mind = attr.Factory(Mind)

    async def get_mind(self, req: web.Request):
        return web.Response(body=self.mind.thought)

    def __attrs_post_init__(self):
        self.app.router.add_get("/zen", self.get_mind)

def init(argv):
    return Main(web.Application(loop = asyncio.get_event_loop())).app
