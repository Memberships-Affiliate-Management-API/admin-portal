from backend.src.admin_requests.api_requests import app_requests
from config import config_instance


class AdminView:

    def __init__(self):
        self._login_endpoint: str = '_api/v1/admin/users/login'
        self._uid: str = config_instance.ADMIN_UID
        self._email: str = config_instance.ADMIN_EMAIL
        self._organization_id: str = config_instance.ORGANIZATION_ID

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
