import typing as t
import sys

import logging

from .config import Config
from . import browse
from ._credentials import Credentials
from ._flow import InstalledAppFlow

Request = object
GoogleAuthError = Exception
_LOGGER = logger = logging.getLogger(__name__)


class Flow:
    def __init__(self, config: Config, *, logger: logging.Logger = logger) -> None:
        self.config = config
        self.logger = logger

    def get_credentials(
        self, scopes: t.List[str], *, force: bool = False
    ) -> Credentials:
        token_path = self.config.client_token_path

        if not force:
            self.logger.debug("see: %s", token_path)
            try:
                credentials = Credentials.from_authorized_user_file(
                    token_path, scopes=scopes
                )
                if self.config.skip_verify or credentials.valid:
                    return credentials

                if self.config.token_refresh_if_need:
                    # invalid scope
                    credentials.refresh(Request())  # xxx
                    if credentials.valid:
                        return credentials
            except GoogleAuthError as e:
                self.logger.info("auth error is raised: %r", e, exc_info=True)
            except FileNotFoundError:
                pass

        secrets_path = self.config.client_secrets_path
        self.logger.info("client secrets are invalid (or not found). %s", secrets_path)
        self.logger.debug("see: %s", secrets_path)

        appflow = InstalledAppFlow.from_client_secrets_file(secrets_path, scopes=scopes)

        if self.config.launch_browser:
            appflow.run_local_server()
        else:
            appflow.run_console()
            self.logger.debug("create: %s", token_path)
        with open(token_path, "w") as wf:
            wf.write(appflow.credentials.to_json())  # TODO: store N items
        return appflow.credentials

    def get_credentials_in_loop(
        self, scopes: t.List[str], *, force: bool = False
    ) -> t.Optional[Credentials]:
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
                return self.get_credentials(scopes, force=force)
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
