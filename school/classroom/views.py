from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .forms import StudentForm, TeacherForm
from .models import Student, Classroom, Teacher

# Task 2

class TeacherDetailView(View):

    def get(self, request, name):
        
        context = {}
        
        context['name'] = name
        context['last_name'] = request.session['last_name']
        id_classroom = Classroom.objects.get(pk=request.session['idClassroom'])
        context['classroom'] = id_classroom

        return render(request, 'teacher-detail.html', context)

class TeacherFormView(View):

    def get(self, request):
        form = TeacherForm()

        context  = {
            'form': form
        }

        return render(request, 'forms/teacher.html', context)

    def post(self, request):

        form = TeacherForm(request.POST)

        if form.is_valid():
            # save in db
            cleaned_data = form.cleaned_data
            t = Teacher.objects.create(**cleaned_data)
            t.save()

            # request.session
            request.session['last_name'] = cleaned_data['last_name']
            request.session['idClassroom'] = cleaned_data['idClassroom'].id

            return redirect('teacher-detail', name=cleaned_data['name'])
 
# Task 1

class StudentDetailView(View):

    def get(self, request, name):
        context = {
            'name': name,
            'last_name': request.session['last_name'],
            'aula': Classroom.objects.get(pk=request.session['id'])
        }

        return render(request, 'student-detail.html', context)

class StudentView(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context 

class StudentFormView(View):

    def get(self, request):

        form = StudentForm()

        context = {
            'form': form
        }

        return render(request, 'forms/student.html', context)

    def post(self, request):
        form = StudentForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            s = Student.objects.create(**cleaned_data)
            s.save()
            request.session['last_name'] = cleaned_data['last_name']
            request.session['id'] = cleaned_data['idClassroom'].id 
            return redirect('student-detail', name=cleaned_data['name'])             
