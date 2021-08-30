from flask_caching import Cache
from config import config_instance

app_cache: Cache = Cache(config=config_instance.cache_dict())