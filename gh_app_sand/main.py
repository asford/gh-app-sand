import logging
import os

import attr
from aiohttp import web

from .mind import Mind
from .webhooks.github import GithubHooks
from .webhooks.buildkite import BuildkiteHooks


@attr.s(auto_attribs=True, slots=True)
class Main:
    app: web.Application
    github_hooks: GithubHooks
    buildkite_hooks: BuildkiteHooks
    mind: Mind

    async def get_mind(self, req: web.Request):
        return web.Response(body=self.mind.thought)

    async def store_ping(self, name, body):
        assert name == "ping"
        self.mind.thought = body["zen"]

    @staticmethod
    def setup(loop=None):
        sdir = os.path.join(os.path.dirname(__file__), "../secrets/")

        app = web.Application(loop=loop)
        github_hooks = GithubHooks(
            secret=open(sdir + "/webhooks/github", "rb").read().strip())
        buildkite_hooks = BuildkiteHooks(
            token=open(sdir + "/webhooks/buildkite", "r").read().strip())
        mind = Mind()
        main = Main(
            app=app,
            github_hooks=github_hooks,
            buildkite_hooks=buildkite_hooks,
            mind=mind)

        app.router.add_get("/zen", main.get_mind)

        app.router.add_post('/webhooks/github', github_hooks.handler)
        github_hooks.signals.add_handler("ping", main.store_ping)
        github_hooks.signals.freeze()

        app.router.add_post('/webhooks/buildkite', buildkite_hooks.handler)
        buildkite_hooks.signals.freeze()


        return main


def create_app(loop):
    async def set_verbose_logging(*_):
        logging.root.setLevel(logging.DEBUG)
        logging.info("debug")

    app = Main.setup(loop=loop).app
    app.on_startup.append(set_verbose_logging)

    return app
