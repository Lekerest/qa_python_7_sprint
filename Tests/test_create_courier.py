import requests
import allure
from helpers import CourierHelper

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestCreateCourier:

    @allure.title("Создание курьера")
    @allure.description("Проверка, что курьера можно успешно создать с валидными данными")
    def test_create_courier(self):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }
        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        if response.status_code == 201:
            CourierHelper.created_couriers.append((payload["login"], payload["password"]))
        with allure.step("Проверка, что курьер успешно создан"):
            assert response.status_code == 201, f"Курьер не был создан, {response.status_code}"

    @allure.title("Создание двух одинаковых курьеров")
    @allure.description("Проверка, что нельзя создать двух курьеров с одинаковыми логином, паролем и именем")
    def test_error_if_create_two_identical_couriers(self, create_courier):
        response, [login, password, first_name] = create_courier
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        with allure.step("Повторная попытка создать курьера с теми же данными"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        with allure.step("Проверка, что возвращается ошибка 409"):
            assert response.status_code == 409, "Должна быть ошибка 409 на создание дублирующегося курьера"

    @allure.title("Создание курьера с обязательными полями")
    @allure.description("Проверка, что курьер создается если передать обязательные поля, логин и пароль")
    def test_successful_registration_with_two_parameters(self):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "password": CourierHelper.generate_random_string(10)
        }
        with allure.step("Создание курьера только с обязательными полями"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        if response.status_code == 201:
            CourierHelper.created_couriers.append((payload["login"], payload["password"]))
        with allure.step("Проверка, что курьер успешно создан"):
            assert response.status_code == 201, "Курьер не создался при передаче 2-ух обязательных полей"

    @allure.title("Ошибка при создании без логина")
    @allure.description("Проверка, что при отсутствии логина возвращается ошибка 400")
    def test_error_without_login(self):
        payload = {
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }
        with allure.step("Попытка регистрации без логина"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        with allure.step("Проверка, что возвращается ошибка 400"):
            assert response.status_code == 400, "Попытка регистрации без логина, должна быть ошибка 400"

    @allure.title("Ошибка при создании без пароля")
    @allure.description("Проверка, что при отсутствии пароля возвращается ошибка 400")
    def test_error_without_password(self):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }
        with allure.step("Попытка регистрации без пароля"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        with allure.step("Проверка, что возвращается ошибка 400"):
            assert response.status_code == 400, "Попытка регистрации без пароля, должна быть ошибка 400"

    @allure.title("Проверка кода ответа при успешной регистрации")
    @allure.description("Проверка, что при успешной регистрации возвращается статус 201")
    def test_status_code_registration(self, create_courier):
        response, _ = create_courier
        with allure.step("Проверка, что код ответа равен 201"):
            assert response.status_code == 201, "Курьер не зарегистрировался"

    @allure.title("Проверка тела ответа при успешной регистрации")
    @allure.description("Проверка, что при успешной регистрации возвращается JSON {'ok': true}")
    def test_registration_response_answer(self, create_courier):
        response, _ = create_courier
        with allure.step("Проверка, что тело ответа содержит {'ok': true}"):
            assert response.json() == {"ok": True}, "Ответ сервера не соответствует ожидаемому {'ok': true}"

    @allure.title("Ошибка при регистрации с уже существующим логином")
    @allure.description("Проверка, что при повторной регистрации с тем же логином возвращается ошибка 409")
    def test_error_with_identical_login(self, create_courier):
        response, [login, _, _] = create_courier
        payload = {
            "login": login,
            "password": CourierHelper.generate_random_string(10),
        }
        with allure.step("Попытка регистрации с уже существующим логином"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        with allure.step("Проверка, что возвращается ошибка 409"):
            assert response.status_code == 409, "Должна быть ошибка 409 на создание курьера с тем же логином"
