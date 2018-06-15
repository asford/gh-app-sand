import logging
import json

import aiohttp
import aiorun
import asyncio
import click
from decorator import decorator

from .github.identity import AppIdentity
from .github.gitcredentials import credential_helper

logger = logging.getLogger(__name__)

#https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-a-github-app
pass_appidentity = click.make_pass_decorator(AppIdentity, ensure=True)


@decorator
def aiomain(coro, *args, **kwargs):
    aiorun.logger.setLevel(51)

    async def main():
        try:
            await coro(*args, **kwargs)
        finally:
            asyncio.get_event_loop().stop()

    return aiorun.run(main())


@click.group()
@click.option(
    '--app_id',
    help=("Integer app id, or path to file containing id. "
          "Resolved from $%s." % AppIdentity.APP_ID_ENV_VAR),
    envvar=AppIdentity.APP_ID_ENV_VAR,
)
@click.option(
    '--private_key',
    help=("App private key, or path to private key file. "
          "Resolved from $%s." % AppIdentity.PRIVATE_KEY_ENV_VAR),
    envvar=AppIdentity.PRIVATE_KEY_ENV_VAR,
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    help="'-v' for logging, '-vv' for debug logging. "
    "Resolved via $GITHUB_APP_AUTH_DEBUG ('1' or '2').",
    envvar="GITHUB_APP_AUTH_DEBUG",
)
@click.pass_context
def main(ctx, app_id, private_key, verbose):
    if verbose:
        logging.basicConfig(
            level=logging.INFO if verbose == 1 else logging.DEBUG,
            format="%(name)s %(message)s",
        )

    ctx.obj = AppIdentity(app_id=app_id, private_key=private_key)


@main.add_command
@click.command(help="Resolve app id/key and check app authentication.")
@pass_appidentity
@aiomain
async def current(appidentity: AppIdentity):
    async with aiohttp.ClientSession(
            headers=appidentity.app_headers(), ) as session:
        async with session.get('https://api.github.com/app', ) as resp:
            resp.raise_for_status()
            print(json.dumps(await resp.json(), indent=2))


@main.add_command
@click.command(help="Generate access token for installation.")
@pass_appidentity
@click.argument('account')
@aiomain
async def token(appidentity, account):
    print(await appidentity.installation_token_for(account))


@main.group(help="git-credential helper implementation.")
def credential():
    pass


@credential.add_command
@click.command(help="Credential storage helper implementation.")
@pass_appidentity
@click.argument('input', type=click.File('r'), default="-")
@click.argument('output', type=click.File('w'), default="-")
@aiomain
async def get(appidentity, input, output):
    # https://git-scm.com/docs/git-credential
    logger.debug("get id: %s input: %s output: %s", appidentity, input, output)
    output.write(await credential_helper(input.read(), appidentity.installation_token_for))
    output.write("\n")


@credential.command(help="no-op git-credential interface")
def store():
    pass


@credential.command(help="no-op git-credential interface")
def erase():
    pass
