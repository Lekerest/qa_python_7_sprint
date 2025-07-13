import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestDeleteCourier:

    @allure.title("Удаление несуществующего курьера")
    @allure.description("Проверка текста ошибки при удалении курьера с несуществующим id.")
    def test_text_after_delete_nonexistent_courier(self):
        id_courier = 12332131
        with allure.step(f"Отправка запроса на удаление несуществующего курьера с id = {id_courier}"):
            response = requests.delete(f"{BASE_URL}/courier/{id_courier}")

        with allure.step("Проверка текста ошибки в ответе"):
            expected = {"message": "Курьера с таким id нет"}
            assert response.json() == expected, f"Ожидалось сообщение {expected}, получено: {response.json()}"

    @allure.title("Удаление без ID")
    @allure.description("Проверка текста ошибки при удалении курьера без указания id.")
    def test_text_after_delete_without_id(self):
        with allure.step("Отправка запроса на удаление без указания id"):
            response = requests.delete(f"{BASE_URL}/courier/")

        with allure.step("Проверка текста ошибки в ответе"):
            expected = {"message": "Недостаточно данных для удаления курьера"}
            assert response.json() == expected, f"Ожидалось сообщение {expected}, получено: {response.json()}"

    @allure.title("Успешное удаление")
    @allure.description("Создание, авторизация и удаление курьера.")
    def test_delete_courier(self, create_courier):
        _, [login, password, _] = create_courier
        login_payload = {"login": login, "password": password}

        with allure.step("Авторизация курьера для получения ID"):
            login_response = requests.post(f"{BASE_URL}/courier/login", json=login_payload)
            id_courier = login_response.json().get("id")

        with allure.step(f"Удаление курьера с id = {id_courier}"):
            response_delete = requests.delete(f"{BASE_URL}/courier/{id_courier}")

        with allure.step("Проверка успешного ответа при удалении"):
            assert response_delete.json() == {"ok": True}, f"Удаление неуспешно, ответ: {response_delete.json()}"

    @allure.title("Код 404 при удалении несуществующего курьера")
    @allure.description("Проверка статус-кода при удалении несуществующего курьера.")
    def test_error_after_delete_nonexistent_courier(self):
        id_courier = 12332131
        with allure.step(f"Отправка запроса на удаление несуществующего курьера с id = {id_courier}"):
            response = requests.delete(f"{BASE_URL}/courier/{id_courier}")

        with allure.step("Проверка, что возвращается статус-код 404"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

    @allure.title("Код 400 при удалении без ID")
    @allure.description("Проверка статус-кода при удалении без указания id.")
    def test_error_after_delete_without_id(self):
        with allure.step("Отправка запроса на удаление без указания id"):
            response = requests.delete(f"{BASE_URL}/courier/")

        with allure.step("Проверка, что возвращается статус-код 400"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
