from typing import Optional
from flask import Blueprint, render_template, get_flashed_messages, make_response, url_for, flash

from backend.src.custom_exceptions.exceptions import status_codes
from backend.src.security.users_authenticator import admin_auth

admin_bp = Blueprint("admin_home", __name__)


@admin_bp.route("/", methods=["GET"])
@admin_auth.logged_admin_user
def admin_home(current_user: Optional[dict]) -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    get_flashed_messages()
    if admin_auth.is_app_admin(current_user=current_user):
        return render_template('admin/home.html', current_user=current_user)
    return render_template('admin/home.html'), status_codes.status_ok_code


@admin_bp.route("/login", methods=["GET"])
def login() -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    return render_template('admin/login.html'), status_codes.status_ok_code


@admin_bp.route("/logout", methods=["GET"])
def logout() -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    get_flashed_messages()
    return render_template('admin/logout.html')


@admin_bp.route("/<string:path>", methods=["GET"])
def default_routes(path: str) -> tuple:
    """
        **admin_home**
            admin home page
    :return:
    """
    if path == 'robots.txt':
        _host_url: str = url_for('admin_home.default_routes', path='sitemap.xml', _external=True)
        response = make_response(render_template('admin/robots.txt', host_url=_host_url))
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
