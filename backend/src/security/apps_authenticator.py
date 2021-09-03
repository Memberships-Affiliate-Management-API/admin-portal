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
from flask import current_app
from typing import Optional

from backend.src.admin_requests.api_requests import app_requests
from backend.src.scheduler.scheduler import schedule_func
from backend.src.utils import create_id, return_ttl
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
        _kwargs: dict = dict(app_id=self._app_id, domain=self._app_domain, secret_key=self._secret_key)
        self._auth_request_id = app_requests.schedule_data_send(_endpoint=self._micro_services_auth, body=_kwargs)
        schedule_func(func=self.fetch_auth_response, kwargs=dict(), delay=5, job_name='fetch_response')

    def fetch_auth_response(self):
        while self.max_retries:
            try:
                self.auth_details = app_requests.get_response(request_id=self._auth_request_id).get('payload')
                if self.auth_details:
                    self.auth_token = self.auth_details['auth_token']
                    break
            except AttributeError:
                pass
            self.max_retries -= 1
            time.sleep(1)
        self.max_retries = 30


app_auth_micro_service: APPAuthenticator = APPAuthenticator()
