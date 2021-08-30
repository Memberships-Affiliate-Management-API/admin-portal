"""
    **cache Manager**
        this module will handle all requests from this application to other api's

"""
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask_caching import Cache
from config import config_instance


class CacheManager:

    def __init__(self) -> None:
        self.app_cache: Cache = Cache()

    def init_app(self, app, config):
        self.app_cache.init_app(app=app, config=config)

    @property
    def cache(self) -> Cache:
        return self.app_cache


cache_man = CacheManager()
