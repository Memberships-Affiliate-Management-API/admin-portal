from flask import Blueprint, request, jsonify
from backend.src.admin_view import AdminView
from backend.src.custom_exceptions.exceptions import status_codes

user_api_bp = Blueprint('user_api', __name__)


@user_api_bp.route('/api/v1/user/<string:path>', methods=["POST"])
def users_api(path: str) -> tuple:
    """

    """
    print('user api : ', path)
    admin_view: AdminView = AdminView()
    if path == 'login':
        json_data: dict = request.get_json()
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        print(email, password)
        response = admin_view.login_user(email=email, password=password)

        return jsonify({'status': True, 'payload': admin_view.login_user(email=email, password=password),
                        'message': 'successfully logged in'}), status_codes.status_ok_code

