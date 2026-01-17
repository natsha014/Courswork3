from src.api import get_vacancies
from src.utils import data_for_db_companies, data_for_db_vacancies, create_database, save_companies_to_database, \
    save_vacancies_to_database
from config import config
from src.db_manager import DBManager


def main():
    employer_ids = [3529, 1057, 11511190, 87021, 64174, 3776, 15478, 2180, 4233, 1740]
    search_query = input("Введите поисковый запрос: ")
    print(f"Загрузка вакансий по запросу '{search_query}'...")

    raw_vacancies = get_vacancies(search_query, employer_ids)
    companies = data_for_db_companies(raw_vacancies)
    vacancies = data_for_db_vacancies(raw_vacancies)

    print(f"\nВакансии сохраняются в базу данных...")
    params = config()
    create_database('vacancies_hh', params)
    save_companies_to_database(companies, 'vacancies_hh', params)
    save_vacancies_to_database(vacancies, 'vacancies_hh', params)
    print(f"\nДанные успешно сохранены в базу 'vacancies_hh'!")
    print(f"Всего компаний: {len(companies)}, всего вакансий: {len(vacancies)}\n")

    db_manager = DBManager('vacancies_hh', params)
    count_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in count_vacancies:
        print(f"{company}: {count} вакансий")

    all_vacancies = db_manager.get_all_vacancies()
    print(f"\nВсего {len(all_vacancies)} вакансий\nСписок вакансий (первые 3):")
    for vac in all_vacancies[:3]:
        company, name, salary, url = vac
        print(f"{company} | {name} | {salary} | {url}")

    avg_salary = db_manager.get_avg_salary()
    print(f"\nСредняя зарплата по вакансиям: {round(avg_salary[0][0], 2)}")

    higher_salary = db_manager.get_vacancies_with_higher_salary()
    print(f"\nВсего {len(higher_salary)} вакансий\nСписок вакансий (первые 3):")
    for vacancy in higher_salary[:3]:
        id_vac, company, name, salary, url = vacancy
        print(f"{id_vac} | {company} | {name} | {salary} | {url}")

    vacancies_keyword = db_manager.get_vacancies_with_keyword(search_query)
    print(f"\nВсего по запросу '{search_query}' в названии найдено: {len(vacancies_keyword)} вакансий")


if __name__ == "__main__":
    main()
