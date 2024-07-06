import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def cro_home(request):
    cro = get_object_or_404(Cro, admin=request.user)
    total_subject = Subject.objects.filter(course=cro.course).count()
    total_attendance = AttendanceReport.objects.filter(cro=cro).count()
    total_present = AttendanceReport.objects.filter(cro=cro, status=True).count()
    if total_attendance == 0:
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(course=cro.course)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, cro=cro).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, cro=cro).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Cro Homepage'

    }
    return render(request, 'cro_template/home_content.html', context)


@ csrf_exempt
def cro_view_attendance(request):
    cro = get_object_or_404(Cro, admin=request.user)
    if request.method != 'POST':
        course = get_object_or_404(Course, id=cro.course.id)
        context = {
            'subjects': Subject.objects.filter(course=course),
            'page_title': 'View Attendance'
        }
        return render(request, 'cro_template/cro_view_attendance.html', context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, cro=cro)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def cro_apply_leave(request):
    form = LeaveReportCroForm(request.POST or None)
    cro = get_object_or_404(Cro, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportCro.objects.filter(cro=cro),
        'page_title': 'Apply for leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.cro = cro
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('cro_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "cro_template/cro_apply_leave.html", context)


def cro_feedback(request):
    form = FeedbackCroForm(request.POST or None)
    cro = get_object_or_404(Cro, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackCro.objects.filter(cro=cro),
        'page_title': 'Cro Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.cro = cro
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('cro_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "cro_template/cro_feedback.html", context)


def cro_view_profile(request):
    cro = get_object_or_404(Cro, admin=request.user)
    form = CroEditForm(request.POST or None, request.FILES or None,
                           instance=cro)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = cro.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                cro.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('cro_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "cro_template/cro_view_profile.html", context)


@csrf_exempt
def cro_fcmtoken(request):
    token = request.POST.get('token')
    cro_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        cro_user.fcm_token = token
        cro_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def cro_view_notification(request):
    cro = get_object_or_404(Cro, admin=request.user)
    notifications = NotificationCro.objects.filter(cro=cro)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "cro_template/cro_view_notification.html", context)


def cro_employee(request):
    cros = CustomUser.objects.filter(user_type=3)
    context = {
        'cros': cros,
        'page_title': 'Manage Cros'
    }
    return render(request, "cro_template/cro_employee.html", context)



def cro_view_result(request):
    cro = get_object_or_404(Cro, admin=request.user)
    results = CroResult.objects.filter(cro=cro)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "cro_template/cro_view_result.html", context)

def cro_view_remarks(request):
    cro = get_object_or_404(Cro, admin=request.user)
    remarks = Areaofimprovement.objects.filter(cro=cro)
    context = {
        'remarks': remarks,
        'page_title': "View Remarks"
    }
    return render(request, "cro_template/cro_view_remarks.html", context)

def cro_walkin(request):
    walks=   Walkin.objects.all()
    return render(request,"cro_template/cro_walkin.html",{'walks':walks})


# def view_walkin_report(request):
#     walk_report=   WalkinReport.objects.all()
#     return render(request,"cro_template/view_walkin_report.html",{'walks':walk_report})

# def walkin_stu(request):
#     return render(request,"cro_template/walkinstu.html")
def walkin_report(request):
    if request.method == 'POST':
        form = WalkinReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('walkin_report')  # Redirect to a success page
    else:
        form = WalkinReportForm()

    
    return render(request,"cro_template/walkinreport.html",{'form': form})

def collection_report(request):
    if request.method == 'POST':
        form = CollectionReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collection_report')  # Redirect to a success page
    else:
        form = CollectionReportForm()

    return render(request,"cro_template/collectionreport.html",{'form': form})
def pendingpayment_report(request):
    if request.method == 'POST':
        form = PendingPaymentReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pendingpayment_report')  # Redirect to a success page
    else:
        form = PendingPaymentReportForm()

    return render(request,"cro_template/ppreport.html",{'form': form})
def registration_report(request):
    if request.method == 'POST':
        form = RegistrationReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_report')  # Redirect to a success page
    else:
        form =  RegistrationReportForm()


    return render(request,"cro_template/registrationreport.html",{'form': form})



def refernce_report(request):
    if request.method == 'POST':
        form = ReferenceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('refernce_report')  # Redirect to a success page
    else:
        form =  ReferenceReportForm()
    return render(request,"cro_template/referencereport.html",{'form': form})

def walkin_stu(request):
    if request.method == 'POST':
        form = WalkinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cro_walkin')  # Redirect to a success page
    else:
        form = WalkinForm()
    return render(request, 'cro_template/walkinstu.html', {'form': form})



# def cro_normal_walkin (request):
#     form = StuForm(request.POST or None, request.FILES or None)
#     context = {'form': form, 'page_title': 'Add Registration'}
#     if request.method == 'POST':            
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 address = form.cleaned_data.get('address')
#                 email = form.cleaned_data.get('email')
#                 gender = form.cleaned_data.get('gender')
#                 password = form.cleaned_data.get('password')
#                 course = form.cleaned_data.get('course')
#                 passport = request.FILES.get('profile_pic')
#                 fs = FileSystemStorage()
#                 filename = fs.save(passport.name, passport)
              
#                 try:
#                     user = CustomUser.objects.create_user(
#                         email=email, password=password,user_type=4,  first_name=first_name, last_name=last_name)
#                     user.gender = gender
#                     user.address = address
#                     user.stu.course = course
#                     user.save()
#                     messages.success(request, "Successfully Added")
#                     return redirect(reverse('cro_normal_walkin'))
#                 except Exception as e:
#                     messages.error(request, "Could Not Add " + str(e))
#             else:
#                 messages.error(request, "Please fulfil all requirements")

            

#     return render(request, 'cro_template/cro_normal_walkin.html', context)

# def cro_registration (request):
#     form = StuForm(request.POST or None, request.FILES or None)
#     context = {'form': form, 'page_title': 'Add Registration'}
#     if request.method == 'POST':            
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 address = form.cleaned_data.get('address')
#                 email = form.cleaned_data.get('email')
#                 gender = form.cleaned_data.get('gender')
#                 password = form.cleaned_data.get('password')
#                 course = form.cleaned_data.get('course')
#                 passport = request.FILES.get('profile_pic')
#                 fs = FileSystemStorage()
#                 filename = fs.save(passport.name, passport)
#                 passport_url = fs.url(filename)
              
#                 try:
#                     user = CustomUser.objects.create_user(
#                         email=email, password=password,user_type=4,  first_name=first_name, last_name=last_name,profile_pic=passport_url)
#                     user.gender = gender
#                     user.address = address
#                     user.stu.course = course
#                     user.save()
#                     messages.success(request, "Successfully Added")
#                     return redirect(reverse('cro_registration'))
#                 except Exception as e:
#                     messages.error(request, "Could Not Add " + str(e))
#             else:
#                 messages.error(request, "Please fulfil all requirements")
 
            

#     return render(request, 'cro_template/managestu.html', context)

# def stu_registration (request):
#     form = StuForm(request.POST or None, request.FILES or None)
#     context = {'form': form, 'page_title': 'Add Registration'}
#     if request.method == 'POST':            
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 address = form.cleaned_data.get('address')
#                 email = form.cleaned_data.get('email')
#                 gender = form.cleaned_data.get('gender')
#                 password = form.cleaned_data.get('password')
#                 course = form.cleaned_data.get('course')
#                 passport = request.FILES.get('profile_pic')
#                 fs = FileSystemStorage()
#                 filename = fs.save(passport.name, passport)
#                 passport_url = fs.url(filename)
              
#                 try:
#                     user = CustomUser.objects.create_user(
#                         email=email, password=password, user_type=4,  first_name=first_name, last_name=last_name,profile_pic=passport_url)
                     
#                     user.gender = gender
#                     user.address = address
#                     user.stu.course = course
#                     user.save()
#                     messages.success(request, "Successfully Added")
#                     return redirect(reverse('stu_registration'))
#                 except Exception as e:
#                     messages.error(request, "Could Not Add " + str(e))
#             else:
#                 messages.error(request, "Please fulfil all requirements")

            

#     return render(request, 'cro_template/stu_registration.html', context)


def add_stu(request):
    form = StuForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Stu'}
    if request.method == 'POST':            
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                address = form.cleaned_data.get('address')
                email = form.cleaned_data.get('email')
                gender = form.cleaned_data.get('gender')
                password = form.cleaned_data.get('password')
                course = form.cleaned_data.get('course')
                passport = request.FILES.get('profile_pic')
                fs = FileSystemStorage()
                filename = fs.save(passport.name, passport)
                passport_url = fs.url(filename)
                try:
                    user = CustomUser.objects.create_user(
                        email=email, password=password, user_type=4, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                    user.gender = gender
                    user.address = address
                    user.stu.course = course
                    user.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add_stu'))
                except Exception as e:
                    messages.error(request, "Could Not Add " + str(e))
            else:
                messages.error(request, "Please fulfil all requirements")

            

    return render(request, 'cro_template/stu_registration.html', context)


def manage_stu(request):
    allStu = CustomUser.objects.filter(user_type=4)
    context = {
        'allStu': allStu,
        'page_title': 'Manage Student'
    }
    return render(request, "cro_template/manage_stu.html", context)


def delete_stu(request, stu_id):
    stu = get_object_or_404(CustomUser, stu__id=stu_id)
    stu.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_stu'))


def edit_stu(request, stu_id):
    stu = get_object_or_404(Stu, id=stu_id)
    form = StuForm(request.POST or None, instance=stu)
    context = {
        'form': form,
        'stu_id': stu_id,
        'page_title': 'Edit Stu'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                # Access the admin directly from the staff object
                user = stu.admin
                
                # Update user fields
                user.username = form.cleaned_data.get('username')
                user.email = form.cleaned_data.get('email')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.gender = form.cleaned_data.get('gender')
                user.address = form.cleaned_data.get('address')
                
                # Check and update password
                password = form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                
                # Check and update profile picture
                passport = request.FILES.get('profile_pic')
                if passport:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                
                # Save user and staff objects
                user.save()
                stu.course = form.cleaned_data.get('course')
                stu.save()
                
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_stu', args=[stu_id]))
            except Exception as e:
                messages.error(request, f"Could Not Update: {e}")
        else:
            messages.error(request, "Please fill the form properly")
    return render(request, "cro_template/edit_stu_template.html", context)

