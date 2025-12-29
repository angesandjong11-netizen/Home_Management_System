from django.db import models

# 1. Nurse (Infirmière)
class Nurse(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True) 
    special = models.CharField(max_length=100)

    def __str__(self):
        return f"Inf. {self.name}"

# 2. Doctor (Docteur)
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True)
    special = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    
    # NEW: Link any nurse to a doctor as their "primary" assistant
    assigned_nurse = models.ForeignKey(
        Nurse, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='primary_doctor'
    )

    def __str__(self):
        return f"Dr. {self.name} ({self.special})"

# 3. Patient
class Patient(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15, null=True)
    address = models.TextField()
    disease = models.CharField(max_length=200, null=True)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# 4. Appointment
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    # This allows choosing ANY nurse during the appointment, 
    # even if they aren't the doctor's primary assistant.
    nurse = models.ForeignKey(
        Nurse, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='appointment_sessions'
    )
    
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Rdv: {self.patient.name} avec {self.doctor.name} + {self.nurse.name if self.nurse else 'Seul'}"