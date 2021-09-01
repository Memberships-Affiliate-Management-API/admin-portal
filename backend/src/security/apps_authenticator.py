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

from typing import Optional

from backend.src.admin_requests.api_requests import app_requests
from backend.src.utils import create_id
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
        self._micro_services_auth: str = "/_ipn/micro-services/auth"
        self.auth_token: Optional[str] = None
        self.max_retries: int = 50

    def __str__(self) -> str:
        return f"<APPAuthenticator app_id: {self._app_id} auth_token: {self.auth_token}"

    def refresh_app_id(self):
        self._app_id = create_id()

    def authenticate_with_admin_api(self):
        """
            **authenticate_with_admin_api**
        """
        if not self._is_running:
            self._is_running = True
            self.refresh_app_id()
            _kwargs: dict = dict(app_id=self._app_id, domain=self._app_domain, secret_key=self._secret_key)
            _request_id: str = app_requests.schedule_data_send(_endpoint=self._micro_services_auth, body=_kwargs)
            print(_request_id)
            while self.max_retries:
                response = app_requests.get_response(request_id=_request_id)

                if response is not None:
                    break
                self.max_retries -= 1

            print(f"responses : {response}")

            if isinstance(response, dict) and response.get('status'):
                self.auth_token = response['payload']['auth_token']



