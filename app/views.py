import json
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from .models import user,adminWeb,studentData,voiceRecData
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .function import calcFeedBack, handle_Xlsx_file, handle_rec_file

# Create your views here.
def Register(request):
    try:
        if request.method=='GET':
            n=request.GET['n']
            u=request.GET['u']
            p=request.GET['p']
            a=request.GET['a']
            adminUser=adminWeb.objects.filter(id=a).get()
            new_user=user(name=n,username=u,password=p,aId=adminUser)
            new_user.save()
            return JsonResponse({'msg':'Success'})
        else:
            return JsonResponse({'msg':'Error'})
    except:
        return JsonResponse({'msg':'Parameter Not Valid'})


# api for admin login
def AdminLogin(request):
    try:
        if request.method=='GET':
            n=request.GET['uname']
            obj=adminWeb.objects.filter(username=n).values("username","password","id")
            o1=json.dumps(list(obj)[0],cls=DjangoJSONEncoder)
            data = json.loads(o1)
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"msg":"No Valid"})
    except:
        return JsonResponse({"msg":"Try Again"})

def getUserForAssign(request):
    if request.method=='GET':
        obj=user.objects.values("id","name")
        o1=json.dumps(list(obj),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)

def checkUsername(request):
    if request.method=='GET':
        u=request.GET['u']
        obj=user.objects.filter(username=u).count()
        if obj==0:
            return JsonResponse({"msg":"No"})
        else:
            return JsonResponse({"msg":"Yes"})

@csrf_exempt
def addDetails(request):
    if request.method == 'POST':
        t=handle_Xlsx_file(request.FILES['file'])
        asId=request.POST['asId']
        assignObj=user.objects.filter(id=asId).get()
        l=0
        for i in t:
            print(i)
            obj=studentData.objects.filter(name=i[0] , number=i[1]).count()
            if obj==0:
                stuObj=studentData(name=i[0],number=i[1],assingTo=assignObj)
                stuObj.save()
            else:
                l=l+1
                pass
        if l==len(t):
            return JsonResponse({"msg":"List Already Uploaded"})
        return JsonResponse({"msg":"Success"})
    else:
        return JsonResponse({"msg":"Error"})
    
def fetchStudentData(request):
    if request.method=='GET':
        uId=request.GET['uid']
        userData=user.objects.filter(id=uId).get()
        print(userData)
        data=studentData.objects.filter(assingTo=userData,dateAt__isnull=True).values("id","name","number")
        o1=json.dumps(list(data)[0],cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)
    
def Home(request):
    return HttpResponse("<h1>This domain is used for API's</h1>")

def userLogin(request):
    if request.method=='GET':
        uname=request.GET['unames']
        data=user.objects.filter(username=uname).values("id","name","username","password")
        o1=json.dumps(list(data)[0],cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)
    
def showAllUsersDetails(request):
    if request.method=='GET':
        aid=request.GET['asId']
        data=user.objects.filter(aId=aid).values("name","username","password")
        o1=json.dumps(list(data),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)

@csrf_exempt   
def updateTime(request):
    if request.method=="POST":
        print("Hii")
        stTime=request.POST['CallStart']
        print(stTime)
        enTime=request.POST['CallEnd']
        stId=request.POST['cid']
        usId=request.POST['userID']
        currentDate=datetime.today().strftime('%Y-%m-%d')
        # userData=user.objects.filter(id=usId).get()
        stuData=studentData.objects.filter(id=stId).get()
        stuData.callSt=stTime
        stuData.callEn=enTime
        stuData.dateAt=currentDate
        stuData.save()
        return JsonResponse({"msg":"Updated"})
    print("Here")
    
@csrf_exempt
def recFileUpload(request):
    if request.method=='POST':
        t=handle_rec_file(request.FILES['files'])
        stId=request.POST['cid']
        stuData=studentData.objects.filter(id=stId).get()
        feed=calcFeedBack(t[0])
        vcReco=voiceRecData(voiceId=stuData,path=t[1],text=t[0],feedback=feed)
        vcReco.save()
        return JsonResponse({"msg":"Done"})
    
