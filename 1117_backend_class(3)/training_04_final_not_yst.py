# 급여 정보를 담당하는 class
class Salary: 
    def __init__(self, base_pay, bonus, overtime):
        self.base_pay=base_pay
        self.bonus=bonus
        self.overtime=overtime

    def get_total(self):
        pay = self.base_pay + self.bonus + self.overtime
        return pay

    def get_tax(self):
        tax = self.get_total()*0.1
        return tax

    def get_net(self):
        net = self.get_total() - self.get_tax()
        return net

# 근무 이력 정보를 갖고 있는 class
class WorkHistory:
    def __init__(self, company, position, start_year, end_year):
        self.company=company
        self.position=position
        self.start_year=start_year
        self.end_year=end_year

    def get_years(self):
        work_year = self.end_year - self.start_year
        return work_year

    def to_string(self):
        return f"{self.company} | {self.get_years()}년"


# 사원 정보와 급여 객체를 갖고 있는 class
class Employee:
    def __init__(self, name, dept, salary):
        self.name=name
        self.dept=dept
        self.salary=salary
        self.histories=[]

    def add_history(self, history):
        self.histories.append(history)

    def get_career(self):
        total=0
        for h in self.histories:
            total += h.get_years()
        return total

    def to_string(self):
        return "{}\t{}\t{}\t{:.2f}\t{:.2f}\t{}년".format(
        self.name, 
        self.dept, 
        self.salary.get_total(), 
        self.salary.get_tax(), 
        self.salary.get_net(),
        self.get_career()
        )
# =====================================================================================
class Department:
    def __init__(self, name, ):
        self.name=name
        self.employees=[]

    def add_employee(self, employee):
        self.employees.append(employee)
        
    def get_payroll(self):
        total=0
        for emp in self.employees:
            total += emp.salary.get_total()
        return total

    def get_avg_career(self):
        pass
    
    def print_member(self):
        pass


class Company:
    def __init__(self, name, departments):
        self.name=name
        self.departments=departments

    def add_department():pass
# =====================================================================================
kim = Employee("김민수", "개발팀", Salary(300, 50, 20))
lee = Employee("이지은", "인사팀", Salary(320, 40, 30))
park = Employee("박준호", "영업팀", Salary(280, 60, 10))
choi = Employee("최서연", "개발팀", Salary(350, 30, 25))
han = Employee("한도윤", "마케팅팀", Salary(300, 70, 15))

kim.add_history(WorkHistory("comp1", "대리", 2016, 2019))
kim.add_history(WorkHistory("comp2", "과장", 2019, 2023))

lee.add_history(WorkHistory("comp3", "사원", 2017, 2020))
lee.add_history(WorkHistory("comp4", "대리", 2020, 2024))

park.add_history(WorkHistory("comp5", "사원", 2015, 2018))
park.add_history(WorkHistory("comp6", "대리", 2018, 2022))

choi.add_history(WorkHistory("comp7", "사원", 2018, 2021))
choi.add_history(WorkHistory("comp8", "대리", 2021, 2024))

han.add_history(WorkHistory("comp9", "사원", 2016, 2019))
han.add_history(WorkHistory("comp10", "과장", 2019, 2024))

employees = [kim, lee, park, choi, han]




# employees = [Employee("김민수", "개발팀", Salary(300, 50, 20), WorkHistory("comp1", "개발자", "대리", 2016, 2019))
#             , Employee("이지은", "인사팀", Salary(320, 40, 30)) 
#             , Employee("박준호", "영업팀", Salary(280, 60, 10))
#             , Employee("최서연", "개발팀", Salary(350, 30, 25))
#             , Employee("한도윤", "마케팅팀", Salary(300, 70, 15))]


print("이름", "부서", "총액", "세금", "실수령액", "경력", sep="\t")
for emp in employees:
    print(emp.to_string())

print()
print("="*70)
print("\t", "근 무 이 력")

for emp in employees:
    print(f"{emp.name} 총 경력 {emp.get_career()}년")
    for h in emp.histories:
        print("\t", h.to_string())































#     def get_total(self):
#         return self.base_pay + self.bonus + self.overtime

#     def get_tax(self):
#         return self.get_total()*0.1

#     def get_net(self):
#         return self.get_total() - self.get_tax()

#     def to_string(self):
#         return "{}\t{}\t{}\t{:.2f}".format(
#         self.name, self.get_total(), self.get_tax(), self.get_net()
#         )

# employees = [Employee("김민수", 300, 50, 20), Employee("이지은", 320, 40, 30), Employee("박준호", 280, 60, 10), Employee("최서연", 350, 30, 25), Employee("한도윤", 300, 70, 15)]

# print("이름", "총액", "세금", "실수령", sep="\t")
# for employee in employees:
#         print(employee.to_string())