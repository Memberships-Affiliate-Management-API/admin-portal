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

from backend.src.scheduler.scheduler import task_scheduler


def run_tasks():
    print(f'running tasks...')
    task_scheduler.run_all(delay_seconds=5)
    task_scheduler.clear()
    print('done running tasks')
