import typing as t


def auth(
    *,
    profile: str,
    scopes: t.List[str],
    skip_verify: bool = False,
    launch_browser: bool = True
):
    """authentication"""
    from . import authflow

    c = authflow.Config(
        launch_browser=launch_browser, profile=profile, skip_verify=skip_verify
    )
    flow = authflow.Flow(c)

    credentials = flow.get_credentials_in_loop(scopes)
    if credentials is not None:
        print(credentials.to_json())


def scopes() -> None:
    "show scope info"
    from . import browse

    browse.scopes_info()


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
    sub_parser.add_argument(
        "--no-launch-browser", action="store_false", dest="launch_browser"
    )
    sub_parser.set_defaults(subcommand=fn)

    fn = scopes
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = params.pop("subcommand")
    action(**params)
