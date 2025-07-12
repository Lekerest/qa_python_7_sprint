import requests
import allure
from helpers import CourierHelper

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

class TestLoginCourier:

    _, [login, password, _] = CourierHelper.register_new_courier_and_return_login_password()

    def test_login_courier(self):
        payload = {
            "login": self.login,
            "password": self.password,
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200

    def test_login_with_validate_two_parameters(self):
        payload = {
            "login": self.login,
            "password": self.password,
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200

    def test_login_with_error_in_login(self):
        payload = {
            "login": "asddfgghjj",
            "password": self.password,
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404

    def test_login_with_error_in_password(self):
        payload = {
            "login": self.login,
            "password": "fgsdsgfdfg",
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404

    def test_login_without_login(self):
        payload = {"password": self.password}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 400

    def test_login_without_password(self):
        payload = {"login": self.login}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 400
