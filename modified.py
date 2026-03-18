std_dic={}
class Student:
    def __init__(self,name,age,marks):
        self.name=name
        self.age=age
        self.marks=marks
        
    def get_grade(self):
        if self.marks>=90:
            return "A"
        elif self.marks>=80:
            return "B"
        else:
            return "C"

def add_student():
    name=input("Enter the name of student:").strip()
    lookup=name.lower()
    if lookup in std_dic:
        print(f"Error:{name} already exists")
        return
       
    age=int(input("Enter the age of student:"))
    marks=int(input("Enter the marks of student:"))
    std_dic[lookup]=Student(name,age,marks)
        
def get_report():
    for students in std_dic.values():
        print("================")
        print(f"Name:{students.name}\nAge:{students.age}\nMarks:{students.marks}\nGrade:{students.get_grade()}")  
        

def save_record(filename):
    with open(filename,"w") as f:
        for students in std_dic.values():
            result=f"Name:{students.name}\nAge:{students.age}\nMarks:{students.marks}\nGrade:{students.get_grade()}"
            f.write("-"*20 + "\n" + result + "\n")
            
while True:
    try:
        print("================")
        print("1. Add student")
        print("2. Show all reports")
        print("3. Save all reports")
        print("4. Exit")
        print("================")
        choice = int(input("Enter choice: "))
        
        if choice==1:
            add_student()
        elif choice==2:
            get_report()
        elif choice==3:
            save_record("record1.txt")
        else:
            break
    except ValueError:
        print("================")
        print("Error:Invalid input please enter valid input")
        print("================")
              