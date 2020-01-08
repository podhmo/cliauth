import typing as t

import logging
import requests_oauthlib
import pydantic

from .config import Config
from . import browse

logger = logging.getLogger(__name__)


class AuthInfo:
    # Temporary Credential Request URL
 	credential_request_url : str = "https://www.hatena.com/oauth/initiate"
    # Resource Owner Authorization URL (PC)
    resource_owner_authorization_url : str="https://www.hatena.ne.jp/oauth/authorize"
    # Resource Owner Authorization URL (スマートフォン)
 	resource_owner_authorization_smartphone_url : str = "https://www.hatena.ne.jp/touch/oauth/authorize"
    # Resource Owner Authorization URL (携帯電話)
	resource_owner_authorization_mobile_url : str = "http://www.hatena.ne.jp/mobile/oauth/authorize"
    # Token Request URL
 	token_request_url : str = "https://www.hatena.com/oauth/token"


class Flow:
    def __init__(self, config: Config, *, logger: logging.Logger = logger) -> None:
        self.config = config
        self.logger = logger

    def get_credentials(
        self, scopes: t.List[str], *, force: bool = False
    ) -> t.Any:
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
