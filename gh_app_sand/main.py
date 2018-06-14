import attr

from aiohttp import web

from .mind import Mind

@attr.s(slots=True, auto_attribs=True)
class Main:
    app: web.Application
    mind: Mind = attr.Factory(Mind)

    async def get_mind(self, req: web.Request):
        return web.Response(body=self.mind.thought)

    @staticmethod
    def setup(loop):
        inst = Main(app=web.Application(loop=loop))
        inst.app.router.add_get("/zen", inst.get_mind)
        return inst
