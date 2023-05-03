from django.urls import path
from . import views

urlpatterns=[
    path('',views.Home,name='Home'),
    path('Register',views.Register,name='Register'),
    path('AdminLogin',views.AdminLogin,name='AdminLogin'),
    path('addDetails',views.addDetails,name="addDetails"),
    path('getUserForAssign',views.getUserForAssign,name="getUserForAssign"),
    path('checkUsername',views.checkUsername,name="checkUsername"),
    path('fetchStudentData',views.fetchStudentData,name='fetchStudentData'),
    path('userLogin',views.userLogin,name="userLogin"),
    path('showAllUsersDetails',views.showAllUsersDetails,name="showAllUsersDetails"),
    path('updateTime',views.updateTime,name="updateTime"),
    path('recFileUpload',views.recFileUpload,name="recFileUpload"),
]