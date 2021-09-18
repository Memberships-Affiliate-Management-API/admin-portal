"""
    **api requests**
        this module will handle all requests from this application to other api's

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import asyncio
from typing import Optional, List

import aiohttp

from backend.src.cache_manager.cache_manager import cache_man
from backend.src.custom_exceptions.exceptions import EnvironNotSet
from backend.src.scheduler.scheduler import create_task
from backend.src.utils import create_id, return_ttl


class APIRequests:
    """
        **Class APIRequests**
            this class handles creating api calls then scheduling them and handles results as they are
            returned asynchronously.

        to make a request schedule a request with schedule_data_send
        obtain the request id then after a while check if the request has been returned with get_response
        using the _request_id
    """

    def __init__(self):
        """
        **initializing requests**
        """
        self._base_url: Optional[str] = None
        self._secret_key: Optional[str] = None
        self._responses_queue: List[Optional[dict]] = []
        self._event_loop = None

    def init_app(self, app):
        self._base_url: str = app.config.get('BASE_URL')
        self._secret_key: str = app.config.get('SECRET_KEY')

    @staticmethod
    async def _async_request(_url, json_data, headers) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                return await response.json()

    def _request(self, _url: str, json_data: dict, headers: dict) -> None:
        """
        :param _url:
        :param json_data:
        :param headers:
        :return:
        """
        # obtain the _request_id to be used as an identifier for this request
        _request_id: str = headers.get('_request_id')
        response = asyncio.run(self._async_request(_url=_url, json_data=json_data, headers=headers))
        print(f"fetched response : {response}")

        # compiling a response dict to contain the _request_id and the returned results of the request
        self._responses_queue.append(dict(_request_id=_request_id, response=response))

    def schedule_data_send(self, _endpoint: Optional[str], body: Optional[dict] = None) -> str:
        """
        **schedule_data_send**
            schedule to send data without expecting a response, as
            responses will be stored on self._responses

        :param _endpoint:
        :param body:
        :return: str -> request_id
        """
        if not bool(self._base_url):
            raise EnvironNotSet()

        _url: str = f'{self._base_url}{_endpoint}'
        if isinstance(body, dict):
            body.update(SECRET_KEY=self._secret_key)
        else:
            body: dict = dict(SECRET_KEY=self._secret_key)
        headers: dict = {'content-type': 'application/json'}
        _request_id: str = create_id()
        # updating the request headers with the _request_id
        headers.update(_request_id=_request_id)
        _kwargs: dict = dict(_url=_url, json_data=body, headers=headers)
        # Scheduling the request to run later and then continue
        create_task(func=self._request, job_name=_request_id, kwargs=_kwargs)
        # returning the _request_id so it can be used to retrieve the results at a later stage
        return _request_id

    @cache_man.cache.memoize(timeout=return_ttl('short'), cache_none=False)
    def get_response(self, request_id: str) -> Optional[dict]:
        """
        **get_response**
            from responses_queue retrieve response
            as a result of caching a request can be obtained multiple times from response _queue as it would be cached
        :return: dict -> containing response or None - None wont be cached
        """
        if isinstance(self._responses_queue, list) and len(self._responses_queue):
            # at Best will return None if response not found
            try:
                _response = [_response.get('response') for _response in self._responses_queue if _response.get('_request_id') == request_id][0] or None
                print(f"response found : {_response}")
                return _response
            except IndexError:
                # continue as there is nothing to do
                pass

        # Note: None results will not be cached
        return None


app_requests: APIRequests = APIRequests()
