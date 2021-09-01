"""
    handle users and admin authentication
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import datetime
from functools import wraps
from typing import Optional

import jwt
import requests
from flask import current_app, request, url_for, flash

from backend.src.cache_manager.cache_manager import cache_man
from backend.src.custom_exceptions.exceptions import UnAuthenticatedError
from backend.src.utils import return_ttl
from config import config_instance


class AdminAuth:

    def get_admin_user(self) -> dict:
        """
            **get_admin_user**
                return admin_user - uses include on development server

            :return: dict
        """
        return self.get_admin_user_from_admin_api()

    def get_admin_user_from_admin_api(self) -> Optional[dict]:
        """
            **get_api_admin_user_details**
                fetch api admin user details from back-end

        :return: dict -> as user
        """
        _endpoint: str = '_api/v1/admin/users/get'
        _base_url: str = config_instance.ADMIN_APP_BASEURL
        _url: str = f'{_base_url}{_endpoint}'
        _secret_key: str = config_instance.SECRET_KEY
        _auth_token: str = self.encode_auth_token(uid=_secret_key)
        _organization_id: str = config_instance.ORGANIZATION_ID
        _uid: str = config_instance.ADMIN_UID
        user_data: dict = dict(SECRET_KEY=_secret_key, auth_token=_auth_token,
                               organization_id=_organization_id, uid=_uid)

        _headers = dict(content_type='application/json', domain=config_instance.ADMIN_APP_BASEURL)
        response = requests.post(url=_url, json=user_data, headers=_headers)

        response_data: dict = response.json()

        if response_data.get('status') is True:
            return response_data.get('payload')
        return None

    @staticmethod
    def get_config_admin_user_details() -> tuple:
        """
            **get_config_admin_user_details**
                return admin user details from config_instance
        :return:
        """
        uid: str = config_instance.ADMIN_UID
        organization_id: str = config_instance.ORGANIZATION_ID
        admin_email: str = config_instance.ADMIN_EMAIL
        names: str = config_instance.ADMIN_NAMES
        surname: str = config_instance.ADMIN_SURNAME
        password: str = config_instance.ADMIN_PASSWORD
        cell: str = config_instance.ADMIN_CELL
        return admin_email, cell, names, organization_id, password, surname, uid

    @staticmethod
    def is_app_admin(current_user: any) -> Optional[bool]:
        """
            **is_app_admin**
                checks if user is app admin - meaning admin for main organization for the API

        :param current_user:
        :return: boolean indicating if current user is admin or not
        """
        if current_user is None:
            return None

        if isinstance(current_user, dict):
            return current_user and current_user.get('uid') and (
                    current_user.get('organization_id') == config_instance.ORGANIZATION_ID)

        # noinspection PyUnresolvedReferences
        return current_user and current_user.uid and (current_user.organization_id == config_instance.ORGANIZATION_ID)

    @staticmethod
    def encode_auth_token(uid: str) -> str:
        """
        **encode_auth_token**
            Generates the Auth Token for JWT Authentication

        **PARAMETERS**
            :param: uid -> string - unique user id
            :return: string -> auth-token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': uid
            }
            token = jwt.encode(payload=payload, key=str(current_app.config.get('SECRET_KEY')), algorithm='HS256')
            return token
        except jwt.InvalidAlgorithmError:
            raise UnAuthenticatedError(description="system error login in please inform admin")

    @staticmethod
    def decode_auth_token(auth_token):
        """
        **decode_auth_token**
            Decodes the auth token

        **PARAMETERS**
            :param auth_token:
            :return: string -> uid
        """
        try:
            payload = jwt.decode(jwt=auth_token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise UnAuthenticatedError(description="Expired token signature please login again")
        except jwt.InvalidTokenError:
            raise UnAuthenticatedError(description="Invalid login credentials please login again")

    @staticmethod
    @cache_man.app_cache.memoize(timeout=return_ttl('short'))
    def send_get_user_request(uid: str) -> Optional[dict]:
        """
        **send_get_user_request**
            send request for user over api and return user dict

        **PARAMETERS**
            :param uid:
            :return: dict -> user record
        """
        # admin api base url
        _base_url: str = config_instance.BASE_URL
        _user_endpoint: str = "_api/v1/admin/auth/get-admin-user"
        _organization_id: str = config_instance.ORGANIZATION_ID
        _data: dict = dict(organization_id=_organization_id, uid=uid, SECRET_KEY=config_instance.SECRET_KEY)
        response = requests.post(url=f"{_base_url}{_user_endpoint}", json=_data)
        response_data: dict = response.json()
        if response_data['status']:
            return response_data['payload']
        return None

    def handle_admin_auth(self, func):
        """
            **handle_admin_auth**
                handles authentication on html routes for users on client dashboard
                and admin dashboard
            :param func:
        """

        # noinspection PyBroadException
        @wraps(func)
        def decorated(*args, **kwargs):

            token: Optional[str] = None
            # print('token headers: {}'.format(request.headers))
            if 'x-access-token' in request.headers:
                token = request.headers.get('x-access-token')

            # NOTE: if running on development server by-pass authentication and return admin user
            if not bool(token):
                raise UnAuthenticatedError(description="You are not logged in please login to proceed")

            try:
                uid: Optional[str] = self.decode_auth_token(auth_token=token)
                if bool(uid):
                    # NOTE: using client api to access user details
                    current_user: Optional[dict] = self.send_get_user_request(uid=uid)
                    if not isinstance(current_user, dict):
                        raise UnAuthenticatedError(description="Unable to authenticate user")
                else:
                    raise UnAuthenticatedError(description="Unable to authenticate user")

            except jwt.DecodeError:
                raise UnAuthenticatedError(description="Error with your login credentials please login again")

            except Exception:
                raise UnAuthenticatedError(description="Error with your login credentials please login again")
            return func(current_user, *args, **kwargs)

        return decorated

    def logged_admin_user(self, func):
        """
            **logged_admin_user**
                only accesses the record of the logged in user without denying access to the route
                if user is not logged in.
        :param func: route to wrap
        :return: wrapped function
        """

        @wraps(func)
        def decorated(*args, **kwargs):
            current_user: Optional[dict] = None
            # NOTE: by passes authentication and returns admin user as authenticated
            # user on development
            # if is_development():
            #     # TODO use api here instead of user model
            #
            #     current_user: Optional[dict] = get_admin_user()
            #     return func(current_user, *args, **kwargs)
            print(request.headers)
            if 'x-access-token' in request.headers:
                token: Optional[str] = request.headers['x-access-token']

                print('token : ', token)
                if bool(token):
                    try:
                        uid: Optional[str] = self.decode_auth_token(auth_token=token)
                        if bool(uid):
                            user_instance: Optional[dict] = self.send_get_user_request(uid=uid)
                            if isinstance(user_instance, dict):
                                current_user: dict = user_instance
                        else:
                            pass
                    except jwt.DecodeError:
                        # If user not logged in do nothing
                        raise UnAuthenticatedError(description="Error with your login credentials please login again")
                else:
                    pass
            return func(current_user, *args, **kwargs)

        return decorated


admin_auth: AdminAuth = AdminAuth()

if __name__ == '__main__':
    """
        NOTE: fast testing of functions here 
    """
    pass
