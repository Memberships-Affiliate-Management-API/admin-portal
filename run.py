"""
    **ADMIN Application for Memberships & Affiliates Management API**
        This application is intended for use by system administrators of memberships and Affiliates API

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
from config import config_instance
from main import create_app
from backend.src.utils import is_development

app = create_app(config_class=config_instance)

debug = is_development() and config_instance.DEBUG
# Press the green button in the gutter to run the script.

# TODO Add logs handler which can send all errors to memberships and Affiliate Management Slack Channel

if __name__ == '__main__':
    if is_development():
        # NOTE: this is a development server
        app.run(debug=debug, use_reloader=True, host='127.0.0.1', port=int(os.environ.get('PORT', 8082)))
    else:
        app.run(debug=debug, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8082)))


