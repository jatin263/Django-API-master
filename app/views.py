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
        adId=request.GET['adId']
        adData=adminWeb.objects.filter(id=adId).get()
        obj=user.objects.filter(aId=adData).values("id","name")
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
@csrf_exempt
def stuFeedBack(request):
    if request.method=='POST':
        stId=request.POST['cid']
        intt=request.POST['interest']
        detailss=request.POST['details']
        stuDataa=studentData.objects.filter(id=stId).get()
        stuDataa.stFeedBack=intt
        stuDataa.stDetails=detailss
        stuDataa.save() 
        return HttpResponse('Sccuess')
    
def getUserCall(request):
    if request.method=='GET':
        userID=request.GET['userid']
        userObj=user.objects.filter(id=userID).get()
        userStu=studentData.objects.filter(assingTo=userObj,dateAt__isnull=False).values("id","name","number","stFeedBack")
        userStu=list(userStu)
        for i in range(len(userStu)):
            stuDataa=studentData.objects.filter(id=userStu[i]["id"]).get()
            print(stuDataa.name)
            try:
                voicData=voiceRecData.objects.filter(voiceId=stuDataa).get()
                userStu[i]["l"]="https://4be6-118-185-190-60.ngrok-free.app/"+voicData.path
                userStu[i].pop("id")
                startt=stuDataa.callSt
                endd=stuDataa.callEn
                a=str(startt).split(":")
                b=str(endd).split(":")
                t1=int(a[2])+60*int(a[1])+3600*int(a[0])
                t2=int(b[2])+60*int(b[1])+3600*int(b[0])
                p=t2-t1
                s=p%60
                m=(p-s)//60%60
                h=(p-s)//3600
                userStu[i]['du']=str("%0.2d" % h)+":"+str("%0.2d" % m)+":"+str("%0.2d" % s)
            except:
                pass
        o1=json.dumps(list(userStu),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)

def summaryData(request):
    if request.method=='GET':
        adminId=request.GET['aid']
        us=user.objects.filter(aId=adminId).values("id","name")
        us=list(us)
        for i in range(len(us)):
            TotalData=studentData.objects.filter(assingTo=us[i]["id"]).count()
            us[i]["total"]=TotalData
            NoDone=studentData.objects.filter(dateAt__isnull=True,assingTo=us[i]["id"]).count()
            us[i]['comp']=TotalData-NoDone
        o1=json.dumps(list(us),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)
    
def summaryData1(request):
    if request.method=='GET':
        adminId=request.GET['aid']
        us=user.objects.filter(aId=adminId).values("id","name")
        us=list(us)
        for i in range(len(us)):
            notCall=0
            TotalFeedBack=0
            TotalData=studentData.objects.filter(assingTo=us[i]["id"])
            TotalData=list(TotalData)
            for j in TotalData:
                if str(j.dateAt) == "None":
                    notCall=notCall+1
                else:
                    voiceData=voiceRecData.objects.filter(voiceId=j.id)
                    for k in voiceData:
                        TotalFeedBack=TotalFeedBack+int(k.feedback)
            us[i]['total']=len(TotalData)
            us[i]['comp']=len(TotalData)-notCall
            try:
                us[i]['accuracy']=str(int(TotalFeedBack/(len(TotalData)-notCall)))+"%"
            except:
                us[i]['accuracy']="0%"
        o1=json.dumps(list(us),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)

def topThreeUser(request):
    if request.method=='GET':
        ans=[]
        adIdd=request.GET['adId']
        adData=adminWeb.objects.filter(id=adIdd).get()
        userData=list(user.objects.filter(aId=adData).values("id","name"))
        print(userData)
        tempList=[]
        for i in userData:
            t=[]
            t.append(i['name'])
            d=i['id']
            userDataTemp=user.objects.filter(id=d).get()
            stuData=studentData.objects.filter(assingTo=userDataTemp).count()
            t.append(stuData)
            tempList.append(t)
        for i in range(len(tempList)):
            for j in range(len(tempList)):
                if tempList[i][1]>tempList[j][1]:
                    temp=tempList[i][1]
                    tempList[i][1]=tempList[j][1]
                    tempList[j][1]=temp
        tempList=tempList[:3]
        for i in tempList:
            ans.append(i[0])
        o1=json.dumps(list(ans),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)
            
def userActivity(request):
    if request.method=='GET':
        adIdd=request.GET['adId']
        adData=adminWeb.objects.filter(id=adIdd).get()
        userData=user.objects.filter(aId=adData)
        for i in userData:
            userData=user.objects.filter(id=i)

def homeFeedBack(request):
    if request.method=='GET':
        adIdd=request.GET['adId']
        interest=0
        notInterest=0
        adData=adminWeb.objects.filter(id=adIdd).get()
        userData=user.objects.filter(aId=adData)
        for i in userData:
            userDataa=user.objects.filter(id=i.id).get()
            totalData=stuData=studentData.objects.filter(assingTo=userDataa).count()
            stuDatat=studentData.objects.filter(assingTo=userDataa,stFeedBack="Interested").count()
            notCall=studentData.objects.filter(assingTo=userDataa,stFeedBack="Not Interested").count()
            interest=interest+stuDatat
            notInterest=notInterest+notCall
        ans=[interest,notInterest]
        o1=json.dumps(list(ans),cls=DjangoJSONEncoder)
        data=json.loads(o1)
        return JsonResponse(data,safe=False)


def totalCalls(request):
    if request.method=='GET':
        adIdd=request.GET['adId']
        adData=adminWeb.objects.filter(id=adIdd).get()
        userData=user.objects.filter(aId=adData)
        totalCallsDone=0
        totalAssign=0
        for i in userData:
            assignCall=studentData.objects.filter(assingTo=i).count()
            callDone=studentData.objects.filter(assingTo=i,dateAt__isnull=False).count()
            totalAssign=totalAssign+assignCall
            totalCallsDone=totalCallsDone+callDone
        ans=[{"Calls_Done"}]

        
