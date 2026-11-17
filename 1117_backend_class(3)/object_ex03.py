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


#학생을 처리하는 함수
#학생 한명의 총점을 리턴하는 함수 : student_get_sum(student)
def student_get_sum(student):
    score_sum=student["korean"] + student["english"] + student["math"] + student["science"]
    return score_sum
#학생 한명의 평균을 리턴하는 : student_get_agv(student)
def student_get_agv(student):
    score_sum = student_get_sum(student)
    score_avg=score_sum/4
    return score_avg

#학생 한명의 점수를 출력하는 함수 : student_to_string(student)
def student_to_string(student):
    return "{}\t{}\t{}".format(student["name"], student_get_sum(student), student_get_agv(student))

print("이름","총점","평균",sep="\t")
for student in students:
        print(student_to_string(student))






