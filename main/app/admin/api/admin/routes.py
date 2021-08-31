from typing import Optional

from flask import Blueprint, request, jsonify, make_response
from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.users_authenticator import admin_auth

admin_api_bp = Blueprint('admin_dashboard', __name__)


# noinspection PyTypeChecker
@admin_api_bp.route("/_api/admin/dashboard/<path:path>", methods=["GET", "POST"])
@admin_auth.logged_user
def admin_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    """

    """
    print(current_user)
    return jsonify(
        {'status': True, 'payload': 'under development', 'message': 'under development'}), status_codes.status_ok_code
