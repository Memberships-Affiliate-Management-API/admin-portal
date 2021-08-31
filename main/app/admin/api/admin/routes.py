from typing import Optional

from flask import Blueprint, request, jsonify

from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.apps_authenticator import app_auth_micro_service
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
    token: str = app_auth_micro_service.auth_token
    domain: str = request.headers.get('referrer')
    # TODO - add user token to current_user and then proceed to use it on the app

    if path == "dashboard":
        return jsonify({'status': True, 'payload': 'dashboard under development',
                        'message': 'under development'}), status_codes.status_ok_code

    elif path == "organizations":
        payload: dict = admin_instance.get_all_organizations(token=token, domain=domain)
        print(f"payload : {payload}")
        return jsonify(payload), status_codes.status_ok_code

    elif path == "users":
        # TODO replace with App Token
        payload: dict = admin_instance.get_main_organization_users(token=token, domain=domain)
        return jsonify(payload), status_codes.status_ok_code

    elif path == "api-keys":
        payload: dict = admin_instance.get_api_keys(token=token, domain=domain)
        return jsonify(payload), status_codes.status_ok_code

    elif path == "affiliates":
        return jsonify({'status': True, 'payload': 'affiliates under development',
                        'message': 'under development'}), status_codes.status_ok_code

    elif path == "accounts":
        return jsonify({'status': True, 'payload': 'accounts under development',
                        'message': 'under development'}), status_codes.status_ok_code

    elif path == "help-desk":
        return jsonify({'status': True, 'payload': 'help-desk under development',
                        'message': 'under development'}), status_codes.status_ok_code

    return jsonify({'status': True, 'payload': 'under development',
                    'message': 'under development'}), status_codes.status_ok_code


