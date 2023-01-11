from django.urls import path 
from . import views

urlpatterns = [
    path('formAlum/', views.StudentFormView.as_view(), name='form-alumn'),
    path('formAlum/<str:name>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('alum/', views.StudentView.as_view(), name='students')
]