#!/usr/bin/env python3

import time

import sys
import jwt
import requests
import click
import logging


default_auth = dict(
    private_key = open("secrets/github-app.private-key.pem", "r").read(),
    app_id = int(open("secrets/github-app.id", "r").read())
)

def jwt_for(app_id, private_key):
    issue_time = time.time() - 1
    #https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-an-installation
    payload = dict(
      iat= issue_time,
      exp= issue_time + (10 * 60),
      # GitHub App's identifier
      iss= app_id
    )

    return jwt.encode(payload, private_key, algorithm='RS256').decode()

def app_session_for(app_id, private_key):
    session = requests.Session()
    session.headers.update({
        "Authorization":"Bearer %s" % jwt_for(app_id, private_key),
        "Accept": "application/vnd.github.machine-man-preview+json"
    })

    return session

def installation_token_for(account, app_id, private_key):
    session = app_session_for(app_id, private_key)
    installations = session.get("https://api.github.com/app/installations")
    installations.raise_for_status()

    ids_by_account = { i["account"]["login"] : i["id"] for i in installations.json() }

    if not account in ids_by_account:
        return None

    token = session.post("https://api.github.com/app/installations/%i/access_tokens" % ids_by_account[account])
    token.raise_for_status()
    return token.json()

def credential_helper(credential_input, get_token_for_account):
    cvals = dict(l.strip().split("=") for l in credential_input.split("\n") if l.strip())
    logging.info("credential input: ", cvals)

    if not cvals.get("host", None) == "github.com":
        return credential_input
    if not cvals.get("protocol", "").startswith("http"):
        return credential_input

    account = cvals.get("path", "").split("/")[0]
    token = get_token_for_account(account)
    if not token:
        return credential_input

    cvals["username"]="x-access-token"
    cvals["password"]=token

    return "\n".join("=".join(i) for i in cvals.items())

def test_credential_helper():
    import pytest

    test_tokens = {"test": "testtoken", "test2": "testtoken2"}

    ssh = """
host=github.com
protocol=ssh
    """.strip()

    assert ssh == credential_helper(ssh, test_tokens.get)

    no_path = """
host=github.com
protocol=https
    """.strip()

    assert no_path == credential_helper(no_path, test_tokens.get)

    test_repo = """
host=github.com
protocol=https
path=test/repo
    """.strip()
    test_repo_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert test_repo_expected == credential_helper(test_repo, test_tokens.get)

    test2_repo = """
host=github.com
protocol=https
path=test2/repo
    """.strip()
    test2_repo_expected = """
host=github.com
protocol=https
path=test2/repo
username=x-access-token
password=testtoken2
    """.strip()

    assert test2_repo_expected == credential_helper(test2_repo, test_tokens.get)

    override_name = """
host=github.com
protocol=https
path=test/repo
username=user
    """.strip()
    override_name_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert override_name_expected == credential_helper(override_name, test_tokens.get)

    invalid_input = """
host=github.com
wat
    """.strip()
    with pytest.raises(ValueError):
        credential_helper(invalid_input, test_tokens.get)


#https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-a-github-app
@click.group()
def cli():
    pass

@click.command()
@click.argument('account')
def token(account):
    print(installation_token_for(account, **default_auth))

@cli.add_command
@click.command()
@click.argument('input', type=click.File('r'), default="-")
@click.argument('output', type=click.File('w'), default="-")
def credential(input, output):
    # https://git-scm.com/docs/git-credential

    def token_for_account(account):
        return installation_token_for(account, **default_auth)["token"]

    output.write(credential_helper(input.read(), token_for_account))
    output.write("\n")

cli.add_command(token)

if __name__ == "__main__":
    cli()
