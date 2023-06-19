from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'), 
    path('Admin_login/',views.Admin_login,name='Admin_login'), 
    path('Officer_login/',views.Officer_login,name='Officer_login'), 
    path('AddOfficer/',views.AddOfficer,name='AddOfficer'),  
    path('logout/',views.logout,name='logout'), 
    path('ChangePassword/',views.ChangePassword,name='ChangePassword'), 
    path('AddCase/',views.AddCase,name='AddCase'), 
    path('ViewSuspects/',views.ViewSuspects,name='ViewSuspects'), 
    path('ViewEvidence/',views.ViewEvidence,name='ViewEvidence'), 
    path('ViewCaseHistory/',views.ViewCaseHistory,name='ViewCaseHistory'), 
    path('GenerateResults/',views.GenerateResults,name='GenerateResults'), 
    path('AddSuspects/',views.AddSuspects,name='AddSuspects'),
    path('AddEvidence/',views.AddEvidence,name='AddEvidence'),
    path('SuspectsList/<int:id>',views.SuspectsList,name='SuspectsList'),
    path('EvidenceList/<int:id>',views.EvidenceList,name='EvidenceList'),
    path('CaseHistoryList/<int:id>',views.CaseHistoryList,name='CaseHistoryList'),
    path('ViewCase/',views.ViewCase,name='ViewCase'),
    path('get_response/',views.get_response,name='get_response'),
    path('Results/<int:id>',views.Results,name='Results'),
    ]