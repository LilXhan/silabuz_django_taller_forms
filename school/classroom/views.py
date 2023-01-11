from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .forms import StudentForm
from .models import Student, Classroom

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
            cleaned = form.cleaned_data
            c = Student.objects.create(**cleaned)
            c.save()

            return redirect('students')
