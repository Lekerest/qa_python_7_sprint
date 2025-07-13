import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа курьером")
    @allure.description("Проверка успешного принятия заказа при корректных id курьера и заказа")
    def test_accept_order(self, courier_and_order):
        id_courier, id_order, _ = courier_and_order
        with allure.step(f"Отправка запроса на принятие заказа с id_order={id_order} и id_courier={id_courier}"):
            response = requests.put(f"{BASE_URL}/orders/accept/{id_order}?courierId={id_courier}")
        with allure.step("Проверка, что в ответе содержится {'ok': True}"):
            assert response.json() == {"ok": True}

    @allure.title("Ошибка при попытке принять заказ без id курьера")
    @allure.description("Проверка ошибки 400 при отсутствии параметра courierId при принятии заказа")
    def test_accept_order_without_id_courier(self, courier_and_order):
        _, id_order, _ = courier_and_order
        with allure.step(f"Отправка запроса на принятие заказа с id_order={id_order} без courierId"):
            response = requests.put(f"{BASE_URL}/orders/accept/{id_order}", params={"courierId": None})
        with allure.step("Проверка, что статус ответа равен 400"):
            assert response.status_code == 400

    @allure.title("Ошибка при неверном id курьера")
    @allure.description("Проверка ошибки 404 при использовании несуществующего id курьера")
    def test_accept_order_with_wrong_id_courier(self, courier_and_order):
        _, id_order, _ = courier_and_order
        id_courier = 123123123
        with allure.step(f"Отправка запроса на принятие заказа с id_order={id_order} и некорректным id_courier={id_courier}"):
            response = requests.put(f"{BASE_URL}/orders/accept/{id_order}", params={"courierId": id_courier})
        with allure.step("Проверка, что статус ответа равен 404"):
            assert response.status_code == 404

    @allure.title("Ошибка при отсутствии id заказа")
    @allure.description("Проверка ошибки 400 при попытке принять заказ без указания id заказа")
    def test_accept_order_without_id_order(self, courier_and_order):
        id_courier, _, _ = courier_and_order
        with allure.step(f"Отправка запроса на принятие заказа без id_order и с id_courier={id_courier}"):
            response = requests.put(f"{BASE_URL}/orders/accept/", params={"courierId": id_courier})
        with allure.step("Проверка, что статус ответа равен 400"):
            assert response.status_code == 400

    @allure.title("Ошибка при неверном id заказа")
    @allure.description("Проверка ошибки 404 при использовании несуществующего id заказа")
    def test_accept_order_with_wrong_id_order(self, courier_and_order):
        id_courier, _, _ = courier_and_order
        id_order = 123123123
        with allure.step(f"Отправка запроса на принятие заказа с некорректным id_order={id_order} и id_courier={id_courier}"):
            response = requests.put(f"{BASE_URL}/orders/accept/{id_order}", params={"courierId": id_courier})
        with allure.step("Проверка, что статус ответа равен 404"):
            assert response.status_code == 404
