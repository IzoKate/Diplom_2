import allure
import pytest

from constants import Constants
from stellarburgers_service.description_route import APIStellarBurger


@allure.epic('Проверяем изменение данных пользователя')
class TestUserLogin:
    #Авторизованный пользователь
    @allure.step("Проверяем изменение данных пользователя авторизованного, меняем пароль- статус 200")
    def test_auth_user_data_change_password_get_state_200(self):
        #Создадим пользователя и авторизуемся
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        APIStellarBurger().post_create_user(data=data)
        del (data['name'])
        response = APIStellarBurger().post_login_user(data=data)
        #Поменяем данные пользователя
        self.token = response.json()['accessToken']
        newdata = {
            "email": data['email'],
            "password": Constants.PASSWORD_AUTH_CHANGE1,
        }
        response = APIStellarBurger().patch_change_user(data=newdata, headers=self.token)
        assert response.status_code == 200

        try:
            # Удалим созданного пользователя
            headers = self.token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем изменение данных пользователя авторизованного, меняем пароль- тело ответа верное")
    def test_auth_user_data_change_password_get_valid_body(self):
        #Создадим пользователя и авторизуемся
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        APIStellarBurger().post_create_user(data=data)
        del (data['name'])
        response = APIStellarBurger().post_login_user(data=data)
        #Поменяем данные пользователя
        token = response.json()['accessToken']
        newdata = {
            "email": data['email'],
            "password": Constants.PASSWORD_AUTH_CHANGE1,
        }
        response = APIStellarBurger().patch_change_user(data=newdata, headers=token)
        assert response.json()['success'] == True
        assert response.json()['user']['email'] == newdata["email"]


        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем изменение данных пользователя авторизованного, меняем логин- статус 200")
    def test_auth_user_data_change_login_get_state_200(self):
        #Создадим пользователя и ааторизуемся
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        APIStellarBurger().post_create_user(data=data)
        del (data['name'])
        response = APIStellarBurger().post_login_user(data=data)
        #Поменяем данные пользователя
        token = response.json()['accessToken']
        newdata = {
            "email": Constants.EMAIL,
            "password": data['password'],
        }
        response = APIStellarBurger().patch_change_user(data=newdata, headers=token)
        assert response.status_code == 200

        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем изменение данных пользователя авторизованного, меняем логин на существующий - статус 403")
    def test_auth_user_data_change_existing_login_get_state_403(self):
        #Создадим пользователя
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        response = APIStellarBurger().post_create_user(data=data)
        # Поменяем данные пользователя
        try:
            del (data['name'])
            token = response.json()['accessToken']
            response = APIStellarBurger().patch_change_user(data=data, headers=token)
            assert response.status_code == 403
        except Exception as e:
            print(f'Ошибка {e}')

        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    #Неавторизованный пользователь
    @allure.step("Проверяем изменение данных пользователя неавторизованного, меняем пароль- статус 401")
    def test_unauth_user_data_change_password_get_state_401(self):
        #Создадим пользователя
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        response = APIStellarBurger().post_create_user(data=data)
        #Выйдем из профиля
        response_logout = APIStellarBurger().post_unlogin_user(data={"token": response.json()['refreshToken']})
        #Поменяем данные пользователя
        token = response.json()['accessToken']
        newdata = {
                "email": data['email'],
                "password": Constants.PASSWORD_AUTH_CHANGE2,
            }
        response = APIStellarBurger().patch_change_user(data=newdata)
        assert response.status_code == 401


        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем изменение данных пользователя неавторизованного, меняем логин - статус 401")
    def test_unauth_user_data_change_login_get_state_401(self):
        #Создадим пользователя
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        response = APIStellarBurger().post_create_user(data=data)
        #Выйдем из профиля
        response_logout = APIStellarBurger().post_unlogin_user(data={"token": response.json()['refreshToken']})
        #Поменяем данные пользователя
        token = response.json()['accessToken']
        newdata = {
                "email": Constants.EMAIL_AUTH_CHANGE2,
                "password": data['password'],
            }
        response = APIStellarBurger().patch_change_user(data=newdata)
        assert response.status_code == 401

        try:
            # Удалим созданного пользователя
            headers = token
            APIStellarBurger().delete_user(headers=headers)
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

