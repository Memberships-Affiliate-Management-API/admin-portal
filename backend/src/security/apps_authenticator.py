"""
    **apps_authenticator**
        will handle internal application api calls

    **NOTE:**
        this authenticator runs on the api side will have access to all the data classes

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import time

from retry import retry
from flask import current_app
from typing import Optional

from backend.src.admin_requests.api_requests import app_requests
from backend.src.scheduler.scheduler import create_task
from backend.src.utils import create_id, return_ttl
from backend.src.custom_exceptions.exceptions import UnAuthenticatedError
from config import config_instance


class APPAuthenticator:
    """
    **Class APPAuthenticator**
        upon start-up and consequently after that the application must authenticate with the api's
    """

    def __init__(self):
        self._is_running: bool = False
        self._app_id: str = create_id()
        self._app_domain: str = config_instance.ADMIN_APP_BASEURL
        self._secret_key: str = config_instance.SECRET_KEY
        self._micro_services_auth: str = "_ipn/micro-services/auth"
        self.auth_token: Optional[str] = None
        self.max_retries: int = 50
        self._auth_request_id: Optional[str] = None
        self.auth_details: Optional[dict] = None

    def __str__(self) -> str:
        return f"<APPAuthenticator app_id: {self._app_id} auth_token: {self.auth_token}"

    def refresh_app_id(self):
        self._app_id = create_id()

    def authenticate_with_admin_api(self):
        """
            **authenticate_with_admin_api**
        """
        # self.refresh_app_id()
        print('running authenticate')
        _kwargs: dict = dict(app_id=self._app_id, domain=self._app_domain, SECRET_KEY=self._secret_key)
        self._auth_request_id = app_requests.schedule_data_send(_endpoint=self._micro_services_auth, body=_kwargs)
        created_task = create_task(func=self.fetch_auth_response, job_name='fetch_auth_response', kwargs=None)
        print(f'task created: {created_task}')

    @retry(exceptions=UnAuthenticatedError, tries=3, delay=1)
    def fetch_auth_response(self):
        self.auth_details = app_requests.get_response(request_id=self._auth_request_id).get('payload')
        if self.auth_details:
            self.auth_token = self.auth_details['auth_token']
            return None
        raise UnAuthenticatedError()


app_auth_micro_service: APPAuthenticator = APPAuthenticator()
