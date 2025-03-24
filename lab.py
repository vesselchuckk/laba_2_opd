import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


# URL поиска вакансий на hh.ru
url = "https://hh.ru/search/vacancy"

# Параметры запроса: ищем вакансии по слову "Python"
params = {
    "text": "Python",
    "page": 0  # номер страницы (будет изменяться в цикле)
}

# Заголовки запроса (User-Agent помогает избежать блокировки)
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/98.0.4758.102 Safari/537.36")
}

vacancies = []  # список для хранения данных о вакансиях

# Перебираем, например, первые 2 страницы результатов
for page in range(0, 2):
    params["page"] = page
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка загрузки страницы {page}: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # На странице вакансии располагаются в блоках с классом "vacancy-serp-item"
    vacancy_items = soup.find_all("div", class_="vacancy-serp-item")

    for vacancy in vacancy_items:
        # Получаем название вакансии и ссылку на подробное описание
        title_elem = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"})
        title = title_elem.text.strip() if title_elem else "Нет названия"
        link = title_elem.get("href") if title_elem else "Нет ссылки"

        # Получаем название компании
        company_elem = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
        company = company_elem.text.strip() if company_elem else "Не указано"

        # Получаем местоположение
        location_elem = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address"})
        location = location_elem.text.strip() if location_elem else "Не указано"

        # Получаем информацию о зарплате
        salary_elem = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        salary = salary_elem.text.strip() if salary_elem else "Не указано"

        # Добавляем данные о вакансии в список
        vacancies.append({
            "Название": title,
            "Компания": company,
            "Локация": location,
            "Зарплата": salary,
            "Ссылка": link
        })

# Создаем Excel-файл с помощью openpyxl
wb = Workbook()
ws = wb.active
ws.title = "Вакансии"

# Записываем заголовки столбцов
headers_row = ["Название", "Компания", "Локация", "Зарплата", "Ссылка"]
ws.append(headers_row)

# Записываем данные по вакансиям
for vac in vacancies:
    ws.append([vac["Название"], vac["Компания"], vac["Локация"], vac["Зарплата"], vac["Ссылка"]])

# Сохраняем файл
wb.save("vacancies.xlsx")

print("Данные успешно сохранены в файл vacancies.xlsx")
