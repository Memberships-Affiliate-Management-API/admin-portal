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


def schedule_func(func: Callable, kwargs: dict, delay: int = 10, job_name: str = "schedule_func") -> None:
    """
    **schedule_cache_deletion**
        schedule cache deletion such that it occurs sometime time in the future
    :param func:
    :param kwargs:
    :param job_name: "schedule_func"
    :param delay: delay in milliseconds
    :return: None
    """

    job_exists: list = [job for job in task_scheduler.get_jobs() if str(job).startswith(job_name)]
    if job_exists:
        return None

    delayed: datetime = datetime.now() + timedelta(milliseconds=delay)

    job = task_scheduler.add_job(func=func, trigger='date', run_date=delayed, kwargs=kwargs,
                                 id=create_unique_id(), name=job_name, misfire_grace_time=360)

