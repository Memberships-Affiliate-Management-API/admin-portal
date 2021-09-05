"""
    **system admin data routes**
        this module allows system admin app to get access to data
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import Optional

from flask import Blueprint, request, jsonify

from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes
from main import app_auth_micro_service
from backend.src.security.users_authenticator import admin_auth

admin_api_bp = Blueprint('admin_dashboard', __name__)


# noinspection PyTypeChecker
@admin_api_bp.route("/_api/admin/dashboard/<path:path>", methods=["GET", "POST"])
@admin_auth.handle_admin_auth
def admin_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    """

    """
    json_data: dict = request.get_json()
    admin_instance: AdminView = AdminView()
    # NOTE uses app auth token to authenticate the api call
    app_token: str = app_auth_micro_service.auth_token
    domain: str = request.headers.get('Origin')
    # TODO - add user token to current_user and then proceed to use it on the app

    if path == "dashboard":
        # retrieve dashboard stats from this route
        return jsonify({'status': True, 'payload': 'dashboard under development',
                        'message': 'under development'}), status_codes.status_ok_code

    elif path == "organizations":
        return admin_instance.get_all_organizations(app_token=app_token, domain=domain)

    elif path == "users":
        # TODO replace with App Token
        return admin_instance.get_main_organization_users(app_token=app_token, domain=domain)

    elif path == "api-keys":
        return admin_instance.get_api_keys(app_token=app_token, domain=domain)

    elif path == "affiliates":
        return admin_instance.get_affiliates(app_token=app_token, domain=domain)

    elif path == "accounts":
        return admin_instance.get_all_subscriptions(app_token=app_token, domain=domain)

    elif path == "help-desk":
        return jsonify({'status': True, 'payload': 'help-desk under development',
                        'message': 'under development'}), status_codes.status_ok_code

    return jsonify({'status': True, 'payload': 'under development',
                    'message': 'under development'}), status_codes.status_ok_code
