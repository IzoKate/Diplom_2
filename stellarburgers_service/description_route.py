from constants import Constants
from stellarburgers_service.request_maker import RequestProcessing


class APIStellarBurger:
    host = Constants.URL_SERVICE

    #Создание пользователя
    def post_create_user(self, path="/api/auth/register", data=None):
        self.headers = Constants.HEADERS_JSON
        url = f"{self.host}{path}"
        return RequestProcessing().make_request('post', url, data=data, headers=self.headers)

    #Удаление пользователя
    def delete_user(self, path="/api/auth/user", data=None, headers=None, parametr=None ):
        url = f'{self.host}{path}'
        headers = {'Authorization': headers}
        return RequestProcessing().make_request(r_type='delete', url=url, data=data, headers=headers)

    #Логин пользователя
    def post_login_user(self, path="/api/auth/login", data=None):
        headers = Constants.HEADERS_JSON
        url = f'{self.host}{path}'
        return RequestProcessing().make_request('post', url, data=data, headers=headers)

    #Изменение данных пользователя
    def patch_change_user(self, path="/api/auth/user", data=None, headers=None):
        url = f'{self.host}{path}'
        headers = {'Authorization': headers, 'Content-type': 'application/json'}
        return RequestProcessing().make_request(r_type='patch', url=url, data=data, headers=headers)

    #Выход из системы
    def post_unlogin_user(self, path="/api/auth/logout", data=None):
        headers = Constants.HEADERS_JSON
        url = f'{self.host}{path}'
        return RequestProcessing().make_request('post', url, data=data, headers=headers)

    #Создание заказа
    def post_create_order(self, path="/api/orders", data=None, headers=None):
        url = f'{self.host}{path}'
        headers = {'Authorization': headers, 'Content-type': 'application/json'}
        return RequestProcessing().make_request('post', url=url, data=data, headers=headers)


    #Получение списка заказов
    def get_list_orders(self, path="/api/orders", headers = None):
        url = f'{self.host}{path}'
        headers = {'Authorization': headers}
        return RequestProcessing().make_request(r_type='get', url=url, headers=headers)
