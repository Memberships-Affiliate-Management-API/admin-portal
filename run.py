"""
    **ADMIN Application for Memberships & Affiliates Management API**
        This application is intended for use by system administrators of memberships and Affiliates API

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from threading import Thread
import os
from flask import Response
from config import config_instance
from main import create_app
from backend.src.utils import is_development
from tasks import run_tasks

app = create_app(config_class=config_instance)

debug = is_development() and config_instance.DEBUG


# Press the green button in the gutter to run the script.

# TODO #1 Add logs handler which can send all errors to memberships and Affiliate Management Slack Channel

@app.before_request
def create_thread() -> None:
    """
    """
    try:
        if not isinstance(app.tasks_thread, Thread):
            app.tasks_thread = Thread(target=run_tasks)
            print('Tasks Thread Created')
    except AttributeError as e:
        print(str(e))
    finally:
        return None


@app.after_request
def run_thread(response: Response) -> Response:
    """

    """
    try:
        if isinstance(app.tasks_thread, Thread) and not app.tasks_thread.is_alive():
            app.tasks_thread.start()
        print(str(app.tasks_thread))
    except RuntimeError as e:
        print(str(e))
        app.tasks_thread = Thread(target=run_tasks)
        app.tasks_thread.start()
    finally:
        return response


if __name__ == '__main__':
    if is_development():
        # NOTE: this is a development server
        app.run(debug=debug, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8082)))
    else:
        app.run(debug=debug, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8082)))
