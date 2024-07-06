"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, cro_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("course/add", hod_views.add_course, name='add_course'),
    path("subject/add", hod_views.add_course, name='add_subject'),
    path("send_cro_notification/", hod_views.send_cro_notification,
         name='send_cro_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_cro", hod_views.admin_notify_cro,
         name='admin_notify_cro'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("cro/view/feedback/", hod_views.cro_feedback_message,
         name="cro_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("cro/view/leave/", hod_views.view_cro_leave,
         name="view_cro_leave",),
     # path("cro/view/report/", cro_views.view_walkin_report,
     #     name="view_walkin_report",),
     path("admin/view/report/", hod_views.view_walkin_report,
         name="view_walkin_report",),
     path("admin/view/colreport/", hod_views.view_collection_report,
         name="view_collection_report",),
     path("admin/view/regreport/", hod_views.view_reg_report,
         name="view_reg_report",),
     path("admin/view/pendpayreport/", hod_views.view_pendpay_report,
         name="view_pendpay_report",),
     path("admin/view/referencereport/", hod_views.view_reference_report,
         name="view_reference_report",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("cro/add/", hod_views.add_cro, name='add_cro'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("cro/manage/", hod_views.manage_cro, name='manage_cro'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("cro/delete/<int:cro_id>",
         hod_views.delete_cro, name='delete_cro'),
    path("cro/edit/<int:cro_id>",
         hod_views.edit_cro, name='edit_cro'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),
    path('validate_name/', hod_views.validate_name, name='validate_name'),



    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/improvement/", staff_views.area_of_improvement, name='area_of_improvement'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance,
         name='staff_update_attendance'),
    path("staff/get_cros/", staff_views.get_cros, name='get_cros'),
    path("staff/attendance/fetch/", staff_views.get_cro_attendance,
         name='get_cro_attendance'),
    path("staff/attendance/save/",
         staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/",
         staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path("staff/result/edit/", EditResultView.as_view(),
         name='edit_cro_result'),
    path('staff/result/fetch/', staff_views.fetch_cro_result,
         name='fetch_cro_result'),



    # Cro
    path("cro/home/", cro_views.cro_home, name='cro_home'),
    path("cro/view/attendance/", cro_views.cro_view_attendance,
         name='cro_view_attendance'),
    path("cro/apply/leave/", cro_views.cro_apply_leave,
         name='cro_apply_leave'),
    path("cro/feedback/", cro_views.cro_feedback,
         name='cro_feedback'),
    path("cro/view/profile/", cro_views.cro_view_profile,
         name='cro_view_profile'),
    path("cro/fcmtoken/", cro_views.cro_fcmtoken,
         name='cro_fcmtoken'),
    path("cro/view/notification/", cro_views.cro_view_notification,
         name="cro_view_notification"),
     path("cro/view/employee/", cro_views.cro_employee,
         name="cro_employee"),
    path('cro/view/result/', cro_views.cro_view_result,
         name='cro_view_result'),
    path('cro/view/remarks/', cro_views.cro_view_remarks,
         name='cro_view_remarks'),

     path('cro/view/walkin/', cro_views.cro_walkin,
         name='cro_walkin'), 
     path('cro/view/walkinstu/', cro_views.walkin_stu,
         name='walkin_stu'), 

 path('cro/view/walkinrep/', cro_views.walkin_report,
         name='walkin_report'),
     path('cro/view/collectionrep/', cro_views.collection_report,
         name='collection_report'),
     path('cro/view/pendingpaymentrep/', cro_views.pendingpayment_report,
         name='pendingpayment_report'),
     path('cro/view/registrationrep/', cro_views.registration_report,
         name='registration_report'),
     path('cro/view/referencerep/', cro_views.refernce_report,
         name='refernce_report'),
         
     # path('cro/view/normal/', cro_views.cro_normal_walkin,
     #     name='cro_normal_walkin'),
     # path('cro/view/registration/', cro_views.cro_registration,
     #     name='cro_registration'),
      path('cro/view/stureg/', cro_views.add_stu,
         name='add_stu'),
            path('cro/view/studetails/', cro_views.manage_stu,
         name='manage_stu'),
     path("stu/edit/<int:stu_id>", cro_views.edit_stu, name='edit_stu'),
    path("stu/delete/<int:stu_id>",
         cro_views.delete_stu, name='delete_stu'),



]
