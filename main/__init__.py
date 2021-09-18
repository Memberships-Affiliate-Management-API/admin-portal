from authlib.integrations.flask_client import OAuth
from flask import Flask

from backend.src.admin_requests.api_requests import app_requests
from backend.src.cache_manager.cache_manager import cache_man
from backend.src.security.apps_authenticator import app_auth_micro_service
from config import config_instance


# noinspection DuplicatedCode
def create_app(config_class=config_instance):
    app = Flask(__name__, static_folder="app/resources/static", template_folder="app/resources/templates")
    app.config.from_object(config_class)
    # custom cache manager
    cache_man.init_app(app=app, config=config_class.cache_dict())
    # custom asynchronous api request handler
    app_requests.init_app(app=app)
    # github auth handler
    # oauth.init_app(app=app, cache=cache_man.cache)

    with app.app_context():
        # user facing or public facing api's
        from backend.src.handlers.routes import default_handlers_bp

        # importing admin app blueprints
        from main.app.admin.routes.dashboard import admin_dashboard_bp

        from main.app.admin.routes.home import admin_bp
        from main.app.admin.api.admin.routes import admin_api_bp
        from main.app.admin.api.auth.routes import auth_admin_api_bp

        from _ipn.micro_auth import microservices_ipn_bp

        # admin app handlers
        app.register_blueprint(admin_api_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(admin_dashboard_bp)
        app.register_blueprint(microservices_ipn_bp)

        # admin api
        app.register_blueprint(auth_admin_api_bp)

        # Error Handlers
        app.register_blueprint(default_handlers_bp)
        app.tasks_thread = None
        app.before_first_request(f=app_auth_micro_service.authenticate_with_admin_api)

        # app_auth_micro_service.authenticate_with_admin_api()

    return app
