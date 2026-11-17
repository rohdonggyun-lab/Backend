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

print(students)