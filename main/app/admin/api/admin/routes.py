from typing import Optional
from flask import Blueprint, request, jsonify, make_response
from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.users_authenticator import admin_auth
from backend.src.admin_view import AdminView

admin_api_bp = Blueprint('admin_dashboard', __name__)


# noinspection PyTypeChecker
@admin_api_bp.route("/_api/admin/dashboard/<path:path>", methods=["GET", "POST"])
@admin_auth.handle_admin_auth
def admin_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    """

    """
    print(f'CURRENT USER DETAILS: {current_user}')
    print(f'PATH : {path}')

    json_data: dict = request.get_json()
    print(f'JSON Data: {json_data}')
    admin_instance: AdminView = AdminView()

    if path == "dashboard":
        return jsonify(
            {'status': True, 'payload': 'dashboard under development', 'message': 'under development'}), status_codes.status_ok_code

    elif path == "organizations":
        payload: dict = admin_instance.get_all_organizations()
        print(f"payload : {payload}")
        return jsonify(payload), status_codes.status_ok_code

    elif path == "users":
        payload: dict = admin_instance.get_main_organization_users()
        return jsonify(payload), status_codes.status_ok_code

    elif path == "api-keys":
        return jsonify(
            {'status': True, 'payload': 'api_keys under development', 'message': 'under development'}), status_codes.status_ok_code
    elif path == "affiliates":
        return jsonify(
            {'status': True, 'payload': 'affiliates under development', 'message': 'under development'}), status_codes.status_ok_code

    elif path == "accounts":
        return jsonify(
            {'status': True, 'payload': 'accounts under development', 'message': 'under development'}), status_codes.status_ok_code
    elif path == "help-desk":
        return jsonify(
            {'status': True, 'payload': 'uhelp-desk nder development', 'message': 'under development'}), status_codes.status_ok_code
    return jsonify(
            {'status': True, 'payload': 'under development', 'message': 'under development'}), status_codes.status_ok_code


