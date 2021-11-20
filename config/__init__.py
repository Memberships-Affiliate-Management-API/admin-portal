"""
    **Flask App Configuration Settings**
    *Python Version 3.8 and above*
    Used to setup environment variables for python flask app
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import os
import typing
# noinspection PyPackageRequirements
from decouple import config
import datetime


class Config:
    """
        **APP Configuration Settings**
            configuration variables for setting up the application
    """
    # TODO - Clean up configuration settings
    def __init__(self) -> None:
        self.PROJECT: str = os.environ.get("PROJECT") or config("PROJECT")
        self.APP_NAME: str = os.environ.get("APP_NAME") or config("APP_NAME")

        self.BASE_URL: str = os.environ.get("BASE_URL") or config("BASE_URL")
        self.CLIENT_APP_BASEURL = os.environ.get("CLIENT_APP_BASEURL") or config("CLIENT_APP_BASEURL")
        self.ADMIN_APP_BASEURL: str = os.environ.get("ADMIN_APP_BASEURL") or config("ADMIN_APP_BASEURL")
        self.GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        self.SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
        self.DEBUG: bool = False

        self.ORGANIZATION_ID: str = os.environ.get("ORGANIZATION_ID") or config("ORGANIZATION_ID")
        self.ADMIN_UID: str = os.environ.get("ADMIN_UID") or config("ADMIN_UID")
        self.ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
        self.ADMIN_NAMES: str = os.environ.get("ADMIN_NAMES") or config("ADMIN_NAMES")
        self.ADMIN_SURNAME: str = os.environ.get("ADMIN_SURNAME") or config("ADMIN_SURNAME")
        self.ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD") or config("ADMIN_PASSWORD")
        self.ADMIN_CELL: str = os.environ.get("ADMIN_CELL") or config("ADMIN_CELL")

        self.UTC_OFFSET = datetime.timedelta(hours=2)
        self.DATASTORE_TIMEOUT: int = 360  # seconds 6 minutes
        self.DATASTORE_RETRIES: int = 3  # total retries when saving to datastore

        self.CURRENCY: str = "USD"
        # TODO obtain correct paypal client ids

        self.IS_PRODUCTION: bool = True
        self.CACHE_TYPE: str = "redis"
        self.CACHE_REDIS_HOST: str = os.environ.get("CACHE_REDIS_HOST") or config("CACHE_REDIS_HOST")
        self.CACHE_REDIS_PORT: str = os.environ.get("CACHE_REDIS_PORT") or config("CACHE_REDIS_PORT")
        self.CACHE_REDIS_PASSWORD: str = os.environ.get("CACHE_REDIS_PASSWORD") or config("CACHE_REDIS_PASSWORD")
        self.CACHE_DEFAULT_TIMEOUT: int = 60 * 60 * 6
        self.PAYMENT_PLANS_SCHEDULES: typing.List[str] = ['monthly', 'quarterly', 'annually']
        self.PAYMENT_PLANS_PAYMENT_DAYS: typing.List[int] = [1, 2, 3, 4, 5]
        self.MINIMUM_WITHDRAWAL_AMOUNT_USD: int = 3000  # amount is in cents 30 Dollars

        self.ENV: str = "production"
        self.TEMPLATES_AUTO_RELOAD: bool = True
        self.PREFERRED_URL_SCHEME: str = "https"

        self.RABBIT_MQ_URL: str = os.environ.get("RABBIT_MQ_URL") or config('RABBIT_MQ_URL')

        # NOTE : setting IS_PRODUCTION here - could find a better way of doing this rather
        # than depending on the OS
        if "DESKTOP-B52R0UU" == os.environ.get('COMPUTERNAME'):
            self.DEBUG = True
            self.IS_PRODUCTION = False
            self.ENV = "development"
            self.PROPAGATE_EXCEPTIONS: bool = True
            self.PRESERVE_CONTEXT_ON_EXCEPTION: bool = True
            self.EXPLAIN_TEMPLATE_LOADING: bool = False
            self.PREFERRED_URL_SCHEME: str = "http"
            self.TESTING: bool = True
            # TODO - set Cache to MEM_CACHE and then setup the server URI, applicable on version 2

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def cache_dict(self) -> dict:
        """
            **cache_dict**
            returns cache settings
        :return: dict
        """
        # TODO : add support for redis cache instead of using simple cache
        return {
            "CACHE_TYPE": self.CACHE_TYPE,
            "CACHE_REDIS_HOST": self.CACHE_REDIS_HOST,
            "CACHE_REDIS_PORT": self.CACHE_REDIS_PORT,
            "CACHE_REDIS_PASSWORD": self.CACHE_REDIS_PASSWORD
        }


config_instance: Config = Config()
# Note: Config is a singleton - this means it cannot be redeclared anywhere else
del Config
