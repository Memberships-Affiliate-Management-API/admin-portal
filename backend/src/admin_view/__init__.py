from backend.src.admin_requests.api_requests import app_requests
from backend.src.utils import return_ttl
from config import config_instance
from backend.src.cache_manager.cache_manager import cache_man


class AdminView:

    def __init__(self):
        self._login_endpoint: str = '_api/v1/admin/auth/login'
        self._logout_endpoint: str = '_api/v1/admin/auth/logout'
        self._all_org_endpoint: str = '_api/v1/admin/organizations/get-all'
        self._all_api_keys: str = '_api/v1/admin/api-keys/get-all'
        self._uid: str = config_instance.ADMIN_UID
        self._email: str = config_instance.ADMIN_EMAIL
        self._organization_id: str = config_instance.ORGANIZATION_ID

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def login_user(self, email, password) -> dict:
        """
        **login_user**
            will return login token
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, email=email, password=password)
        _request_id = app_requests.schedule_data_send(_endpoint=self._login_endpoint, body=_kwargs)
        while True:
            response = app_requests.get_response(request_id=_request_id)
            if response is not None:
                return response

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def logout_user(self, email: str, token: str) -> dict:
        """
        **logout_user**
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, email=email, token=token)
        _request_id = app_requests.schedule_data_send(_endpoint=self._logout_endpoint, body=_kwargs)
        while True:
            response = app_requests.get_response(request_id=_request_id)
            if response is not None:
                return response

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_all_organizations(self, token: str, domain: str) -> dict:
        """
            **get_all_organizations**

        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, token=token)
        _request_id = app_requests.schedule_data_send(_endpoint=self._all_org_endpoint, body=_kwargs)
        while True:
            response = app_requests.get_response(request_id=_request_id)
            if response is not None:
                return response

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_main_organization_users(self, token: str, domain: str) -> dict:
        """
        **get_main_organization_users**
            returns a list of all users registered to use the API on their websites or blogs

        :param token:
        :param domain:
        return dict: system organization users or clients
        """

        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, token=token)
        _request_id = app_requests.schedule_data_send(_endpoint=self._all_org_endpoint, body=_kwargs)
        while True:
            response = app_requests.get_response(request_id=_request_id)
            if response is not None:
                return response

    @cache_man.cache.memoize(timeout=return_ttl('short'))
    def get_api_keys(self, token: str, domain: str) -> dict:
        """
        **get_api_keys**
            returns a list of all api keys which are on the api

        :param token:
        :param domain:
        return dict: system organization users or clients
        """
        _kwargs: dict = dict(uid=self._uid, organization_id=self._organization_id, domain=domain, token=token)
        _request_id = app_requests.schedule_data_send(_endpoint=self._all_api_keys, body=_kwargs)
        while True:
            response = app_requests.get_response(request_id=_request_id)
            if response is not None:
                return response
