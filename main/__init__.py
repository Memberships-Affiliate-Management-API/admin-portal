from flask import Flask
from flask_caching import Cache
from config import config_instance
from authlib.integrations.flask_client import OAuth
# TODO: consider upgrading the cache service from version 2 of this api
from backend.src.utils.utils import clear_cache

app_cache: Cache = Cache(config=config_instance.cache_dict())

default_timeout: int = 60 * 60 * 6

# github authenticate - enables developers to easily sign-up to our api
oauth = OAuth()
github_authorize = oauth.register(
    name='github',
    client_id=config_instance.GITHUB_CLIENT_ID,
    client_secret=config_instance.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'})


# noinspection DuplicatedCode
def create_app(config_class=config_instance):
    app = Flask(__name__, static_folder="app/resources/static", template_folder="app/resources/templates")
    app.config.from_object(config_class)

    app_cache.init_app(app=app, config=config_class.cache_dict())
    oauth.init_app(app=app, cache=app_cache)
    # user facing or public facing api's
    from backend.src.default_handlers.routes import default_handlers_bp

    # importing admin app blueprints
    from main.app.admin.routes.dashboard import admin_dashboard_bp
    from main.app.admin.routes.home import admin_bp

    # admin app handlers
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    app.register_blueprint(default_handlers_bp)

    # Clear Cache
    if clear_cache(app=app, cache=app_cache):
        print("Cache Cleared and Starting")

    return app
