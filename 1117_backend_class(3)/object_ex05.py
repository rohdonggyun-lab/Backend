#학생과 점수의 리스트/딕셔너리에서 출력하고 이걸 자동화하기 위해 함수를 만드는 과정


# 학생 class를 선언해주세요.
class Student:
    def __init__(self, name, korean, english, math, science):
        self.name=name
        self.korean=korean
        self.english=english
        self.math=math
        self.science=science

    def student_get_sum(self):
        return self.korean + self.english + self.math + self.science

    def student_get_avg(self):
        return self.student_get_sum()/4

    #학생 한명의 점수를 출력하는 함수 : student_to_string(student)
    def student_to_string(self):
            return "{}\t{}\t{:.2f}".format(
            self.name, self.student_get_sum(), self.student_get_avg()
            )

students=[
    Student("노동균", 90, 95, 98, 100)
    ,Student("노세람", 80, 85, 88, 90)
    ,Student("노현준", 70, 75, 78, 80)
    ,Student("노정현", 60, 65, 68, 70)
    ,Student("노민재", 50, 55, 58, 60)
]

print("이름","총점","평균",sep="\t")
for student in students:
        print(student.student_to_string())

print(students[0].name)





