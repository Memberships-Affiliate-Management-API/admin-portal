"""
    **Microservices Auth Endpoint**
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac

from flask import Blueprint, jsonify, request

from backend.src.custom_exceptions.exceptions import status_codes, UnAuthenticatedError
from backend.src.utils import return_ttl, is_development
from config import config_instance
from backend.src.cache_manager.cache_manager import cache_man
microservices_ipn_bp = Blueprint("microservices_ipn", __name__)


@microservices_ipn_bp.route('/_ipn/micro-services/verify-app-id', methods=["POST"])
# @cache_man.cache.cached(timeout=return_ttl('short'), unless=is_development(), cache_none=False)
def verify_app_id() -> tuple:
    """
    **verify_app_id**
        The API will try to validate the app_id, this application will only verify the app_id
        if it can also verify the identity of the api server through its domain and also the secret key
    """
    json_data: dict = request.get_json()
    domain: str = json_data.get('domain')
    app_id: str = json_data.get('app_id')
    secret_key: str = json_data.get('secret_key')

    _secret_key: str = config_instance.SECRET_KEY
    _admin_domain: str = config_instance.ADMIN_APP_BASEURL

    admin_domain_compare: bool = hmac.compare_digest(domain, _admin_domain)
    secret_key_compare: bool = hmac.compare_digest(secret_key, _secret_key)

    _payload: dict = dict(domain=domain, app_id=app_id, secret_key=secret_key)

    if admin_domain_compare and secret_key_compare:
        return jsonify({'status': True, 'payload': _payload, 'message': 'app id verified'}), status_codes.status_ok_code
    raise UnAuthenticatedError()
