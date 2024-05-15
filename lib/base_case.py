# деякі повтори коду зручно винести в батьківський клас і потім перевикористовувати.
# Для цього ми створимо клас, який назвемо BaseCase.
# В окрему директорію під назвою lib - покладемо ключові класи нашого фреймворку, щоб вони були відділені від самих тестів.
# В класі BaseCase напишемо методи для отримання значень cookie та header-а із відповідей сервера по імені.
# Суть методів полягатиме в наступному: спочатку ми будемо передавати в цей метод об"єкт відповіді,
# який ми отримуємо в результаті запиту,
# і імя, по якому ми будемо з цієї відповіді отримувати значення cookie або header-а
# Метод сам буде розуміти чи є такі дані у відповіді, і якщо немає, то тест буде падати, отже щось пішло не так, оскільми ми очікували, що дані повинні бути, а їх немає
# Якщо ж дані є, то метод буде їх повертати.
# .gitignore файл - git не буде відмічати в нашому проекті зайві файли.



from json.decoder import JSONDecodeError
from requests import Response
# Response - це class в модулі requests
class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]   # return response.cookies.get(cookie_name)

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]  # return response.headers.get(header_name)

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in json format. Response text is {response.text}"
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        return response_as_dict[name]
