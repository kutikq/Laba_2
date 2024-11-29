import requests as re
import unittest as unit

def find_color_from_url(url):
     # Отправка запроса на указанный URL
    response = re.get(url)
    response.raise_for_status()  # Проверка успешности запроса

    # Извлекаем текст страницы
    html_content = response.text

    # Регулярное выражение для поиска HEX цветов
    pattern = r'#[A-Fa-f0-9]{6}'
    hex_colors = re.findall(pattern, html_content)
    return hex_colors

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