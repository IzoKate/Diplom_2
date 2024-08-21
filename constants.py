from stellarburgers_service.user import RegisterUserRandom


class Constants:
    URL_SERVICE = "https://stellarburgers.nomoreparties.site"
    HEADERS_JSON = {'Content-type': 'application/json'}

    NAME = RegisterUserRandom.generate_random_string(8)
    PASSWORD = RegisterUserRandom.generate_random_string(8)
    EMAIL = f'{RegisterUserRandom.generate_random_string(9)}@ya.ru'


    PASSWORD_AUTH_CHANGE1 = '8765432100'
    PASSWORD_AUTH_CHANGE2 = '8765432100'
    EMAIL_AUTH_CHANGE1 = 'izosimova099888@yandex.ru'
    EMAIL_AUTH_CHANGE2 = 'izosimova099888@yandex.ru'


    CONSTANTS_DATA = {
                "email": EMAIL,
                "password": PASSWORD,
                "name": NAME
            }

    INGREDIENTS_DATA = {"ingredients": ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa6d"]}
    INGREDIENTS_DATA_EMPTY = {"ingredients": []}
    INVALID_INGREDIENTS_DATA = {"ingredients": ["000000000082001bdaaa6d","00000000001f82001bdaaa6d"]}