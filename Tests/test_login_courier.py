import requests
import allure
from helpers import CourierHelper

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestLoginCourier:

    login_data = CourierHelper.register_new_courier_and_return_login_password()
    login = login_data[1][0]
    password = login_data[1][1]

    @allure.title("Авторизация курьера с валидными данными")
    @allure.description("Проверка успешной авторизации курьера при валидном логине и пароле")
    def test_login_courier(self):
        payload = {"login": self.login, "password": self.password}
        with allure.step("Отправка запроса авторизации с валидными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что статус ответа 200"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Авторизация не удалась."

    @allure.title("Авторизация с передачей всех обязательных полей")
    @allure.description("Проверка, что для авторизации нужны логин и пароль")
    def test_login_with_validate_two_parameters(self):
        payload = {"login": self.login, "password": self.password}
        with allure.step("Отправка запроса авторизации с логином и паролем"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что статус ответа 200"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Обязательные поля должны быть переданы."

    @allure.title("Ошибка при неверном логине")
    @allure.description("Проверка ошибки 404 при несуществующем логине")
    def test_login_with_error_in_login(self):
        payload = {"login": "asddfgghjj", "password": self.password}
        with allure.step("Отправка запроса авторизации с неверным логином"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что возвращается ошибка 404"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}. Ошибка при неверном логине."

    @allure.title("Ошибка при неверном пароле")
    @allure.description("Проверка ошибки 404 при неправильном пароле")
    def test_login_with_error_in_password(self):
        payload = {"login": self.login, "password": "fgsdsgfdfg"}
        with allure.step("Отправка запроса авторизации с неверным паролем"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что возвращается ошибка 404"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}. Ошибка при неверном пароле."

    @allure.title("Ошибка при отсутствии логина")
    @allure.description("Проверка ошибки 400 при отсутствии поля 'login'")
    def test_login_without_login(self):
        payload = {"password": self.password}
        with allure.step("Отправка запроса авторизации без логина"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что возвращается ошибка 400"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}. Нет поля 'login'."

    @allure.title("Ошибка при отсутствии пароля")
    @allure.description("Проверка ошибки 400 при отсутствии поля 'password'")
    def test_login_without_password(self):
        payload = {"login": self.login}
        with allure.step("Отправка запроса авторизации без пароля"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что возвращается ошибка 400"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}. Нет поля 'password'."

    @allure.title("Ошибка авторизации несуществующего курьера")
    @allure.description("Проверка ошибки 404 при несуществующем курьере")
    def test_login_with_nonexistent_courier(self):
        payload = {"login": "fgsdsgfdfg", "password": "fgsdsgfdfg"}
        with allure.step("Отправка запроса авторизации несуществующего курьера"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что возвращается ошибка 404"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}. Курьер не существует."

    @allure.title("Проверка поля 'id' в успешном ответе")
    @allure.description("Проверка, что при успешной авторизации в ответе есть 'id'")
    def test_login_response_text(self):
        payload = {"login": self.login, "password": self.password}
        with allure.step("Отправка запроса авторизации"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        with allure.step("Проверка, что в теле ответа присутствует поле 'id'"):
            response_json = response.json()
            assert "id" in response_json, f"В ответе нет 'id': {response_json}. Должен быть идентификатор курьера."
