import requests as re

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

