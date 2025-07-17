import pytest
from helpers import CourierHelper
import requests
import logging

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def create_courier():
    credentials = CourierHelper.register_new_courier_and_return_login_password()
    if not credentials:
        pytest.fail("Не удалось зарегистрировать курьера")
    return credentials


@pytest.fixture(scope="session", autouse=True)
def auto_cleanup():
    yield
    CourierHelper.cleanup_created_couriers()

@pytest.fixture(scope="function")
def courier_and_order():

    login = password = None

    # Регистрация нового курьера
    try:
        login_data = CourierHelper.register_new_courier_and_return_login_password()
        login, password = login_data[1][0], login_data[1][1]
    except Exception as e:
        pytest.fail(f"Ошибка при регистрации курьера: {e}")

    # Авторизация курьера
    login_payload = {"login": login, "password": password}
    login_response = requests.post(f"{BASE_URL}/courier/login", json=login_payload)
    if login_response.status_code != 200:
        pytest.fail(f"Ошибка авторизации курьера: {login_response.status_code}, ответ: {login_response.text}")

    id_courier = login_response.json().get("id")
    if not id_courier:
        pytest.fail(f"Не удалось получить id курьера из ответа: {login_response.json()}")

    # Создание заказа
    order_payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }
    order_response = requests.post(f"{BASE_URL}/orders", json=order_payload)
    if order_response.status_code != 201:
        pytest.fail(f"Ошибка при создании заказа: {order_response.status_code}, ответ: {order_response.text}")

    track_order = order_response.json().get("track")
    if not track_order:
        pytest.fail(f"Не удалось получить track заказа из ответа: {order_response.json()}")

    get_id_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track_order})
    if get_id_response.status_code != 200:
        pytest.fail(f"Ошибка получение заказа по треку: {get_id_response.status_code}, ответ: {get_id_response.text}")
    id_order = get_id_response.json().get("order").get("id")

    yield id_courier, id_order, track_order

    cancel_response = requests.put(f"{BASE_URL}/orders/cancel", params={"track": track_order})
    if cancel_response.status_code == 200:
        logging.info(f"Заказ с треком {track_order} успешно отменён.")
    else:
        logging.warning(f"{cancel_response.text}, заказ будет завершен, отменить нельзя")
        requests.put(f"{BASE_URL}/orders/finish/{id_order}")

