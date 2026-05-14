class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: {self.name}, {self.age}"

class Student(Person):
    _id_counter = 0
    def __init__(self, name, age, group, gpa):
        super().__init__(name, age)
        self.group = group
        self.__gpa = gpa
        self.id = Student._id_counter
        Student._id_counter += 1

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if 0.0 <= value <= 4.0:
            self.__gpa = value

    def __str__(self):
        return f"ID: {self.id} Student: {self.name}, Group: {self.group}, GPA: {self.gpa}"