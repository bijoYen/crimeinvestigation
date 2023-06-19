from django.shortcuts import render,redirect
from django import template
from django.contrib.sessions.models import Session
import string
import datetime
from django.core.files.storage import FileSystemStorage
from django.utils.module_loading import import_string
from datetime import date
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Avg, Max, Min, Sum, Count

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import pandas as pd
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from AppCriminal.models import *

import operator



def home(request):
    return render(request,'home.html',{})


def about(request):
    return render(request,"about.html",{})


def Admin_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if Admin_Details.objects.filter(Username=Username, Password=password).exists():
                user = Admin_Details.objects.get(Username=Username, Password=password)
                request.session['type_id'] = 'Admin'
                request.session['username'] = Username
                request.session['login'] = 'Yes'
                return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/Admin_login/')
    else:
        return render(request, 'Admin_login.html', {})



def Officer_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if Officer_details.objects.filter(Username=Username, Password=password).exists():
            user = Officer_details.objects.all().filter(Username=Username, Password=password)
            request.session['Officer_id'] = str(user[0].id)
            request.session['type_id'] = 'Officer'
            request.session['username'] = Username
            request.session['login'] = 'Yes'
            return redirect('/')
            
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/Officer_login/')
    else:
        return render(request, 'Officer_login.html', {})

        




def ChangePassword(request):
    if request.method == 'POST':
        CurrentPassword = request.POST['CurrentPassword']
        NewPassword = request.POST['NewPassword']
        ConfirmPassword = request.POST['ConfirmPassword']

        uid = request.session['User_id']
        CurrUser = User_details.objects.all().filter(id=uid)
        if CurrUser[0].Password == CurrentPassword:
            if NewPassword == ConfirmPassword:
                User_details.objects.filter(id=uid).update(Password=NewPassword)
                messages.info(request,'Passwords Changed Successfully')
                return render(request, 'ChangePassword.html', {})
            else:
                messages.info(request,'New Passwords doesnt match')
                return render(request, 'ChangePassword.html', {})
        else:
            messages.info(request,'Current Password doesnt match')
            return render(request, 'ChangePassword.html', {})
        
    else:
        return render(request, 'ChangePassword.html', {})



