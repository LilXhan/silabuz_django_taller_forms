from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    class Meta:
        abstract = True 

class Classroom(models.Model):
    name = models.CharField(max_length=2)

    class Meta:
        db_table = 'classrooms'

    def __str__(self):
        return self.name


class Student(Person):
    idClassroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=None)

    class Meta:
        db_table = 'students'


class Teacher(Person):
    idClassroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teachers'