import dataclasses
import pathlib
import logging

from ..langhelpers import reify

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
    def discovery_cache_path(self) -> pathlib.Path:
        name = "-".join(x for x in [self.profile, "google-discovery.pickle"] if x)
        return self.dirpath / name

    @reify
    def dirpath(self) -> pathlib.Path:
        dirpath = pathlib.Path(self.prefix).expanduser()
        logger.debug("see: %s", dirpath)
        if not dirpath.exists():
            logger.info("create: %s", dirpath)
            dirpath.mkdir(exist_ok=True)
        return dirpath
