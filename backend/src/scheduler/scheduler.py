"""
    **scheduler**
        used to dynamically add jobs on a separate thread to complete tasks that should not interfere
        with requests, or requests that takes a long time to complete
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Callable
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from backend.src.utils import create_id as create_unique_id

task_scheduler = BackgroundScheduler()
cron_scheduler = BackgroundScheduler()


def schedule_func(func: Callable, kwargs: dict, delay: int = 10) -> None:
    """
    **schedule_cache_deletion**
        schedule cache deletion such that it occurs sometime time in the future
    :param func:
    :param kwargs:
    :param delay: delay in milliseconds
    :return: None
    """
    twenty_seconds_after = datetime.now() + timedelta(milliseconds=delay)
    job = task_scheduler.add_job(func=func, trigger='date', run_date=twenty_seconds_after, kwargs=kwargs,
                                 id=create_unique_id(), name="schedule_func", misfire_grace_time=360)
    print('job is : ', job)
