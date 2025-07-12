import requests
import allure
from helpers import CourierHelper

class TestCreateCourier:

################## курьера можно создать; ##################
    @allure.title("Создание курьера")
    @allure.description("Проверка, что курьера можно успешно создать с валидными данными")
    def test_create_courier(self, create_courier):
        response, [login, password, first_name] = create_courier
        assert login and password and first_name, "Регистрация курьера не удалась — один из параметров пуст"

################## нельзя создать двух одинаковых курьеров; ##################
    @allure.title("Создание двух одинаковых курьеров")
    @allure.description("Проверка, что нельзя создать двух курьеров с одинаковыми логином, паролем и именем")
    def test_error_if_create_two_identical_couriers(self, create_courier):
        response, [login, password, first_name] = create_courier
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 409, "Должна быть ошибка 409 на создание дублирующегося курьера"

################## чтобы создать курьера, нужно передать в ручку все обязательные поля; ##################
    @allure.title("Создание курьера с обязательными полями")
    @allure.description("Проверка, что курьер создается если передать обязательные поля, логин и пароль")
    def test_successful_registration_with_two_parameters(self):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "password": CourierHelper.generate_random_string(10)
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 201, "Курьер не создался при передаче 2-ух обязательных полей"
        if response.status_code == 201:
            CourierHelper.created_couriers.append((payload["login"], payload["password"]))

################## если одного из полей нет, запрос возвращает ошибку; ##################
    @allure.title("Ошибка при создании без логина")
    @allure.description("Проверка, что при отсутствии логина возвращается ошибка 400")
    def test_error_without_login(self):
        payload = {
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 400, "Попытка регистрации без логина, должна быть ошибка 400"

################## если одного из полей нет, запрос возвращает ошибку; ##################
    @allure.title("Ошибка при создании без пароля")
    @allure.description("Проверка, что при отсутствии пароля возвращается ошибка 400")
    def test_error_without_password(self):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 400, "Попытка регистрации без пароля, должна быть ошибка 400"

################## запрос возвращает правильный код ответа; ##################
    @allure.title("Проверка кода ответа при успешной регистрации")
    @allure.description("Проверка, что при успешной регистрации возвращается статус 201")
    def test_status_code_registration(self, create_courier):
        response, [login, password, first_name] = create_courier
        assert response.status_code == 201, "Курьер не зарегистрировался"

################## успешный запрос возвращает {"ok":true}; ##################
    @allure.title("Проверка тела ответа при успешной регистрации")
    @allure.description("Проверка, что при успешной регистрации возвращается JSON {'ok': true}")
    def test_registration_response_answer(self, create_courier):
        response, [login, password, first_name] = create_courier
        assert response.json() == {"ok": True}, "Ответ сервера не соответствует ожидаемому {'ok': true}"

################## если создать пользователя с логином, который уже есть, возвращается ошибка. ##################
    @allure.title("Ошибка при регистрации с уже существующим логином")
    @allure.description("Проверка, что при повторной регистрации с тем же логином возвращается ошибка 409")
    def test_error_with_identical_login(self, create_courier):
        response, [login, password, first_name] = create_courier
        payload = {
            "login": login,
            "password": CourierHelper.generate_random_string(10),
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 409, "Должна быть ошибка 409 на создание курьера с тем же логином"
