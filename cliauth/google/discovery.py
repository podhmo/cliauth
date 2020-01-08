from __future__ import annotations
import typing as t
import logging
import pickle

from googleapiclient.discovery_cache.base import Cache as _Cache
from googleapiclient import discovery as _discovery

from . import Config
from ..langhelpers import reify

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, config: Config, *, logger: logging.Logger = logger) -> None:
        self.config = config
        self.logger = logger

    @reify
    def cache(self):
        cache_path = self.config.discovery_cache_path
        self.logger.debug("see: %s", cache_path)

        if cache_path.exists():
            with cache_path.open("rb") as rf:
                return pickle.load(rf)

        return _MemoryCache()

    def save(self, *, cache: t.Optional[_Cache] = None):
        cache = cache or self.cache

        cache_path = self.config.discovery_cache_path
        self.logger.debug("save: %s", cache_path)
        with cache_path.open("wb") as wf:
            pickle.dump(cache, wf)


class _MemoryCache(_Cache):
    def __init__(self):
        self.cache = {}

    def get(self, url):
        return self.cache.get(url)

    def set(self, url, content):
        self.cache[url] = content

    @property
    def is_empty(self):
        return len(self.cache) == 0


@t.no_type_check
def build(
    serviceName,
    version,
    http=None,
    discoveryServiceUrl=_discovery.DISCOVERY_URI,
    developerKey=None,
    model=None,
    requestBuilder=_discovery.HttpRequest,
    credentials=None,
    cache_discovery=True,
    cache: t.Optional[Cache] = None,
):
    """Construct a Resource for interacting with an API.

  Construct a Resource object for interacting with an API. The serviceName and
  version are the names from the Discovery service.

  Args:
    serviceName: string, name of the service.
    version: string, the version of the service.
    http: httplib2.Http, An instance of httplib2.Http or something that acts
      like it that HTTP requests will be made through.
    discoveryServiceUrl: string, a URI Template that points to the location of
      the discovery service. It should have two parameters {api} and
      {apiVersion} that when filled in produce an absolute URI to the discovery
      document for that service.
    developerKey: string, key obtained from
      https://code.google.com/apis/console.
    model: googleapiclient.Model, converts to and from the wire format.
    requestBuilder: googleapiclient.http.HttpRequest, encapsulator for an HTTP
      request.
    credentials: oauth2client.Credentials or
      google.auth.credentials.Credentials, credentials to be used for
      authentication.
    cache_discovery: Boolean, whether or not to cache the discovery doc.
    cache: googleapiclient.discovery_cache.base.CacheBase, an optional
      cache object for the discovery documents.

  Returns:
    A Resource object with methods for interacting with the service.
  """
    need_save = cache is not None and cache.cache.is_empty

    resource = _discovery.build(
        serviceName=serviceName,
        version=version,
        http=http,
        discoveryServiceUrl=discoveryServiceUrl,
        developerKey=developerKey,
        model=model,
        requestBuilder=requestBuilder,
        credentials=credentials,
        cache_discovery=True,
        cache=cache.cache if cache else None,
    )
    if cache is None:
        logger.info("if speed up, passing cache")
        return resource

    if need_save:
        cache.save()
    return resource
