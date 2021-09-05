"""
    **module admin view**
        allows system admin to control how to access data from admin api
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from json import JSONDecodeError
from typing import Optional

import aiohttp
import requests

from backend.src.cache_manager.cache_manager import cache_man
from backend.src.custom_exceptions.exceptions import EnvironNotSet, RemoteDataError
from backend.src.utils import return_ttl
from config import config_instance


class AdminView:
    """
    **Class AdminView**
        logic needed to get system admin data
    """

    # TODO need to do some refactoring here

    def __init__(self) -> None:
        self._login_endpoint: str = '_api/v1/admin/auth/login'
        self._logout_endpoint: str = '_api/v1/admin/auth/logout'
        self._all_org_endpoint: str = '_api/v1/admin/organizations/get-all'
        self._all_api_keys: str = '_api/v1/admin/api-keys/get-all'
        self._all_affiliates: str = '_api/v1/admin/affiliates/get-all'
        self._get_all_subscriptions: str = '_api/v1/admin/memberships/get-all'
        self._uid: str = config_instance.ADMIN_UID
        self._email: str = config_instance.ADMIN_EMAIL
        self._organization_id: str = config_instance.ORGANIZATION_ID
        self._secret_key: str = config_instance.SECRET_KEY
        self._base_url: str = config_instance.BASE_URL

    @staticmethod
    async def _async_request(_url, json_data, headers) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                return await response.json()

    def _requests_(self, _endpoint: str, body: dict) -> tuple:
        """

        """
        if not bool(self._base_url):
            raise EnvironNotSet()

        _url: str = f'{self._base_url}{_endpoint}'
        if isinstance(body, dict):
            body.update(SECRET_KEY=self._secret_key)
        else:
            body: dict = dict(SECRET_KEY=self._secret_key)

        headers: dict = {'content-type': 'application/json'}
        response = requests.post(url=_url, json=body, headers=headers)

        if 'application/json' == response.headers.get('Content-Type'):
            try:
                status_code = response.status_code
                json_data: dict = response.json()
                print(json_data)

                return json_data, status_code
            except JSONDecodeError as e:
                print(f'ERROR: {e}')
        raise RemoteDataError()

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def login_user(self, email: str, password: str, app_token: str, domain: str) -> tuple:
        """
        **login_user**
            will return login token
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, email=email,
                             password=password, app_token=app_token, domain=domain)

        return self._requests_(_endpoint=self._login_endpoint, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def logout_user(self, email: str, token: str, app_token: str, domain: str) -> tuple:
        """
        **logout_user**
        :param token: user auth token
        :param app_token: application authentication token
        :param domain: domain authenticated
        :param email: user email address
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id,
                             email=email, token=token, app_token=app_token, domain=domain)
        return self._requests_(_endpoint=self._logout_endpoint, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_all_organizations(self, app_token: str, domain: str) -> tuple:
        """
            **get_all_organizations**

        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, app_token=app_token)
        return self._requests_(_endpoint=self._all_org_endpoint, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_main_organization_users(self, app_token: str, domain: str) -> tuple:
        """
        **get_main_organization_users**
            returns a list of all users registered to use the API on their websites or blogs

        :param app_token:
        :param domain:
        return dict: system organization users or clients
        """

        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, app_token=app_token)
        return self._requests_(_endpoint=self._all_org_endpoint, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_all_api_keys(self, app_token: str, domain: str) -> tuple:
        """
        **get_all_api_keys**
            returns a list of all api keys which are on the api

        :param app_token:
        :param domain:
        return dict: system organization users or clients
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, app_token=app_token)
        return self._requests_(_endpoint=self._all_api_keys, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_all_affiliates(self, app_token: str, domain: str) -> tuple:
        """

        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, app_token=app_token)
        return self._requests_(_endpoint=self._all_affiliates, body=_kwargs)

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_all_subscriptions(self, app_token: str, domain: str) -> tuple:
        """

        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, app_token=app_token)
        return self._requests_(_endpoint=self._get_all_subscriptions, body=_kwargs)
