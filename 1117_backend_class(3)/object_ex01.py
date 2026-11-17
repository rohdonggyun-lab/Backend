#학생과 점수의 리스트/딕셔너리에서 출력하고 이걸 자동화하기 위해 함수를 만드는 과정


# 학생 리스트를 선언해주세요.
class Student:
    def __init__(self, name, korean, english, math, science):
        self.name=name
        self.korean=korean
        self.english=english
        self.math=math
        self.science=science
        self.student=[]






student1=Student("노동균", 90, 95, 98, 100)
student2=Student("노세람", 80, 85, 88, 90)
student3=Student("노현준", 70, 75, 78, 80)
student4=Student("노정현", 60, 65, 68, 70)
student5=Student("노민재", 50, 55, 58, 60)






students=[
    {"name": "노동균","korean":90,"english":95,"math":98,"science":100}
    , {"name": "노세람","korean":80,"english":85,"math":88,"science":90}
    , {"name": "노현준","korean":70,"english":75,"math":78,"science":80}
    , {"name": "노정현","korean":60,"english":65,"math":68,"science":70}
    , {"name": "노민재","korean":50,"english":55,"math":58,"science":60}]


# 학생명단(성적표) 출력하세요

print("이름", "총점", "평균", sep="\t")
for student in students:
    student_sum=student["korean"] + student["english"] + student["math"] + student["science"]
    student_avg=student_sum/4
    print(student["name"], student_sum, student_avg)

#딕셔너리를 리턴하는 함수를 선언
def create_student(name, korean, english, math, science):
    return {
        "name":name,
        "korean":korean,
        "english":english,
        "math":math,
        "science":science
    }

students=[
    create_student("노동균", 90, 95, 98, 100)
    ,create_student("노세람", 80, 85, 88, 90)
    ,create_student("노현준", 70, 75, 78, 80)
    ,create_student("노정현", 60, 65, 68, 70)
    ,create_student("노민재", 50, 55, 58, 60)
    ]

print(create_student)