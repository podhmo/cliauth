import typing as t


def auth(*, profile: str):
    print(profile)


def run(argv: t.Optional[str] = None):
    import argparse

    parser = argparse.ArgumentParser(prog="cliauth")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    subparsers.required = True

    fn = auth
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument("--profile", default="default")
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = params.pop("subcommand")
    action(**params)
