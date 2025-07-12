import pytest
import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

class TestCreateOrder:

    base_order = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],])

    @allure.title("Создание заказа с цветом: {color}")
    @allure.description("Проверка, что заказ можно создать с разными значениями цвета")
    def test_order_with_colour(self, color):
        order_data = self.base_order.copy()
        # noinspection PyTypeChecker
        order_data["color"] = color

        response = requests.post(f"{BASE_URL}/orders", json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()
