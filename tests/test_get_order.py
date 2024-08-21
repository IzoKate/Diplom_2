import allure

from constants import Constants
from stellarburgers_service.description_route import APIStellarBurger


class TestGetOrderUser:
    @allure.step("Проверяем получение заказов авторизованного пользователя- статус 200")
    def test_auth_user_get_order_state_200(self):
        # Создадим пользователя и авторизуемся
        data = Constants.CONSTANTS_DATA
        response1 = APIStellarBurger().post_create_user(data=data)
        response2 = APIStellarBurger().post_login_user(data=data)
        token = response2.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA, headers=token)
        response_orders = APIStellarBurger().get_list_orders(headers=token)
        assert response_orders.status_code == 200

        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем получение заказов авторизованного пользователя- тело ответа верное")
    def test_auth_user_get_order_got_list_user_order(self):
        # Создадим пользователя и авторизуемся
        data = Constants.CONSTANTS_DATA
        response1 = APIStellarBurger().post_create_user(data=data)
        response2 = APIStellarBurger().post_login_user(data=data)
        token = response2.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA, headers=token)
        response_orders = APIStellarBurger().get_list_orders(headers=token)
        assert response_orders.json()['success'] == True
        assert list(response_orders.json().keys()) == ['success','orders','total','totalToday']

        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем получение заказов неавторизованного пользователя- статус 401")
    def test_unauth_user_get_order_state_401(self):
        # Создадим пользователя и авторизуемся
        response_orders = APIStellarBurger().get_list_orders()
        assert response_orders.status_code == 401

    @allure.step("Проверяем получение заказов неавторизованного пользователя- тело ответа верное")
    def test_unauth_user_get_order_state_401(self):
        # Создадим пользователя и авторизуемся
        response_orders = APIStellarBurger().get_list_orders()
        assert response_orders.json()['success'] == False
        assert response_orders.json()['message'] == 'You should be authorised'
