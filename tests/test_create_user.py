import allure

from constants import Constants
from stellarburgers_service.description_route import APIStellarBurger
import pytest

@allure.epic('Делаем проверки создания пользователя')
class TestUserCreate:
    @allure.step("Проверяем, что пользователя можно создать и запрос возвращает правильный код ответа 200")
    def test_user_create_check_get_state_200(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.status_code == 200

        try:
        #Удалим созданного пользователя
            headers = self.response.json()['accessToken']
            self.response = APIStellarBurger().delete_user(headers=headers)
            assert self.response.status_code == 202
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем, что у созданного пользователя тело ответа верное")
    def test_user_create_check_get_valid_body(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.json()['success'] == True
        assert self.response.json()['user']['email'] == data["email"]
        assert 'accessToken' in self.response.json()
        assert 'refreshToken' in self.response.json()

        try:
        #Удалим созданного пользователя
            headers = self.response.json()['accessToken']
            self.response = APIStellarBurger().delete_user(headers=headers)
            assert self.response.status_code == 202
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем, что уже зарегистрированного пользователя нельзя создать повторно код ответа 403")
    def test_create_double_user_get_state_403(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        self.token = self.response.json()['accessToken']
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.status_code == 403

        try:
            # Удалим созданного пользователя
            headers = self.token
            self.response = APIStellarBurger().delete_user(headers=headers)
            assert self.response.status_code == 202
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')

    @allure.step("Проверяем, что уже зарегистрированного пользователя нельзя создать повторно -  верное тело ответа")
    def test_create_double_user_get_valid_body(self):
        data = {
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "name": Constants.NAME
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        self.token = self.response.json()['accessToken']
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.json()['success'] == False
        assert self.response.json()['message'] == "User already exists"

        try:
            # Удалим созданного пользователя
            headers = self.token
            self.response = APIStellarBurger().delete_user(headers=headers)
            assert self.response.status_code == 202
        except Exception as e:
            print(f'Не смогли удалить пользователя, ошибка {e}')


    @allure.step("Проверяем, что пользователя нельзя создать, если не заполнено одно из обязательных полей - статус 403")
    @pytest.mark.parametrize('email, password,name',
                             [
                                 ['', Constants.PASSWORD, Constants.NAME],
                                 [Constants.EMAIL, '', Constants.NAME],
                                 ['', '', Constants.NAME],
                                 [Constants.EMAIL, '', ''],
                                 ['', Constants.PASSWORD, ''],
                                 ['', '', '']
                             ])
    def test_user_create_without_mandatory_field_get_state_403(self, email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.status_code == 403


    @allure.step("Проверяем, что пользователя нельзя создать, если не заполнено одно из обязательных полей - тело ответа верное")
    @pytest.mark.parametrize('email, password,name',
                             [
                                 ['', Constants.PASSWORD, Constants.NAME],
                                 [Constants.EMAIL, '', Constants.NAME],
                                 ['', '', Constants.NAME],
                                 [Constants.EMAIL, '', ''],
                                 ['', Constants.PASSWORD, ''],
                                 ['', '', '']
                             ])
    def test_user_create_without_mandatory_field_get_state_403(self, email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        self.response = APIStellarBurger().post_create_user(data=data)
        assert self.response.json()['success'] == False
        assert self.response.json()['message'] == "Email, password and name are required fields"