def AddOfficer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Username = request.POST['Username']
        Email = request.POST['Email']        
        Mobile = request.POST['Mobile']
        Image = request.FILES['Image']
        Address =  request.POST['Address']
        State =  request.POST['State']
        City =  request.POST['City']

        password_characters = string.ascii_letters + string.digits 
        password = ''.join(random.choice(password_characters) for i in range(8))
        print("Random string password is:", password)


        if Officer_details.objects.filter(Username=Username).exists():
            messages.info('request','Username taken')
            return redirect('/AddOfficer/')

        elif Officer_details.objects.filter(Email=Email).exists():
            messages.info('request','Email Id taken')
            return redirect('/AddOfficer/')

        else:

            senderemail = 'mailtestingw@gmail.com'
            senderpassword = 'testmail1234'
            send_to_email = Email
            subject = 'Registration Successfull'
            

            messagePlain = 'The password for your login is : '+password

            msg = MIMEMultipart('alternative')
            msg['From'] = senderemail
            msg['To'] = send_to_email
            msg['Subject'] = subject

            # Attach both plain and HTML versions
            msg.attach(MIMEText(messagePlain, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(senderemail, senderpassword)
            text = msg.as_string()
            server.sendmail(senderemail, send_to_email, text)
            server.quit()
            
   
            register1 = Officer_details( FirstName = first_name,LastName = last_name,Username =Username,Email = Email,Password = password,mobile = Mobile,Address = Address,City = City,State = State,Image = Image)
            register1.save()

            messages.info(request,'Officer Added Successful and Credentials are sent to Officer on email')
            return redirect('/AddOfficer/')
    else:
        return render(request, 'AddOfficer.html', {})



def logout(request):
    Session.objects.all().delete()
    return redirect('/')

 
def AddCase(request):
    if request.method == 'POST':
        CaseName = request.POST['Case_Name']
        Note = request.POST['Note']
        OfficerName = request.POST['Officer_Name']
        Case_Type = request.POST['Case_Type']

        if Case_details.objects.filter(OfficerID=OfficerName, Status="Pending").exists():
            messages.info(request,'Officer Already Assigned to a Case.')
            return redirect('/AddCase/')
        else:
            Cid = list(Case_details.objects.aggregate(Max('CaseID')).values())[0] or 0
            finalCid = int(Cid)+1
            cid = finalCid
            register1 = Case_details(CaseID=cid,OfficerID=OfficerName,Name=CaseName,CaseType=Case_Type,Note=Note,GuiltyRelation="",Status="Pending",GuiltyID="")
            register1.save()

            messages.info(request,'Case Added Successful')
            return redirect('/AddCase/')           
    else:
        Officer = Officer_details.objects.all()
        return render(request, 'AddCase.html', {'Officer':Officer})



def ViewSuspects(request):
    if request.method == 'POST':
        return redirect('/ViewSuspects/')
    else:
        if request.session['type_id'] == 'Admin':
            Case = Case_details.objects.all()
            return render(request, 'ViewSuspects.html', {'Case':Case  })
        else:
            Oid = request.session['Officer_id']
            print("Oid",Oid)
            Case = Case_details.objects.all().filter(OfficerID=Oid)
            print(Case)
            return render(request, 'ViewSuspects.html', {'Case':Case  })
        



def ViewEvidence(request):
    if request.method == 'POST':
        return redirect('/ViewEvidence/')
    else:
        if request.session['type_id'] == 'Admin':
            Case = Case_details.objects.all()
            return render(request, 'ViewEvidence.html', {'Case':Case  })
        else:
            Oid = request.session['Officer_id']
            print("Oid",Oid)
            Case = Case_details.objects.all().filter(OfficerID=Oid)
            print(Case)
            return render(request, 'ViewEvidence.html', {'Case':Case  })
        


def ViewCaseHistory(request):
    if request.method == 'POST':
        return redirect('/ViewCaseHistory/')
    else:
        if request.session['type_id'] == 'Admin':
            Case = Case_details.objects.all()
            return render(request, 'ViewCaseHistory.html', {'Case':Case})
        else:
            Oid = request.session['Officer_id']
            print("Oid",Oid)
            Case = Case_details.objects.all().filter(OfficerID=Oid)
            print(Case)
            return render(request, 'ViewCaseHistory.html', {'Case':Case})
        

def GenerateResults(request):
    if request.method == 'POST':
        return redirect('/GenerateResults/')
    else:
        Case = Case_details.objects.all().filter(Status="Pending")
        return render(request, 'GenerateResults.html', {'Case':Case})

def AddSuspects(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Email = request.POST['Email']
        Mobile = request.POST['Mobile']
        Image = request.FILES['Image']
        Address = request.POST['Address']
        Relation = request.POST['Relation']
        Rank = 0
        Note = request.POST['Note']
        Case_id = request.POST['Case_id']
        OfficerID  = request.POST['OfficerID']
          
        register1 = Suspects_details( CaseID = Case_id,Name = first_name+" "+last_name,OfficerID  = OfficerID,Email = Email,mobile = Mobile,Address = Address,Relation = Relation,Date = datetime.date.today(),Rank = Rank,Image = Image,Note = Note)
        register1.save()
             
        register1 = CaseHistory(CaseID = Case_id,History = "New Suspect Added to the case : "+first_name+" "+last_name,Date = datetime.date.today(),OfficerID = request.session['Officer_id'])
        register1.save()

        messages.info(request,'Suspects Added Successful')
        return redirect('/AddSuspects/')
    else:
        Case = Case_details.objects.all().filter(OfficerID = request.session['Officer_id'])
        Oid = request.session['Officer_id']
        return render(request, 'AddSuspects.html', {'Case':Case,'Oid':Oid})


def AddEvidence(request):
    if request.method == 'POST':
        Case_id = request.POST['Case_id']
        Evidence = request.POST['Evidence']
        Image = request.FILES['Image']
        SuspectName = request.POST['Suspect_Name']
        Type = request.POST['Type']
        Note = request.POST['Note']
        Rank = request.POST['Rank']
        OfficerName = request.POST['Officer_Name']
          
        regi = Evidence_Details(CaseID = Case_id,Evidence = Evidence,Type = Type,Image=Image,Suspects = SuspectName,Date=datetime.date.today(),Note = Note,Rank = Rank,OfficerID = OfficerName )
        regi.save()


        Suspect = Suspects_details.objects.all().filter(id=SuspectName)

        updatedrank = int(Suspect[0].Rank) + int(Rank)
        Suspects_details.objects.filter(id=SuspectName).update(Rank=updatedrank)


            
        register1 = CaseHistory(CaseID = Case_id,History = "New Evidence Added to the case : "+Evidence+" and the Suspect is"+SuspectName ,Date = datetime.date.today(),OfficerID = request.session['Officer_id'])
        register1.save()

        messages.info(request,'Evidence Added Successful')
        return redirect('/AddEvidence/')
    else:
        Case = Case_details.objects.all().filter(OfficerID = request.session['Officer_id'])
        Oid = request.session['Officer_id']
        return render(request, 'AddEvidence.html', {'Case':Case,'Oid':Oid})



def SuspectsList(request,id):
    if request.method == 'POST':                   
        return redirect('/ViewSuspects',{})
    else:
        Sus = Suspects_details.objects.all().filter(CaseID=id)
        cnt = Suspects_details.objects.all().filter(CaseID=id).count()
        return render(request, 'SuspectsList.html', {'Sus':Sus,'cnt':cnt})


def EvidenceList(request,id):
    if request.method == 'POST':                   
        return redirect('/BlogDetails/',{})
    else:
        Evi = Evidence_Details.objects.all().filter(CaseID=id)
        cnt = Evidence_Details.objects.all().filter(CaseID=id).count()
        return render(request, 'EvidenceList.html', {'Evi':Evi,'cnt':cnt})



def CaseHistoryList(request,id):
    if request.method == 'POST':                   
        return redirect('/BlogDetails/',{})
    else:
        History = CaseHistory.objects.all().filter(CaseID=id)
        return render(request, 'CaseHistoryList.html', {'History':History})



def ViewCase(request):
    if request.method == 'POST':
        return redirect('/ViewSuspects/')
    else:
        Case = Case_details.objects.all()
        return render(request, 'ViewCase.html', {'Case':Case})


def get_response(request):
    caseId = request.POST.get('caseId')
    Sus = Suspects_details.objects.all().filter(CaseID=caseId)
    SusCount = Suspects_details.objects.all().filter(CaseID=caseId).count()

    if SusCount > 0:
        SuspectLists = ""
        for r in Sus:
            SuspectLists += str(r.id)+"&"+r.Name+"%" 
        print(SuspectLists)
        answer = SuspectLists
    else:
        answer = "No Suspects Are Available for the Case Kindly add Suspects to add Evidence"

    data = {
        'respond': answer
        }
    return JsonResponse(data)


def Results(request,id):
    #print("id",id)
    Case = Case_details.objects.all().filter(CaseID=id)
    CaseType = Case[0].CaseType
    PreviosCase = Case_details.objects.all().filter(CaseType=CaseType,Status="Solved")
    #print('Previous',PreviosCase.count())
    relationPoint = 0
    previousrelation = ""
    thisdict = {}

    if PreviosCase.count() > 0:
        #print("enter if")
        result = Case_details.objects.all().filter(CaseType=CaseType,Status="Solved").values('GuiltyRelation').order_by('GuiltyRelation').annotate(count=Count('GuiltyRelation'))
        previousrelation = result[0]["GuiltyRelation"]
        #print('previousrelation',previousrelation)

    else:
        #print("enter else")
        previousrelation = ""

    sus =  Suspects_details.objects.all().filter(CaseID=id)

    for r in sus:
        #print()
        #print('id',r.id)

        if r.Relation == "Family":
            relationPoint = 3

        elif r.Relation == "Business Partner":
            relationPoint = 4

        elif r.Relation == "Worker":
            relationPoint = 2

        elif r.Relation == "Close Friend":
            relationPoint = 3

        elif r.Relation == "Friend":
            relationPoint = 2

        elif r.Relation == "Colleague":
            relationPoint = 2

        elif r.Relation == "Others":
            relationPoint = 1

        #print('for previousrelation',previousrelation)


        if r.Relation == previousrelation and r.Relation != "":
            relationPoint += 2


        #print('relationPoint',relationPoint)

        RankPoint = r.Rank

        LogicalRank = Evidence_Details.objects.all().filter(Type="Logical",CaseID=id,Suspects=r.id).aggregate(Avg('Rank'))['Rank__avg'] or 0
        #print('Average of Logical Rank = ',int(LogicalRank))

        LogicalValue = 60/100*int(LogicalRank)
        #print('60% LogicalValue = ',int(LogicalValue))
        LogicalCount = Evidence_Details.objects.all().filter(Type="Logical",CaseID=id,Suspects=r.id).count()
        #print('LogicalCount = ',LogicalCount)

        PhysicalRank = Evidence_Details.objects.all().filter(Type="Physical",CaseID=id,Suspects=r.id).aggregate(Avg('Rank'))['Rank__avg'] or 0
        #print('Average of Physical Rank = ',int(PhysicalRank))

        PhysicalValue = 80/100*int(PhysicalRank)
        #print('80% PhysicalValue = ',int(PhysicalValue))

        PhysicalCount = Evidence_Details.objects.all().filter(Type="Physical",CaseID=id,Suspects=r.id).count()
        #print('PhysicalCount = ',PhysicalCount)


        EvidenceCount = Evidence_Details.objects.all().filter(CaseID=id,Suspects=r.id).count()
        #print('EvidenceCount = ',EvidenceCount)

        EviCount = 50/100*int(EvidenceCount)
        #print('50% LogicalValue = ',int(EviCount))


        finalscore =  relationPoint + PhysicalValue + LogicalValue + EviCount
        #print('finalscore',finalscore)

        thisdict[r.id] = finalscore

    #print(thisdict)

    sort_orders = dict( sorted(thisdict.items(), key=operator.itemgetter(1),reverse=True))

    #print(type(sort_orders))
    #print(sort_orders)

    Guilty = list(sort_orders.keys())[0]

    Suspect =  Suspects_details.objects.all().filter(id=Guilty)

    #print('System Proved',Suspect[0].Name,"Guilty")

    result = thisdict[list(sort_orders.keys())[0]]
    #print(result)

    Case_details.objects.filter(id=id).update(Status = 'Solved',GuiltyID = Suspect[0].id,GuiltyRelation =Suspect[0].Relation)

    messages.info(request,'Case Solved !System Proved '+str(Suspect[0]. Name)+' guilty and the relations with victim is '+Suspect[0].Relation+' for the Case-ID '+str(id))



    return redirect('/GenerateResults/',{})
        