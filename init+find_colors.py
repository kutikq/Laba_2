import requests
import re
import unittest as unit
import os

def find_color_from_url(url):
     #выдавал ошибку если запускал тест=>доюавил исключение
    try:
        # Отправка запроса на указанный URL
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса

        # Извлекаем текст страницы
        html_content = response.text

        # Регулярное выражение для поиска HEX цветов
        pattern = r'\b#[A-Fa-f0-9]{6}\b'
        hex_colors = re.findall(pattern, html_content)
        return hex_colors
     
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе URL: {e}")
        return []

# Функция для поиска HEX-цветов в файле
def find_hex_colors_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            pattern = r'\b#[A-Fa-f0-9]{6}\b'
            hex_colors = re.findall(pattern, content)
            return hex_colors
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return []

#функция для ручного поиска
def find_hex_colors_from_text(text):
    pattern = r'#[A-Fa-f0-9]{6}'
    return re.findall(pattern, text)

class TestHexColorFinder(unit.TestCase):
    def test_find_hex_colors_from_text(self):
        # Тест с корректными HEX-цветами
        text = "Цвета: #ff80ed, #008080 и #000000."
        expected = ['#ff80ed', '#008080', '#000000']
        self.assertEqual(find_hex_colors_from_text(text), expected)

        # Тест с некорректными значениями
        text = "Некорректные: #GGGGGG, 123456, #12FG45."
        self.assertEqual(find_hex_colors_from_text(text), [])

        # Тест с пустой строкой
        text = ""
        self.assertEqual(find_hex_colors_from_text(text), [])

    def test_find_hex_colors_from_url(self):
        # Тест с корректным URL (проверяется наличие хоть одного цвета)
        url = "https://www.color-hex.com/popular-colors.php"
        result = find_color_from_url(url)
        self.assertGreater(len(result), 0, "Список HEX-цветов пуст.")

        # Тест с некорректным URL
        url = "https://nonexistent-url-example.com"
        result = find_color_from_url(url)
        self.assertEqual(result, [])

    def test_edge_cases(self):
        # ЕСли введем не в нашем формате
        text = "Пограничные случаи: #ff0000 и #FFFFFF000."
        expected = ['#ff0000']
        self.assertEqual(find_hex_colors_from_text(text), expected)
        
    def test_find_hex_colors_from_file(self):
        # Создание временного файла для теста
        test_file_path = "test_file.txt"
        with open(test_file_path, 'w', encoding='utf-8') as file:
            file.write("Цвета в файле: #FF5733, #33FF57 и текст без цвета.")

        # Проверка функции
        expected = ['#FF5733', '#33FF57']
        self.assertEqual(find_hex_colors_from_file(test_file_path), expected)

        # Удаление временного файла
        os.remove(test_file_path)

        # Проверка с несуществующим файлом
        self.assertEqual(find_hex_colors_from_file("nonexistent_file.txt"), [])

if __name__ == "__main__":
    print("Запуск тестов...")
    unit.main(exit=False)