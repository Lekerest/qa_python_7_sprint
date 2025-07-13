import pytest
import requests
import allure
from data import Data

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    @allure.title("Создание заказа с цветом: {color}")
    @allure.description("Проверка, что заказ можно создать с разными значениями цвета")
    def test_order_with_colour(self, color):
        order_data = Data.base_order.copy()
        order_data["color"] = color

        with allure.step(f"Отправка запроса на создание заказа с цветом: {color}"):
            response = requests.post(f"{BASE_URL}/orders", json=order_data)

        with allure.step("Проверка, что статус ответа 201 и в ответе есть поле 'track'"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            assert "track" in response.json(), f"В ответе отсутствует поле 'track': {response.json()}"
