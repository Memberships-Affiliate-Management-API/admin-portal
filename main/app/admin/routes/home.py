from typing import Optional
from flask import Blueprint, render_template, get_flashed_messages, make_response

from backend.src.custom_exceptions.exceptions import status_codes
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


@admin_bp.route("/<string:path>", methods=["GET"])
def default_routes(path: str) -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    if path == 'robots.txt':
        response = make_response('admin/robots.txt')
        response.headers['content-type'] = 'text/plain'
        return response, status_codes.status_ok_code

    elif path == 'sitemap.xml':
        response = make_response('admin/sitemap.xml')
        response.headers['content-type'] = 'text/xml'
        return response, status_codes.status_ok_code

    elif path == 'favicon.ico':
        response = make_response(render_template('admin/favicon.ico'))
        response.headers['content-type'] = "img/ico"
        return response, status_codes.status_ok_code

    elif path == 'sw.js':
        response = make_response(render_template('admin/scripts/sw.js'))
        response.headers['content-type'] = 'application/javascript'
        return response, status_codes.status_ok_code

