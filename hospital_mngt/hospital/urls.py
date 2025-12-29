from django.urls import path
from hospital.views import (
    About, Home, Contact, Login, Logout_admin, 
    view_doctor, add_doctor, delete_doctor,
    view_patient, add_patient, edit_patient, delete_patient,
    view_appointment, add_appointment, delete_appointment, edit_appointment,
    view_nurse, add_nurse, delete_nurse, edit_nurse,edit_doctor,
    Index, Landing
)

urlpatterns = [
    # Main Navigation
    path('', Landing, name='login_landing'),
    path('home/', Home, name='home'), 
    
    # Authentication & Static Pages
    path('login/', Login, name='login'),
    path('logout/', Logout_admin, name='logout_admin'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('dashboard/', Index, name='index'),

    # Doctor Management
    path('view_doctor/', view_doctor, name='view_doctor'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('delete_doctor/<int:pid>/', delete_doctor, name='delete_doctor'),
    path('edit_doctor/<int:pid>/', edit_doctor, name='edit_doctor'),

    # Patient Management
    path('view_patient/', view_patient, name='view_patient'),
    path('add_patient/', add_patient, name='add_patient'),
    path('edit_patient/<int:pid>/', edit_patient, name='edit_patient'),
    path('delete_patient/<int:pid>/', delete_patient, name='delete_patient'),

    # Nurse Management
    path('view_nurse/', view_nurse, name='view_nurse'),
    path('add_nurse/', add_nurse, name='add_nurse'),
    path('delete_nurse/<int:pid>/', delete_nurse, name='delete_nurse'),
    path('edit_nurse/<int:pid>/', edit_nurse, name='edit_nurse'), # <--- Added the missing comma here

    # Appointment Management
    path('view_appointment/', view_appointment, name='view_appointment'),
    path('add_appointment/', add_appointment, name='add_appointment'),
    path('edit_appointment/<int:pid>/', edit_appointment, name='edit_appointment'),
    path('delete_appointment/<int:pid>/', delete_appointment, name='delete_appointment'),
]