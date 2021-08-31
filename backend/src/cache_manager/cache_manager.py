"""
    **cache Manager**
        this module will handle all requests from this application to other api's

"""
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Callable

from flask_caching import Cache
from config import config_instance


class CacheManager:

    def __init__(self) -> None:
        self.total_cache_calls: int = 0
        self.app_cache: Cache = Cache()

    def init_app(self, app, config):
        self.app_cache.init_app(app=app, config=config)

    @property
    def cache(self) -> Cache:
        self.total_cache_calls += 1
        print(self.total_cache_calls)
        return self.app_cache

    @property
    def size_of(self) -> int:
        """
        **size_of**
            returns the present size of cache
        """
        return self.app_cache.__sizeof__()

    def delete_cache_item(self, func: Callable, kwargs: dict) -> None:
        """
        **deletes a specific cached item**
            clears present cache
        """
        self.app_cache.delete_memoized(f=func, kwargs=kwargs)


cache_man = CacheManager()
