from typing import Any

import requests


def get_vacancies(keyword: str, employer_ids: list[int] | None = None, per_page: int = 20) -> list[dict[str, Any]]:
    """Ищет вакансии на hh.ru по ключевому слову"""

    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}

    all_vacancies = []
    if employer_ids is None:
        employer_ids = []
    for employer_id in employer_ids:
        params: dict[str, Any] = {"text": keyword, "per_page": per_page, "employer_id": employer_id}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            current_data = response.json()
            items = current_data.get("items", [])
            print(f"ID {employer_id}: найдено {len(items)} вакансий")

            all_vacancies.extend(items)

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при запросе ID {employer_id}: {e}")
            continue
    return all_vacancies
