# 급여 정보를 담당하는 class
class Salary:
    def __init__(self, base_pay, bonus, overtime):
        self.base_pay = base_pay
        self.bonus = bonus
        self.overtime = overtime

    def get_total(self):
        pay = self.base_pay + self.bonus + self.overtime
        return pay

    def get_tax(self):
        tax = self.get_total() * 0.1
        return tax

    def get_net(self):
        net = self.get_total() - self.get_tax()
        return net


# 근무 이력 한 건을 담당하는 class
class WorkHistory:
    def __init__(self, company, position, start_year, end_year):
        self.company = company
        self.position = position
        self.start_year = start_year
        self.end_year = end_year

    def get_years(self):
        work_year = self.end_year - self.start_year
        return work_year

    def to_string(self):
        return "{}\t{}\t{}~{}\t{}년".format(
            self.company,
            self.position,
            self.start_year,
            self.end_year,
            self.get_years()
        )


# 사원 정보 + Salary + WorkHistory 
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.dept = ""          # 부서 배치 전에는 빈 문자열
        self.salary = salary
        self.histories = []

    def add_history(self, history):
        self.histories.append(history)

    def get_career(self):
        total = 0
        for h in self.histories:
            total += h.get_years()
        return total            # for 문 밖에서 반환

    def to_string(self):
        return "{}\t{}년\t{}\t{:.1f}\t{:.1f}".format(
            self.name,
            self.get_career(),
            self.salary.get_total(),
            self.salary.get_tax(),
            self.salary.get_net()
        )


# 부서 정보 + Employee 
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        employee.dept = self.name       
        self.employees.append(employee)

    def get_payroll(self):
        total = 0
        for emp in self.employees:
            total += emp.salary.get_total()
        return total

    def get_avg_career(self):
        if len(self.employees) == 0:    # 0으로 나누기 방지
            return 0
        total = 0
        for emp in self.employees:
            total += emp.get_career()
        return total / len(self.employees)

    def print_members(self):
        print("[{}] {}명 | 급여 총액 {} | 평균 경력 {:.1f}년".format(
            self.name,
            len(self.employees),
            self.get_payroll(),
            self.get_avg_career()
        ))
        print("  이름\t경력\t총액\t세금\t실수령액")
        for emp in self.employees:
            print("  " + emp.to_string())


# 회사 정보 + Department 
class Company:
    def __init__(self, name):
        self.name = name
        self.departments = []

    def add_department(self, dept):
        self.departments.append(dept)

    def get_employee_count(self):
        total = 0
        for dept in self.departments:
            total += len(dept.employees)
        return total

    def get_payroll(self):
        total = 0
        for dept in self.departments:
            total += dept.get_payroll()
        return total

    def print_report(self):
        print("===== {} 사원 현황 =====".format(self.name))
        for dept in self.departments:
            dept.print_members()
        print("전체 사원 {}명 | 전체 급여 총액 {}".format(
            self.get_employee_count(),
            self.get_payroll()
        ))


# =====================================================================================
# 1. 사원 생성 
kim = Employee("김민수", Salary(300, 50, 20))
choi = Employee("최서연", Salary(350, 30, 25))
lee = Employee("이지은", Salary(320, 40, 30))
park = Employee("박준호", Salary(280, 60, 10))
han = Employee("한도윤", Salary(300, 70, 15))

# 2. 근무이력 추가
kim.add_history(WorkHistory("네오소프트", "사원", 2015, 2018))
kim.add_history(WorkHistory("한빛시스템", "대리", 2018, 2022))

choi.add_history(WorkHistory("데이터랩", "연구원", 2012, 2016))
choi.add_history(WorkHistory("클라우드원", "선임", 2016, 2020))
choi.add_history(WorkHistory("넥스트AI", "책임", 2020, 2023))

lee.add_history(WorkHistory("그린HR", "사원", 2017, 2021))

han.add_history(WorkHistory("브랜드웍스", "사원", 2019, 2022))

# 3. 부서 생성 후 사원 배치 
dev = Department("개발팀")
dev.add_employee(kim)
dev.add_employee(choi)

hr = Department("인사팀")
hr.add_employee(lee)

sales = Department("영업팀")
sales.add_employee(park)

marketing = Department("마케팅팀")
marketing.add_employee(han)

# 4. 회사 생성 후 부서 등록
company = Company("블루웨이브")
company.add_department(dev)
company.add_department(hr)
company.add_department(sales)
company.add_department(marketing)

# 5. 보고서 출력
company.print_report()