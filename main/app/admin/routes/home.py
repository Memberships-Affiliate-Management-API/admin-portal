from typing import Optional
from flask import Blueprint, render_template, url_for, get_flashed_messages
from security.users_authenticator import handle_users_auth


admin_bp = Blueprint("admin_home", __name__)


@admin_bp.route("/", methods=["GET"])
@handle_users_auth
def admin_home(current_user: Optional[dict]) -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    get_flashed_messages()
    return render_template('admin/home.html')


