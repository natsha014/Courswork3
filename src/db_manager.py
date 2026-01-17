from typing import Any

import psycopg2


class DBManager:
    def __init__(self, db_name: str, params: dict) -> None:
        self.db_name = db_name
        self.params = params

    def _execute_query(self, query: str, params: Any = None) -> Any:
        """Метод для выполнения запросов"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
            SELECT company_name, COUNT(vacancies.vacancy_id) as vacancies_count
            FROM companies
            JOIN vacancies USING (employer_id)
            GROUP BY company_name
            ORDER BY vacancies_count DESC;
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        query = """
            SELECT companies.company_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            JOIN companies USING (employer_id)
            ORDER BY salary
        """
        return self._execute_query(query)

    def get_avg_salary(self) -> Any:
        """Получает среднюю зарплату по вакансиям"""
        query = """
            SELECT AVG(salary)
            FROM vacancies
        """
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям"""
        query = """
            SELECT *
            FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            ORDER BY salary DESC
        """
        return self._execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python"""
        query = """
            SELECT *
            FROM vacancies WHERE vacancy_name ILIKE %s
        """
        return self._execute_query(query, (f"%{keyword}%",))
