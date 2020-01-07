import typing as t
import sys
import pathlib
import logging
import dataclasses
from google_auth_oauthlib import flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from ..langhelpers import reify
from . import browse

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    prefix: str = "~/.config/cliauth"
    profile: str = ""

    skip_verify: bool = True
    token_refresh_if_need: bool = True
    launch_browser: bool = True

    @reify
    def client_secrets_path(self) -> pathlib.Path:
        name = "-".join(x for x in [self.profile, "google-client-secrets.json"] if x)
        return self.dirpath / name

    @reify
    def client_token_path(self) -> pathlib.Path:
        name = "-".join(x for x in [self.profile, "google-token.json"] if x)
        return self.dirpath / name

    @reify
    def dirpath(self) -> pathlib.Path:
        dirpath = pathlib.Path(self.prefix).expanduser()
        logger.debug("see: %s", dirpath)
        if not dirpath.exists():
            logger.info("create: %s", dirpath)
            dirpath.mkdir(exist_ok=True)
        return dirpath


class Flow:
    def __init__(self, config: Config, *, logger: logging.Logger = logger) -> None:
        self.config = config
        self.logger = logger

    def get_credentials(self, scopes: t.List[str],) -> Credentials:
        token_path = self.config.client_token_path
        self.logger.debug("see: %s", token_path)

        try:
            credentials = Credentials.from_authorized_user_file(
                token_path, scopes=scopes
            )
            if self.config.skip_verify or credentials.valid:
                return credentials

            if self.config.token_refresh_if_need:
                credentials.refresh(Request())  # xxx
                if credentials.valid:
                    return credentials
        except FileNotFoundError:
            pass

        secrets_path = self.config.client_secrets_path
        self.logger.info("client secrets are invalid (or not found). %s", secrets_path)
        self.logger.debug("see: %s", secrets_path)

        appflow = flow.InstalledAppFlow.from_client_secrets_file(
            secrets_path, scopes=scopes
        )

        if self.config.launch_browser:
            appflow.run_local_server()
        else:
            appflow.run_console()
            self.logger.debug("create: %s", token_path)
        with open(token_path, "w") as wf:
            wf.write(appflow.credentials.to_json())  # TODO: store N items
        return appflow.credentials

    def get_credentials_in_loop(self, scopes: t.List[str],) -> t.Optional[Credentials]:
        if not scopes:
            print(
                """
please passing scopes: (e.g. 'https://www.googleapis.com/auth/spreadsheets.readonly')
""",
                file=sys.stderr,
            )
            browse.scopes_info()
            return None

        while True:
            try:
                return self.get_credentials(scopes)
            except (FileNotFoundError, ValueError) as e:
                logger.warn("\t !! excpetion %r", e)
                logger.debug("error", exc_info=True)
                print(
                    f"""
please save file at {self.config.client_secrets_path} (OAuth 2.0 client ID)
""",
                    file=sys.stderr,
                )
                browse.credentials_info()
                input(
                    """
saved? (if saved, please typing enter key)
> """
                )
