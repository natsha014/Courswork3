from typing import Any

import psycopg2


def data_for_db_companies(raw_vacancies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Создание списка компаний для базы данных"""

    companies_dict = {}

    for item in raw_vacancies:
        employer = item.get("employer")
        if employer:
            emp_id = employer.get("id")
            if emp_id not in companies_dict:
                companies_dict[emp_id] = {
                    "employer_id": int(emp_id),
                    "name": employer.get("name"),
                    "url": employer.get("alternate_url"),
                }
    companies_list = list(companies_dict.values())
    return companies_list


def data_for_db_vacancies(raw_vacancies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Создание списка вакансий для базы данных"""

    vacancies_list = []

    for item in raw_vacancies:
        salary = item.get("salary")
        salary_from = salary.get("from") if salary else None

        vacancy_data = {
            "name": item.get("name"),
            "salary_from": salary_from,
            "url": item.get("alternate_url"),
            "employer_id": int(item.get("employer", ()).get("id")) if item.get("employer") else None,
        }
        vacancies_list.append(vacancy_data)
    return vacancies_list


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE companies (
                employer_id INT PRIMARY KEY,
                company_name VARCHAR NOT NULL,
                company_url TEXT
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES companies(employer_id) ON DELETE CASCADE,
                vacancy_name VARCHAR NOT NULL,
                salary INTEGER,
                vacancy_url TEXT
            )
        """
        )

    conn.commit()
    conn.close()


def save_companies_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (employer_id, company_name, company_url)
                VALUES (%s, %s, %s)
                """,
                (company["employer_id"], company["name"], company["url"]),
            )

    conn.commit()
    conn.close()


def save_vacancies_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute(
                """
                INSERT INTO vacancies (employer_id, vacancy_name, salary, vacancy_url)
                VALUES (%s, %s, %s, %s)
                """,
                (vacancy["employer_id"], vacancy["name"], vacancy["salary_from"], vacancy["url"]),
            )

    conn.commit()
    conn.close()
