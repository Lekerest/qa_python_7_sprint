import requests
import random
import string
import logging

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CourierHelper:
    # Глобальный список для отслеживания зарегистрированных курьеров
    created_couriers = []

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @classmethod
    def register_new_courier_and_return_login_password(cls):
        login = cls.generate_random_string(10)
        password = cls.generate_random_string(10)
        first_name = cls.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)
        if response.status_code == 201:
            cls.created_couriers.append((login, password))
            logger.info(f"Курьер создан: login={login}")
        else:
            logger.warning(f"Не удалось создать курьера: статус {response.status_code}, ответ: {response.text}")
        return response, [login, password, first_name]  # возвращаем и response, и данные

    @classmethod
    def cleanup_created_couriers(cls):
        for login, password in cls.created_couriers:
            login_payload = {
                "login": login,
                "password": password
            }

            login_response = requests.post(f"{BASE_URL}/courier/login", data=login_payload)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
                if courier_id:
                    delete_response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
                    if delete_response.status_code != 200:
                        logger.error(f"Ошибка удаления курьера ID {courier_id}: статус {delete_response.status_code}")
                    else:
                        logger.info(f"Курьер с ID {courier_id} удалён успешно.")
                else:
                    logger.error(f"Не удалось получить ID курьера {login}")
            else:
                logger.error(f"Не удалось авторизовать курьера {login} для удаления: статус {login_response.status_code}")
