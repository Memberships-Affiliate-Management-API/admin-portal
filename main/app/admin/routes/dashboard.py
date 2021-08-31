from typing import Optional
from flask import Blueprint, render_template, url_for, get_flashed_messages, redirect, flash
from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.users_authenticator import admin_auth


admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@admin_auth.logged_user
def admin_dashboard(current_user: Optional[dict]) -> tuple:
    """
        **admin_dashboard**
            home route for system admin dashboard
    :param current_user:
    :return:
    """
    get_flashed_messages()
    if not admin_auth.is_app_admin(current_user=current_user):
        flash('This area is not for public use sorry')
        return redirect(url_for('admin_home.login'))

    return render_template('admin/dashboard.html', current_user=current_user), status_codes.status_ok_code


# noinspection PyTypeChecker
@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@admin_auth.logged_user
def admin_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    """
            **admin_dashboard_routes**
                home route for system admin dashboard

        :param current_user:
        :param path:
        :return:
    """

    get_flashed_messages()

    if not admin_auth.is_app_admin(current_user=current_user):
        flash('This area is not for public use sorry')
        return redirect(url_for('admin_home.login'))

    if path == "affiliates":
        return render_template('admin/affiliates.html', current_user=current_user), status_codes.status_ok_code
    elif path == "users":
        return render_template('admin/users.html', current_user=current_user), status_codes.status_ok_code
    elif path == "organizations":
        return render_template('admin/organizations.html', current_user=current_user), status_codes.status_ok_code
    elif path == "api-keys":
        return render_template('admin/api_keys.html', current_user=current_user), status_codes.status_ok_code
    elif path == "accounts":
        return render_template('admin/accounts.html', current_user=current_user), status_codes.status_ok_code
    elif path == "help-desk":
        return render_template('admin/helpdesk.html', current_user=current_user), status_codes.status_ok_code
