from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email, )
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)
    
class Walkin(models.Model):
    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    walkin_date=models.DateField()
    sales_person=models.CharField(max_length=20,choices=choice)
    stu_name=models.CharField(max_length=20)
    mobile=models.IntegerField(max_length=10)
    parent_number=models.IntegerField(max_length=10)
    course_recom=models.CharField(max_length=20)
    join_date=models.DateField()

    def __str__(self):
        return self.sales_person

class CollectionReport(models.Model):

    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    cho=(
        ('2021-2022','2022-2023'),
      
        ('2023-2024','2024-2025'),
    
        ('2025-2026','2026-2027'),
     
        ('2027-2028','2028-2029'),
     
        ('2029-2030','2030-2031'),
    )
    financial_year=models.CharField(max_length=100,choices=cho)
    sales_person=models.CharField(max_length=20,choices=choice)
    from_date=models.DateField()
    to_date=models.DateField()
    def __str__(self):
        return self.category

class WalkinReport(models.Model):
    choi=(
        ('walkin',"Walkin"),
         ('register',"Register"),
          ('all',"All"),
        )
    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    cho=(
        ('2021-2022','2022-2023'),
      
        ('2023-2024','2024-2025'),
    
        ('2025-2026','2026-2027'),
     
        ('2027-2028','2028-2029'),
     
        ('2029-2030','2030-2031'),
    )
    financial_year=models.CharField(max_length=100,choices=cho)
    category=models.CharField(max_length=20,choices=choi)
    sales_person=models.CharField(max_length=20,choices=choice)
    from_date=models.DateField()
    to_date=models.DateField()
    def __str__(self):
        return self.category

class PendingPaymentReport(models.Model):
  
    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    cho=(
        ('2021-2022','2022-2023'),
      
        ('2023-2024','2024-2025'),
    
        ('2025-2026','2026-2027'),
     
        ('2027-2028','2028-2029'),
     
        ('2029-2030','2030-2031'),
    )
    financial_year=models.CharField(max_length=100,choices=cho)
   
    sales_person=models.CharField(max_length=20,choices=choice)
    from_date=models.DateField()
    to_date=models.DateField()
    def __str__(self):
        return self.category

class RegistrationReport(models.Model):
    choi=(
        ('walkin',"Walkin"),
         ('register',"Register"),
          ('all',"All"),
        )
    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    cho=(
        ('2021-2022','2022-2023'),
      
        ('2023-2024','2024-2025'),
    
        ('2025-2026','2026-2027'),
     
        ('2027-2028','2028-2029'),
     
        ('2029-2030','2030-2031'),
    )
    financial_year=models.CharField(max_length=100,choices=cho)
    category=models.CharField(max_length=20,choices=choi)
    sales_person=models.CharField(max_length=20,choices=choice)
    from_date=models.DateField()
    to_date=models.DateField()
    def __str__(self):
        return self.category

class ReferenceReport(models.Model):

    choice=(
        ('sheela',"Sheela"),
         ('saranya',"Saranya"),
          ('jeba',"Jeba"),
           ('bamila',"Bamila"),
            ('rolisha',"Rolisha")

        )
    cho=(
        ('2021-2022','2022-2023'),
      
        ('2023-2024','2024-2025'),
    
        ('2025-2026','2026-2027'),
     
        ('2027-2028','2028-2029'),
     
        ('2029-2030','2030-2031'),
    )
    financial_year=models.CharField(max_length=100,choices=cho)
   
    sales_person=models.CharField(max_length=20,choices=choice)
    from_date=models.DateField()
    to_date=models.DateField()
    def __str__(self):
        return self.category

# class FollowReport(models.Model):
#     choi=(
#         ('walkin',"Walkin"),
#          ('register',"Register"),
#           ('all',"All"),
#         )
#     choice=(
#         ('sheela',"Sheela"),
#          ('saranya',"Saranya"),
#           ('jeba',"Jeba"),
#            ('bamila',"Bamila"),
#             ('rolisha',"Rolisha")

#         )
#     cho=(
#         ('2021-2022','2022-2023'),
      
#         ('2023-2024','2024-2025'),
    
#         ('2025-2026','2026-2027'),
     
#         ('2027-2028','2028-2029'),
     
#         ('2029-2030','2030-2031'),
#     )
#     financial_year=models.IntegerField(max_length=100,choices=cho)
#     category=models.CharField(max_length=20,choices=choi)
#     sales_person=models.CharField(max_length=20,choices=choice)
#     from_date=models.DateField()
#     to_date=models.DateField()
#     def __str__(self):
#         return self.category


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Cro"), (4, "Stu"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name +" "+  self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class Course(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Stu(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Cro(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Staff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name



class Subject(models.Model):
    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    cro = models.ForeignKey(Cro, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportCro(models.Model):
    cro = models.ForeignKey(Cro, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackCro(models.Model):
    cro = models.ForeignKey(Cro, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#area of improvement
class Areaofimprovement(models.Model):
    #staff = models.ForeignKey(Staff,on_delete=models.CASCADE, default=1)
    cro = models.ForeignKey(Cro, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationCro(models.Model):
    cro = models.ForeignKey(Cro, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CroResult(models.Model):
    cro = models.ForeignKey(Cro, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Cro.objects.create(admin=instance)
        if instance.user_type == 4:
            Stu.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.cro.save()
    if instance.user_type == 4:
        instance.stu.save()
