import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestCreateCourier:

    @allure.title("Получение списка заказов")
    @allure.description("Проверка, что можно получить список заказов")
    def test_create_courier(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert "orders" in response.json(), f"Список заказов не был получен, код {response.status_code}"