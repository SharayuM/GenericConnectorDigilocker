from __future__ import unicode_literals
from django.db import models


class user(models.Model):
    user_name = models.CharField(primary_key=True, max_length=25)
    password = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20, null=True)

class doc_data(models.Model):
    user_name=models.ForeignKey(user, on_delete=models.CASCADE)
    uri=models.CharField(max_length=100)
    source=models.CharField(max_length=100)
    txn=models.CharField(max_length=100)
    sharedTill=models.CharField(max_length=100)
    filename=models.CharField(max_length=100)
    contentType=models.CharField(max_length=100)
    docType=models.CharField(max_length=100)
    docId=models.CharField(max_length=100)

class user_details(models.Model):
    user_name = models.ForeignKey(user, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20,null=True)
    middle_name = models.CharField(max_length=20,null=True)
    last_name = models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=20,null=True)
    state = models.CharField(max_length=20,null=True)
    experience=models.IntegerField(null=True)
    current_salary=models.IntegerField(null=True)
    skills=models.CharField(max_length=50,null=True)
    current_company=models.CharField(max_length=20,null=True)
    current_designation=models.CharField(max_length=20,null=True)



class jobs(models.Model):
    job_id = models.AutoField(primary_key=True, max_length=10)
    job_name = models.CharField(max_length=20,null=True)
    job_description = models.CharField(max_length=20,null=True)
    date_of_joining = models.DateField(max_length=20,null=True)
    location = models.CharField(max_length=20,null=True)
    flag = models.IntegerField(default = '1')


class applied_jobs(models.Model):
    job_id=models.ForeignKey(jobs,on_delete=models.CASCADE,related_name='app_job')
    user_name = models.ForeignKey(user, on_delete=models.CASCADE, related_name='app_user')
    dof_app=models.DateField(max_length=20,null=True)
    status=models.IntegerField(default='1')

class saved_jobs(models.Model):
    job_id = models.ForeignKey(jobs,on_delete=models.CASCADE,related_name='id_job')
    user_name = models.ForeignKey(user, on_delete=models.CASCADE, related_name='username')