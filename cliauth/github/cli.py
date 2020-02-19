import typing as t


def auth(
    *,
    profile: str,
    scopes: t.List[str],
    skip_verify: bool = False,
    launch_browser: bool = True,
    force: bool = False,
):
    """authentication"""
    from .config import Config
    from .authflow import Flow

    c = Config(launch_browser=launch_browser, profile=profile, skip_verify=skip_verify)
    flow = Flow(c)

    credentials = flow.get_credentials_in_loop(scopes, force=force)
    if credentials is not None:
        print(credentials.to_json())


def scopes() -> None:
    "show scope info"
    from . import browse

    browse.scopes_info()


def access_token(*, profile: str) -> None:
    """generate access token from refresh token"""
    from .config import Config
    from .authflow import Flow
    import requests

    c = Config(profile=profile, skip_verify=True)
    flow = Flow(c)

    credentials = flow.get_credentials(scopes=None)
    url = "https://www.googleapis.com/oauth2/v4/token"

    session = requests.Session()
    response = session.post(
        url,
        data={
            "refresh_token": credentials.refresh_token,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "grant_type": "refresh_token",
        },
    )
    assert response.status_code == 200, response.text
    print(response.text)


def revoke_token(
    *,
    profile: str,
    access_token: t.Optional[str] = None,
    refresh_token: t.Optional[str] = None,
) -> None:
    """revoke"""
    import requests

    if access_token is None:
        from .config import Config
        from .authflow import Flow
        from google.auth.transport.requests import AuthorizedSession

        c = Config(profile=profile, skip_verify=True)
        flow = Flow(c)

        credentials = flow.get_credentials(scopes=None)
        session = AuthorizedSession(credentials)
        token = credentials.refresh_token
    else:
        session = requests.Session()
        token = access_token or refresh_token

    url = "https://accounts.google.com/o/oauth2/revoke"

    response = session.post(url, data={"token": token})
    assert response.status_code == 200, response.text
    print(response.text)


def token_info(
    *,
    profile: str,
    access_token: t.Optional[str] = None,
    id_token: t.Optional[str] = None,
) -> None:
    """token info"""
    import requests

    if access_token is None and id_token is None:
        from .config import Config
        from .authflow import Flow
        from google.auth.transport.requests import AuthorizedSession

        c = Config(profile=profile, skip_verify=True)
        flow = Flow(c)

        credentials = flow.get_credentials(scopes=None)
        session = AuthorizedSession(credentials)
    else:
        session = requests.Session()

    url = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    data = {}
    if access_token:
        data["access_token"] = access_token
    if id_token:
        data["id_token"] = id_token
    response = session.post(url, data=data)
    assert response.status_code == 200, response.text
    print(response.text)


def run(argv: t.Optional[str] = None):
    import argparse
    import os

    if os.environ.get("DEBUG"):
        import logging

        logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(prog="cliauth")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    subparsers.required = True

    fn = auth
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument("--profile", default="")
    sub_parser.add_argument("-s", "--scopes", action="append")
    sub_parser.add_argument("--skip-verify", action="store_true")
    sub_parser.add_argument("--force", action="store_true")
    sub_parser.add_argument(
        "--no-launch-browser", action="store_false", dest="launch_browser"
    )
    sub_parser.set_defaults(subcommand=fn)

    fn = scopes
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.set_defaults(subcommand=fn)

    fn = access_token
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument("--profile", default="")
    sub_parser.set_defaults(subcommand=fn)

    fn = token_info
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument("--profile", default="")
    sub_parser.add_argument("--access-token", default=None)
    sub_parser.add_argument("--id-token", default=None)
    sub_parser.set_defaults(subcommand=fn)

    fn = revoke_token
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument("--profile", default="")
    sub_parser.add_argument("--access-token", default=None)
    sub_parser.add_argument("--refresh-token", default=None)
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = params.pop("subcommand")
    action(**params)
