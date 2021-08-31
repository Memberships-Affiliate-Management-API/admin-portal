from flask import Flask
from config import config_instance
from authlib.integrations.flask_client import OAuth
from backend.src.admin_requests.api_requests import app_requests
from backend.src.cache_manager.cache_manager import cache_man
from backend.src.scheduler.scheduler import task_scheduler

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

    # custom cache manager
    cache_man.init_app(app=app, config=config_class.cache_dict())
    # custom asynchronous api request handler
    app_requests.init_app(app=app)

    # github auth handler
    oauth.init_app(app=app, cache=cache_man.cache)

    # user facing or public facing api's
    from backend.src.handlers.routes import default_handlers_bp

    # importing admin app blueprints
    from main.app.admin.routes.dashboard import admin_dashboard_bp

    from main.app.admin.routes.home import admin_bp
    from main.app.admin.api.admin.routes import admin_api_bp
    from main.app.admin.api.users.routes import user_api_bp

    # admin app handlers
    app.register_blueprint(admin_api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_dashboard_bp)

    # admin api
    app.register_blueprint(user_api_bp)

    # Error Handlers
    app.register_blueprint(default_handlers_bp)

    task_scheduler.start()

    return app
