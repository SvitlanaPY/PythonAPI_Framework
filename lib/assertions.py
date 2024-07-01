# в тестах нам насправді не потрібно отримувати значень cookies, headers чи json, замість того нам просто потрібно переконатись,
# що значення взагалі існує і порівняти його з очікуваним значенням;
# щоб ці всі перевірки зробити зручними і витрачати в тестах на ці перевірки лише одну стрічку, потрібно створити окремий клас Assertions
# в цей клас ми покладемо функції, які будуть дещо розширювати спектр перевірок всередині тесту.
# наприклад в класі можна зробити метод, який на вхід буде отримувати:
# відповідь response, очікуване значення, сам із цієї відповіді (response) буде парсити реальне значення і порівнювати їх.
#

from json.decoder import JSONDecodeError
from requests import Response
import json
class Assertions:
    # перевіряємо, що значення всередині json є доступним за певним іменем і рівне тому значенню, яке ми очікуємо.
    # цей метод є статичним, оскільки наш клас Assertions не є нащадком для наших тестів і
    # щоб використовувати ф-ії цього класу в тестах, нам потрібно зробити ф-ії статичними.
    # на вхід ф-ія повинна отримувати обєкт з відповідю від сервера (response) щоб отримати від нього text,
    # а також ім"я (name) по якому шукати значення в json, очікуване значення і текст помилки у випадку, якщо це значення не вдається знайти.
    # ф-ія не повертатиме значення, а порівнюватиме значення з очікуваним значенням

    @staticmethod
    def assert_json_value_by_name(response: Response, key_name, expected_value, error_message):
        # assert response.status_code == 200, 'Wrong status code'  -  # status_code будемо перевіряти в окремому assertion (assert_code_status)
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in json format. Response text is {response.text}"

        assert key_name in response_as_dict, f"Response JSON doesn't have key {key_name}"
        assert response_as_dict[key_name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key_name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in json format. Response text is {response.text}"

        assert key_name in response_as_dict, f"Response JSON doesn't have key {key_name}"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"
