import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


class TestGetOrderByNumber:

    @allure.title("Получение заказа по номеру трека")
    @allure.description("Проверка успешного получения заказа по корректному номеру трека")
    def test_get_order_by_number(self, courier_and_order):
        _, _, track_order = courier_and_order
        with allure.step(f"Отправка GET-запроса на получение заказа по треку: {track_order}"):
            get_order_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track_order})
        with allure.step("Проверка, что в ответе присутствует ключ 'order'"):
            assert "order" in get_order_response.json()

    @allure.title("Ошибка при отсутствии номера заказа")
    @allure.description("Проверка получения ошибки 400 при попытке получить заказ без указания номера трека")
    def test_get_order_without_number(self):
        with allure.step("Отправка GET-запроса без параметра 't' (номер трека)"):
            get_order_response = requests.get(f"{BASE_URL}/orders/track")
        with allure.step("Проверка, что статус ответа равен 400"):
            assert get_order_response.status_code == 400

    @allure.title("Ошибка при несуществующем номере заказа")
    @allure.description("Проверка получения ошибки 404 при запросе с несуществующим номером трека")
    def test_get_order_with_nonexistence_number(self):
        track_order = 123123123
        with allure.step(f"Отправка GET-запроса с несуществующим номером трека: {track_order}"):
            get_order_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track_order})
        with allure.step("Проверка, что статус ответа равен 404"):
            assert get_order_response.status_code == 404