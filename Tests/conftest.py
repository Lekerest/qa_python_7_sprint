import pytest
from helpers import CourierHelper

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
