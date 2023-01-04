import application.salary as salary
import application.db.people as people
from datetime import date

if __name__ == '__main__':
    salary.calculate_salary()
    people.get_employees()

    print(date.today())
