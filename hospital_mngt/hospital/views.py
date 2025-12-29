from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, Nurse

# --- Navigation & Public Pages ---

def Landing(request):
    """Public Landing Page"""
    return render(request, 'landing.html')

def Contact(request):
    """Contact page accessible to all"""
    return render(request, 'contact.html')

def Home(request):
    """Redirects to dashboard if logged in, else landing"""
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, 'landing.html')

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('home')
        else:
            error = "yes"
    return render(request, 'login.html', {'error': error})

def Logout_admin(request):
    logout(request)
    return redirect('login')

# --- Secured Areas (@login_required) ---

@login_required(login_url='login')
def About(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def Index(request):
    """Dashboard Statistics"""
    if not request.user.is_staff:
        return redirect('login')
    
    context = {
        'd_count': Doctor.objects.count(),
        'p_count': Patient.objects.count(),
        'a_count': Appointment.objects.count(),
        'n_count': Nurse.objects.count(),
        # Count appointments where a specific nurse was assigned
        'binome_count': Appointment.objects.filter(nurse__isnull=False).count(),
    }
    return render(request, 'index.html', context)

# --- Doctor Management ---

@login_required(login_url='login')
def view_doctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_doctor.html', {'doctors': doctors})

@login_required(login_url='login')
def add_doctor(request):
    nurses = Nurse.objects.all()
    if request.method == "POST":
        n = request.POST.get('name')
        m = request.POST.get('mobile')
        s = request.POST.get('special')
        sal = request.POST.get('salary')
        nurse_id = request.POST.get('nurse')
        
        assigned_nurse_obj = Nurse.objects.filter(id=nurse_id).first() if nurse_id else None

        Doctor.objects.create(
            name=n, 
            mobile=m, 
            special=s, 
            salary=sal,
            assigned_nurse=assigned_nurse_obj  # FIXED: matches models.py
        )
        return redirect('view_doctor')
        
    return render(request, 'add_doctor.html', {'nurses': nurses})

@login_required(login_url='login')
def edit_doctor(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    nurses = Nurse.objects.all() # Added to allow changing assigned nurse
    if request.method == "POST":
        doctor.name = request.POST.get('name')
        doctor.mobile = request.POST.get('mobile')
        doctor.special = request.POST.get('special')
        doctor.salary = request.POST.get('salary')
        
        nurse_id = request.POST.get('nurse')
        doctor.assigned_nurse = Nurse.objects.filter(id=nurse_id).first() if nurse_id else None
        
        doctor.save()
        return redirect('view_doctor')
    return render(request, 'edit_doctor.html', {'doctor': doctor, 'nurses': nurses})

@login_required(login_url='login')
def delete_doctor(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    doctor.delete()
    return redirect('view_doctor')

# --- Nurse Management ---

@login_required(login_url='login')
def view_nurse(request):
    nurses = Nurse.objects.all()
    return render(request, 'view_nurse.html', {'nurses': nurses})

@login_required(login_url='login')
def add_nurse(request):
    if request.method == "POST":
        n = request.POST.get('name')
        m = request.POST.get('mobile')
        s = request.POST.get('special')
        Nurse.objects.create(name=n, mobile=m, special=s)
        return redirect('view_nurse')
    return render(request, 'add_nurse.html')

@login_required(login_url='login')
def edit_nurse(request, pid):
    nurse = get_object_or_404(Nurse, id=pid)
    if request.method == "POST":
        nurse.name = request.POST.get('name')
        nurse.mobile = request.POST.get('mobile')
        nurse.special = request.POST.get('special')
        nurse.save()
        return redirect('view_nurse')
    return render(request, 'edit_nurse.html', {'nurse': nurse})

@login_required(login_url='login')
def delete_nurse(request, pid):
    nurse = get_object_or_404(Nurse, id=pid)
    nurse.delete()
    return redirect('view_nurse')

# --- Patient Management ---

@login_required(login_url='login')
def view_patient(request):
    patients = Patient.objects.all()
    return render(request, 'view_patient.html', {'patients': patients})

@login_required(login_url='login')
def add_patient(request):
    doctors = Doctor.objects.all()
    if request.method == "POST":
        n = request.POST.get('name')
        g = request.POST.get('gender')
        m = request.POST.get('mobile')
        a = request.POST.get('address')
        d_name = request.POST.get('disease')
        doc_id = request.POST.get('doctor')
        
        doctor_obj = Doctor.objects.filter(id=doc_id).first() if doc_id else None
        Patient.objects.create(name=n, gender=g, mobile=m, address=a, disease=d_name, assigned_doctor=doctor_obj)
        return redirect('view_patient')
    return render(request, 'add_patient.html', {'doctors': doctors})

@login_required(login_url='login')
def edit_patient(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        patient.name = request.POST.get('name')
        patient.gender = request.POST.get('gender')
        patient.mobile = request.POST.get('mobile')
        patient.address = request.POST.get('address')
        patient.disease = request.POST.get('disease')
        doc_id = request.POST.get('doctor')
        patient.assigned_doctor = Doctor.objects.filter(id=doc_id).first() if doc_id else None
        patient.save()
        return redirect('view_patient')
    return render(request, 'edit_patient.html', {'patient': patient, 'doctors': doctors})

@login_required(login_url='login')
def delete_patient(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    patient.delete()
    return redirect('view_patient')

# --- Appointment Management ---

@login_required(login_url='login')
def view_appointment(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointment.html', {'appointments': appointments})

@login_required(login_url='login')
def add_appointment(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    nurses = Nurse.objects.all()
    if request.method == "POST":
        doc_id = request.POST.get('doctor')
        pat_id = request.POST.get('patient')
        nurse_id = request.POST.get('nurse')
        d = request.POST.get('date')
        t = request.POST.get('time')
        
        doctor_obj = get_object_or_404(Doctor, id=doc_id)
        patient_obj = get_object_or_404(Patient, id=pat_id)
        nurse_obj = Nurse.objects.filter(id=nurse_id).first() if nurse_id else None
        
        Appointment.objects.create(
            doctor=doctor_obj, 
            patient=patient_obj, 
            nurse=nurse_obj, 
            date=d, 
            time=t
        )
        return redirect('view_appointment')
    return render(request, 'add_appointment.html', {'doctors': doctors, 'patients': patients, 'nurses': nurses})

@login_required(login_url='login')
def edit_appointment(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    doctors = Doctor.objects.all()
    nurses = Nurse.objects.all()
    patients = Patient.objects.all()
    if request.method == "POST":
        appointment.doctor = get_object_or_404(Doctor, id=request.POST.get('doctor'))
        appointment.nurse = Nurse.objects.filter(id=request.POST.get('nurse')).first()
        appointment.patient = get_object_or_404(Patient, id=request.POST.get('patient'))
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.save()
        return redirect('view_appointment')
    return render(request, 'edit_appointment.html', {
        'appointment': appointment, 'doctors': doctors, 'nurses': nurses, 'patients': patients
    })

@login_required(login_url='login')
def delete_appointment(request, pid):
    app = get_object_or_404(Appointment, id=pid)
    app.delete()
    return redirect('view_appointment')