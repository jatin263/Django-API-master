from django.db import models


class adminWeb(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,default="")
    username=models.CharField(max_length=20,default="")
    password=models.CharField(max_length=20,default="")

    class Meta:
        db_table=""
        managed=True
        verbose_name='Admin'
        verbose_name_plural='Admins'



class user(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    username=models.CharField(max_length=10,default="",unique=True)
    password=models.CharField(max_length=10,default="")
    aId=models.ForeignKey('app.adminWeb',on_delete=models.CASCADE)

    class Meta:
        db_table=""
        managed=True
        verbose_name='User'
        verbose_name_plural='Users'

class studentData(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    number=models.CharField(max_length=50,default="")
    assingTo=models.ForeignKey("app.user",on_delete=models.CASCADE)
    dateAt=models.DateField(null=True, auto_now=False, auto_now_add=False,blank=True)
    callSt=models.TimeField(null=True,auto_now=False,auto_now_add=False,blank=True)
    callEn=models.TimeField(null=True,auto_now=False,auto_now_add=False,blank=True)

    class Meta:
        db_table=""
        managed=True
        verbose_name='StudentData'
        verbose_name_plural='StudentDatas'

class voiceRecData(models.Model):
    id=models.AutoField(primary_key=True)
    voiceId=models.ForeignKey("app.studentData",on_delete=models.CASCADE)
    path=models.TextField(max_length=200,default="")
    text=models.TextField(max_length=3000,default="")
    feedback=models.IntegerField(default="")

    class Meta:
        db_table=""
        managed=True
        verbose_name='Voice Data'
        verbose_name_plural="Voices Data"

