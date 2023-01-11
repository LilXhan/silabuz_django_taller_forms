from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from .forms import StudentForm
from .models import Student, Classroom


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
