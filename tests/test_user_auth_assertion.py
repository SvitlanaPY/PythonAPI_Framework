import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        auth_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=auth_data)
        assert response1.status_code == 200, 'Wrong status code'
        # these three asserts are moved to class BaseCase:
        # assert "auth_sid" in response1.cookies, "There is no auth cookie in the response1"
        # assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response1"
        # assert "user_id" in response1.json(), "There is no user id in the response1"

        # self.auth_sid = response1.cookies.get("auth_sid")    # response1.cookies["auth_sid"]
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        # self.token = response1.headers.get("x-csrf-token")   # response1.headers["x-csrf-token"]
        self.token = self.get_header(response1, "x-csrf-token")
        # self.user_id_from_auth_method = response1.json().get("user_id")  # or self.user_id_from_auth_method = response1.json()["user_id"]
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")


    def test_user_auth(self):
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from login-method is not equal to user id from auth-method"
        )
        # assert "user_id" in response2.json(), "There is no user id in the response2"
        # user_id_from_check_method = response2.json()["user_id"]   # user_id_from_check_method = response2.json().get("user_id")
        # assert self.user_id_from_check_method == self.user_id_from_auth_method, "User id from login-method is not equal to user id from auth-method"


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_user_auth(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token}
            )
        elif condition == "no_token":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with {condition}"
        )
        # assert "user_id" in response2.json(), "There is no user id in the response2"
        # user_id_from_check_method = response2.json()["user_id"]   # user_id_from_check_method = response2.json().get("user_id")
        # assert self.user_id_from_check_method == 0, f"User is authorized with {condition}"

# PS D:\AutomationAPI\PythonAPI_Framework> python -m pytest -s tests/test_user_auth_assertion.py
