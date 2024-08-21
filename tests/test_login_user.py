import allure
import pytest

from constants import Constants
from stellarburgers_service.description_route import APIStellarBurger


@allure.epic('Делаем проверки авторизации пользователя')
class TestUserLogin:
    @allure.step("Проверяем, что авторизация успешна под существующим пользователем - статус 200")
    def test_user_login_check_state_200(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        APIStellarBurger().post_create_user(data=data)
        del (data['name'])
        response = APIStellarBurger().post_login_user(data=data)
        assert response.status_code == 200

        try:
            # Удалим созданного пользователя
            headers = response.json()['accessToken']
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем, что авторизация успешна под существующим пользователем - тело запроса верное")
    def test_user_login_check_get_valid_body(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        APIStellarBurger().post_create_user(data=data)
        del (data['name'])
        response = APIStellarBurger().post_login_user(data=data)
        assert response.json()['success'] == True
        assert response.json()['user']['email'] == data["email"]
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

        try:
            # Удалим созданного пользователя
            headers = response.json()['accessToken']
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')



    @allure.step("Проверяем, что авторизация неуспешна под пользователем - статус 401")
    @pytest.mark.parametrize('email, password',
                             [
                                 [Constants.EMAIL, Constants.PASSWORD],
                                 ['', Constants.PASSWORD],
                                 [Constants.EMAIL, ''],
                                 ['', '']
                             ])
    def test_user_login_check_unauthorized_state_401(self, email, password):
            data = {
                "email": email,
                "password": password
            }
            APIStellarBurger().post_create_user(data=data)
            response = APIStellarBurger().post_login_user(data=data)
            assert response.status_code == 401


    @allure.step("Проверяем, что авторизация неуспешна под пользователем - тело ответа верное")
    @pytest.mark.parametrize('email, password',
                             [
                                 [Constants.EMAIL, Constants.PASSWORD],
                                 ['', Constants.PASSWORD],
                                 [Constants.EMAIL, ''],
                                 ['', '']
                             ])
    def test_user_login_check_unauthorized_get_invalid_body(self, email, password):
            data = {
                "email": email,
                "password": password
            }
            APIStellarBurger().post_create_user(data=data)
            response = APIStellarBurger().post_login_user(data=data)
            assert response.json()['success'] == False
            assert response.json()['message'] == "email or password are incorrect"
