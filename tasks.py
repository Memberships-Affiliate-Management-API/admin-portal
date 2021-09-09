import asyncio
from backend.src.scheduler.scheduler import task_scheduler


async def main():
    while True:
        all_jobs = task_scheduler.get_jobs()
        for job in all_jobs:
            print(f'Admin Running Job : {job}')
            job.run()
            task_scheduler.cancel_job(job)
        await asyncio.sleep(30)


if __name__ == '__main':
    print('Admin Starting Task Scheduler')
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Exception Thrown by Admin Task Scheduler : {e}')
