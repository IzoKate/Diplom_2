import allure

from constants import Constants
from stellarburgers_service.description_route import APIStellarBurger


class TestOrderCreate:
    #Авторизованный пользователь:

    @allure.step("Проверяем, что можно создать заказ под авторизованным пользователем c ингредиентами- код ответа 200")
    def test_create_order_auth_user_state_200(self):
        data = Constants.CONSTANTS_DATA
        response_create = APIStellarBurger().post_create_user(data=data)
        self.token = response_create.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA, headers=self.token)
        assert response.status_code == 200

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем, что можно создать заказ под авторизованным пользователем c ингредиентами- тело ответа верное")
    def test_create_order_auth_user_get_valid_state(self):
        data = Constants.CONSTANTS_DATA
        response = APIStellarBurger().post_create_user(data=data)
        self.token = response.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA, headers=self.token)
        assert response.json()['success'] == True
        assert response.json()['order']['ingredients'][0]['_id'] in Constants.INGREDIENTS_DATA['ingredients']

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем, что можно создать заказ под авторизованным пользователем без ингредиентов- код ответа 400")
    def test_create_order_auth_user_without_ingredient_state_400(self):
        data = Constants.CONSTANTS_DATA
        response = APIStellarBurger().post_create_user(data=data)
        self.token = response.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA_EMPTY, headers=self.token)
        assert response.status_code == 400

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем, что можно создать заказ под авторизованным пользователем без ингредиентов- тело ответа верное")
    def test_create_order_auth_user_without_ingredient_get_valid_body(self):
        data = Constants.CONSTANTS_DATA
        response = APIStellarBurger().post_create_user(data=data)
        self.token = response.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA_EMPTY, headers=self.token)
        assert response.json()['success'] == False
        assert response.json()['message'] == 'Ingredient ids must be provided'

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем, что если передать неверный хэш ингредиента - код ответа 500")
    def test_create_order_auth_user_invalid_ingredient_state_500(self):
        data = Constants.CONSTANTS_DATA
        response_create = APIStellarBurger().post_create_user(data=data)
        self.token = response_create.json()['accessToken']
        response = APIStellarBurger().post_create_order(data=Constants.INVALID_INGREDIENTS_DATA, headers=self.token)
        assert response.status_code == 500

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    #Неавторизованный пользователь
    @allure.step("Проверяем, что можно создать заказ под неавторизованным пользователем без ингредиентов- тело ответа верное")
    def test_create_order_unauth_user_without_ingredient_get_valid_body(self):
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA_EMPTY)
        assert response.json()['success'] == False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.step("Проверяем, что можно создать заказ под неавторизованным пользователем без ингредиентов- статус ответа 400")
    def test_create_order_unauth_user_without_ingredient_state400(self):
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA_EMPTY)
        assert response.status_code == 400

    @allure.step("Проверяем, что можно создать заказ под неавторизованным пользователем c ингредиентами- тело ответа верное")
    def test_create_order_unauth_user_with_ingredient_get_valid_body(self):
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA)
        assert response.json()['success'] == True
        assert ['success', 'name', 'order'] == list(response.json().keys())

    @allure.step("Проверяем, что можно создать заказ под неавторизованным пользователем c ингредиентами- статус ответа 200")
    def test_create_order_unauth_user_with_ingredient_state400(self):
        response = APIStellarBurger().post_create_order(data=Constants.INGREDIENTS_DATA)
        assert response.status_code == 200

    @allure.step("Проверяем, что если передать неверный хэш ингредиента у неавторизованного пользователя - код ответа 500")
    def test_create_order_unauth_user_invalid_ingredient_state_500(self):
        response = APIStellarBurger().post_create_order(data=Constants.INVALID_INGREDIENTS_DATA)
        assert response.status_code == 500
