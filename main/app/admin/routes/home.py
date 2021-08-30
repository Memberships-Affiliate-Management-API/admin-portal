from typing import Optional
from flask import Blueprint, render_template, get_flashed_messages
from backend.src.security.users_authenticator import handle_users_auth, is_app_admin, logged_user

admin_bp = Blueprint("admin_home", __name__)


@admin_bp.route("/", methods=["GET"])
@logged_user
def admin_home(current_user: Optional[dict]) -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    get_flashed_messages()
    if is_app_admin(current_user=current_user):
        return render_template('admin/home.html', current_user=current_user)
    return render_template('admin/login.html')



