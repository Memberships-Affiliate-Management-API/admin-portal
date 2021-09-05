from flask import Blueprint, request, jsonify, make_response
from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.apps_authenticator import app_auth_micro_service

auth_admin_api_bp = Blueprint('admin_auth_api', __name__)


@auth_admin_api_bp.route('/api/v1/user/<string:path>', methods=["POST"])
def auth_api(path: str) -> tuple:
    """

    """
    admin_view: AdminView = AdminView()
    # Application authentication token
    app_token: str = app_auth_micro_service.auth_token
    domain: str = request.headers.get('Origin')

    if path == 'login':
        json_data: dict = request.get_json()
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        return admin_view.login_user(email=email, password=password, app_token=app_token, domain=domain)

    elif path == "logout":
        json_data: dict = request.get_json()
        email: str = json_data.get('email')
        token: str = json_data.get('token')
        return admin_view.logout_user(email=email, token=token, app_token=app_token, domain=domain)
