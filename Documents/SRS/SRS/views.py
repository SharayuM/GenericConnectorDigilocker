from .shaencrypt import encrypt_string
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
#from .image import upload,replace
from .image import sign_up,check_login,savedetails,savejob
from requests import sessions,session
from .models import user_details, user, jobs, applied_jobs,doc_data, saved_jobs
import datetime,time
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
from passlib.hash import pbkdf2_sha256

def index(request):
    if request.method == 'POST' and 'verify_otp_btn' in request.POST:
        username =request.session['Email']
        password =request.session['Password']
        enc_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
        mobile_no =request.session['Mobile']
        if user.objects.filter(mobile_no = mobile_no).exists():
            return render(request, 'index.html', {"mobile_same" : 1})
        else:
            if str(request.POST['verify_otp'])==str(request.session['otp']):
                t = sign_up(username,enc_password,mobile_no)
                del request.session['Email']
                del request.session['Password']
                del request.session['Mobile']
                del request.session['otp']
            else :
                return render(request,'index.html',{"invalidotp" :1 })
            if t == 1:
                del request.session['Email']
                del request.session['Password']
                del request.session['Mobile']
                del request.session['otp']
                return render(request,'index.html',{"invalid" :1 })
            else :

                return render(request,'index.html',{"success" :1 })

    if request.session.has_key('username'):
        return render(
        request,
        'index.html',{"username" : request.session['username']})

    return render(
        request,
        'index.html')


    #myForm = CustomForm(request.POST)
    '''action=1
    if(action==1):
        upload("Amruta", 3,"/home/super--user/cap.png")
    else:
        replace("Amruta", 2,"/home/super--user/test.png")'''


def myview_job(request):
    try:
        available=jobs.objects.all();
    except:
        return render(
            request,
            'jobopenings.html')
    try:
        if request.session.has_key("username"):
            if request.session['username'] == "test.datastream@gmail.com":
                return HttpResponseRedirect("/adminpage")
            else:
                applied=applied_jobs.objects.filter(user_name_id=user.objects.get(user_name=request.session['username']))
                saved = saved_jobs.objects.filter(user_name_id = request.session['username'])
                avails=[]
                appls=[]
                save = []
                unsave = []
                for job in available:
                    flag=0
                    for ap in applied:
                        if ap.job_id_id==job.job_id:
                            flag=1
                            appls.append(job)
                            break

                    if flag == 0:
                            #print(job)
                        avails.append(job)
                for av in avails:
                    flag = 0
                    for s in saved:
                        if s.job_id_id == av.job_id:
                            flag = 1
                            save.append(av)
                            break
                    if flag == 0:
                        unsave.append(av)
                    #print(avails)
                '''if request.session.has_key('jobsave'):
                    del request.session['jobsave']
                    return render(request,'jobopenings.html',{"avails":avails,"appls":appls,"username" : request.session['username'],"save" : 0})
                else:
                    return render(request,'jobopenings.html',{"avails":avails,"appls":appls,"username" : request.session['username'],"save":1})'''
                #else:
                return render(request,'jobopenings.html',{"avails":avails,"appls":appls,"username" : request.session['username'], "save" : save, "unsave" : unsave})
        return render(
        request,
        'jobopenings.html',{"available":available})
    except:
        return render(
            request,
            'jobopenings.html')


def applicant_details(request):
    aadhaar=0
    pancard=0
    ssccard=0
    hsccard=0
    if request.session.has_key('username'):
        if request.session['username'] == "test.datastream@gmail.com":
            return HttpResponseRedirect("/adminpage")
        else:
            try:
                import datetime,time
                now = datetime.datetime.now()
                unixtime = time.mktime(now.timetuple())
                c=int(unixtime)
                import os
                hash = encrypt_string(str(c))
                if os.path.exists(os.path.join(
                        "/home/sharayu/1544/SRS/static/SIHImages/" + request.session['username'] + "_aadhaar.jpg")):
                    aadhaar=1
                elif doc_data.objects.filter(user_name_id= request.session['username'] , docType="Aadhaar Card").exists():
                    aadhaar = 2

                if os.path.exists(os.path.join(
                        "/home/sharayu/1544/SRS/static/SIHImages/" + request.session['username'] + "_pancard.jpg")):
                    pancard=1
                elif doc_data.objects.filter(user_name_id=request.session['username'], docType="PAN Verification Record").exists():
                    pancard=2

                if os.path.exists(os.path.join(
                        "/home/sharayu/1544/SRS/static/SIHImages/" + request.session['username'] + "_ssccard.jpg")):
                    ssccard=1
                elif doc_data.objects.filter(user_name_id=request.session['username'], docType="SSC Marksheet - X").exists():
                    ssccard = 2

                if os.path.exists(os.path.join(
                        "/home/sharayu/1544/SRS/static/SIHImages/" + request.session['username'] + "_hsccard.jpg")):
                    hsccard = 1
                elif doc_data.objects.filter(user_name_id=request.session['username'], docType="HSC Marksheet - XII").exists():
                    hsccard = 2
                    

                udata = user_details.objects.get(user_name_id=request.session['username'])
                if request.session.has_key('filldetails'):
                    del request.session['filldetails']
                    return render(request, 'ApplicantDetails.html', {"aadhaar":aadhaar,"pancard":pancard,"ssccard":ssccard,"hsccard":hsccard,"uname":request.session['username'],"hash":hash,"timestamp":c, "data":udata, "filldetails" : 1})
                else:
                    return render(request, 'ApplicantDetails.html', {"aadhaar":aadhaar,"pancard":pancard,"ssccard":ssccard,"hsccard":hsccard,"uname":request.session['username'],"data":udata,"hash":hash,"timestamp":c})
            except:
                print("except")
                if request.session.has_key('filldetails'):
                    del request.session['filldetails']
                    return render(request, 'ApplicantDetails.html', {"aadhaar":aadhaar,"pancard":pancard,"ssccard":ssccard,"hsccard":hsccard,"uname":request.session['username'],"hash":hash,"timestamp":c, "filldetails" : 1})
                else:
                    return render(request,'ApplicantDetails.html',{"aadhaar":aadhaar,"pancard":pancard,"ssccard":ssccard,"hsccard":hsccard,"uname":request.session['username'],"hash":hash,"timestamp":c})
    return render(request,'index.html',{"loginfirst" :1 })



def logout(request):
   try:

       for key in request.session.keys():
           del request.session[key]
   except:
      pass
   return render(
       request,
       'index.html',
   )



def login(request):
    username = request.POST.get("Email")
    password = request.POST.get("Password")
    t=check_login(username,password)
    try:
        for key in request.session.keys():
            del request.session[key]
    except:
      pass

    if t==1:
        request.session['username']=username
    else:
        return render(
        request,
        'index.html',{"loginfailed":1}
    )
    return HttpResponseRedirect("index")

def myview_status(request):
    if request.session.has_key('username'):
        if request.session['username'] == "test.datastream@gmail.com":
            return HttpResponseRedirect("/adminpage")
        else:
            try:
                all_jobs = jobs.objects.all();
                applied = applied_jobs.objects.filter(user_name=request.session['username'])
                return render(
                        request,
                        'status.html',{"username":request.session['username'],"applied" : applied, "all_jobs" : all_jobs})
            except:
                return render(request,'status.html',{"username":request.session['username'], "applied" : applied})
    else:
        return render(request, 'index.html', {"loginfirst": 1})

def profile(request):
    if request.session.has_key('username'):
        if request.session['username'] == "test.datastream@gmail.com":
            return HttpResponseRedirect("/adminpage")
        else:
            try:
                udata = user_details.objects.get(user_name_id=request.session['username'])
                return render(request, 'Profile.html', {"uname":request.session['username'],"user":udata})
            except:
                return render(request, 'Profile.html', {"uname":request.session['username'], "error" : 1})
    else:
        return render(request, 'index.html', {"loginfirst": 1})

@csrf_exempt
def signup(request):
    if 'Email' in  request.POST and 'Password' in request.POST and 'Mobile' in request.POST:
        if user.objects.filter(mobile_no = request.POST['Mobile']).exists():
            return render(request, 'index.html', {"mobile_same" : 1})
        request.session['Email']=request.POST['Email']
        request.session['Password']=request.POST['Password']
        request.session['Mobile']=request.POST['Mobile']
        from random import randint
        request.session['otp']=randint(1000,9999)

        from . import waytosms
        q=waytosms.sms('7020073329','Q2563H')
        q.send(request.POST['Mobile'], 'your otp is '+str(request.session['otp']) )
        q.logout()
        print(request.session['otp'])
        return HttpResponse(json.dumps({'key': 'value'}))

def showdoc(request,type):
    if request.session.has_key('username'):
        request.session['allowed']=1
        return retrievedoc(request,str(request.session['username']),type)
    else:
        return render(request, 'index.html', {"loginfirst": 1})

def savedata(request):
    if request.session.has_key('username'):
        if request.session['username'] == "test.datastream@gmail.com":
            return HttpResponseRedirect("/adminpage")
        else:
            if 'SubmitDetails' in request.POST:
                savedetails(request,1)
            elif 'submitaadhaar' in request.POST:
                savedetails(request,2)
            elif 'submitpan' in request.POST:
                savedetails(request,3)
            elif 'submitssc' in request.POST:
                savedetails(request,4)
            elif 'submithsc' in request.POST:
                savedetails(request,5)
            print("hello")
            return render(request,'ApplicantDetails.html',{"uname":request.session['username'],"saved":"saved","data":user_details.objects.get(user_name_id=request.session['username'])})
    else:
        return render(request, 'index.html', {"loginfirst": 1})

def apply_to_job(request,ID=0):

    try:

        user_exists = user_details.objects.get(user_name_id = request.session['username'])
        uid = request.session['username']
        import os
            #with open(os.path.join("/home/jobs/SRSSIH/SRS/static/SIHImages/",id+"_"+dtype), 'rb') as f:
             #   my_file = f.read()
        if os.path.exists(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+uid+"_aadhaar.jpg")):
            pass
        elif doc_data.objects.get(user_name_id = uid, docType = "Aadhaar Card"):
            pass
        else:
            request.session['filldetails'] = 1
            return applicant_details(request)

        if os.path.exists(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+uid+"_pancard.jpg")):
            pass
        elif doc_data.objects.get(user_name_id = uid, docType = "PAN Verification Record"):
            pass
        else:
            request.session['filldetails'] = 1
            return applicant_details(request)

        if os.path.exists(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+uid+"_ssccard.jpg")):
            pass
        elif doc_data.objects.get(user_name_id = uid, docType = "SSC Marksheet - X"):
            pass
        else:
            request.session['filldetails'] = 1
            return applicant_details(request)

        if os.path.exists(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+uid+"_hsccard.jpg")):
            pass
        elif doc_data.objects.filter(user_name_id = uid, docType = "HSC Marksheet - XII"):
            pass
        else:
            request.session['filldetails'] = 1
            return applicant_details(request)

        print("11")
        if ID == 0:
            return HttpResponseRedirect("/")
        elif request.session.has_key('username'):
            if request.session['username'] == "test.datastream@gmail.com":
                return HttpResponseRedirect("/adminpage")
            else:
                try:

                    if applied_jobs.objects.filter(job_id_id = ID, user_name_id = request.session['username']).exists():
                        return HttpResponseRedirect("/jobopenings")
                    else:

                        print("22")
                        applied_jobs.objects.create(dof_app=datetime.datetime.today(),status=1,job_id_id=ID,user_name_id=request.session['username'])
                        print("33")
                        jobapplied=jobs.objects.get(job_id=ID)
                        print("41")
                        from . import waytosms
                        try:
                            message="Congrats.Successfully applied to the post of "+str(jobapplied.job_name);
                            q = waytosms.sms('7020073329', 'Q2563H')
                            q.send(str(user.objects.get(user_name=request.session['username']).mobile_no), message)
                            q.logout()
                        except:
                            pass
                        print("51")
                        if saved_jobs.objects.filter(job_id_id=ID, user_name_id=request.session['username']).exists():
                            saved_jobs.objects.filter(job_id_id=ID, user_name_id=request.session['username']).delete()
                        print("61")
                        try:
                            subject="Job Application"
                            from_email=settings.EMAIL_HOST_USER
                            signup_message="""you have applied for """+jobs.objects.get(job_id=ID).job_name+""" wait for further notice from us.Thank you."""
                            to_email=[request.session['username']]
                            send_mail(subject=subject,from_email=from_email,recipient_list=to_email,message=signup_message,fail_silently=False)
                        except:
                            pass
                        return HttpResponseRedirect("/jobopenings")
                except:
                    print("71")
                    return render(request, 'index.html', {"loginfirst": 1})
        else:
            print("81")
            return render(request, 'index.html', {"loginfirst": 1})
    except:
       # return render(request, 'jobopenings.html', {"exists" : 1})
       request.session['filldetails'] = 1
       return applicant_details(request)



@csrf_exempt
def uploaddoc(request):
    if request.session.has_key('username'):
        if request.is_ajax():
            try:
                if str(request.POST.get('source'))=='U':
                    print("unverified")
                    return HttpResponse(json.dumps({'verified': 'false'}))

                print("verified")
                udata=doc_data.objects.get(user_name_id=request.session['username'],docType=request.POST.get('docType'))
                udata.delete()
            except:
                pass

            print("11")
            udata=doc_data.objects.create(user_name_id=request.session['username'],uri=request.POST.get('uri'),source=request.POST.get('source'),
                txn=request.POST.get('txn'),
                sharedTill=request.POST.get('sharedTill'),
                filename=request.POST.get('filename'),
                contentType=request.POST.get('contentType'),
                docType=request.POST.get('docType'),
                docId=request.POST.get('docId'))

        print("returning")
        return HttpResponse(json.dumps({'verified': 'true'}))

def adminpage(request):
    alljobs = jobs.objects.all()
    return render(request, 'Admin.html',{"alljobs" : alljobs})

def meetourteam(request):
    if request.session.has_key('username'):
        return render(request, 'MeetOurTeam.html',{"username":request.session['username']})
    else:
        return render(request, 'MeetOurTeam.html')


def mapplicantdetails(request):
    return render(request, 'ApplicationDetailsMobile.html')

def add_job(request):
    if request.session['username'] == "test.datastream@gmail.com":
        t = savejob(request)
        #jobs.objects.create(job_name = request.POST.get('JobName'), job_description = request.POST.get('jobdescription'),date_of_joining = request.POST.get('DOJ'), location = request.POST.get('location'))
        #return HttpResponse(json.dumps({'key': 'value'}))
        if t == 1:
            return render(request, 'Admin.html', {"check" : 1})
        else:
             return HttpResponseRedirect('/adminpage')
    else:
        return HttpResponseRedirect('/')


def cancel_job(request, PID=0, ID=0):
    try:
        applied_jobs.objects.filter(job_id_id = ID, user_name_id = request.session['username']).delete()
        try:
            subject="Job Cancellation"
            from_email=settings.EMAIL_HOST_USER
            signup_message="""you have sucessfully cancelled Job  """+jobs.objects.get(job_id=ID).job_name+""".Thank you."""
            to_email=[request.session['username']]
            send_mail(subject=subject,from_email=from_email,recipient_list=to_email,message=signup_message,fail_silently=False)
            message="Successfully cancelled application to the post of "+str(jobs.objects.get(job_id=ID).job_name);
            q = waytosms.sms('7020073329', 'Q2563H')
            q.send(str(user.objects.get(user_name=request.session['username']).mobile_no), message)
            q.logout()
        except:
            pass
        if PID == 1:
            return HttpResponseRedirect("/jobopenings")
        else:
            return HttpResponseRedirect("/status")
    except:
        return render(request, 'jobopenings.html', {"error" : 1})

def removesave(request,ID=0):
    try:
        saved_jobs.objects.filter(job_id_id=ID,user_name_id = request.session['username']).delete()
        return HttpResponseRedirect("/viewsavejob")
    except:
        return render(request, 'savejobs.html', {"error" : 1})






def recievedapplication(request):
    jid = request.POST.get('jobid')
    application = applied_jobs.objects.filter(job_id_id = jid)
    job = jobs.objects.get(job_id = jid)
    return render(request, 'RecievedApplication.html', {"application" : application, "job" : job})

def change_status(request):
    username = request.POST.get('username')
    jid = request.POST.get('id')
    application=applied_jobs.objects.filter(job_id_id=jid)
    value = request.POST.get('PreviousReceiver')
    try:
        job=jobs.objects.get(job_id=jid)
        obj = applied_jobs.objects.get(job_id_id = jid, user_name_id = username)
        if value == "Under Review":
            obj.status = 2
        elif value == "Shortlisted":
            obj.status = 3
        elif value == "Rejected":
            obj.status = 0
        else:
            obj.status = 1
        obj.save()

        return render(request, 'RecievedApplication.html', {"application" : application, "job" : job})
    except:
        return render(request, 'RecievedApplication.html', {"error" : 1,"application" : application, "job" : job})

def remove_job(request):
    jid = request.POST.get('jobid')
    try:
        job = jobs.objects.get(job_id = jid)
        job.flag = 0
        job.save()
        alljobs = jobs.objects.all()
        return render(request, 'Admin.html',{"alljobs" : alljobs})
    except:
        return render(request, 'Admin.html',{"alljobs" : alljobs, "error" : 1})


def savejobs(request,ID=0):
    if request.session.has_key('username'):
        try:
            saved_jobs.objects.get(job_id_id=ID,user_name_id=request.session['username'])
            #request.session['jobsave'] = 1
            return myview_job(request)
        except:
            saved_jobs.objects.create(job_id_id=ID,user_name_id=request.session['username'])
            return myview_job(request)
    else:
        return render(request, 'index.html', {"loginfirst": 1})

def view_save_job(request):
    if request.session.has_key('username'):
        if saved_jobs.objects.filter(user_name_id=request.session['username']).count():
            job = saved_jobs.objects.filter(user_name_id=request.session['username'])
            all_jobs = jobs.objects.all()
            return render(request, 'savejobs.html',
                          {"job": job, "all_jobs": all_jobs, "username": request.session['username']})
        else:
            return render(request, 'savejobs.html', {"nojob": 1, "username": request.session['username']})
    else:
        return render(request, 'index.html', {"loginfirst": 1})
    '''if request.session.has_key('username'):
        try:
            job = saved_jobs.objects.filter(user_name_id=request.session['username'])
            all_jobs = jobs.objects.all()
            return render(request, 'savejobs.html', {"job": job, "all_jobs" : all_jobs,"username":request.session['username']})
        except:
            return render(request, 'savejobs.html', {"error" : 1,"username":request.session['username']})
    else:
        return render(request, 'index.html', {"loginfirst": 1})'''

def retrievedoc(request,id,doc):
    if request.session.has_key('username'):
        if  request.session['username'] == "test.datastream@gmail.com" or request.session.has_key('allowed'):
            if  request.session.has_key('allowed'):
                del request.session['allowed']
            import hashlib
            if doc == 1:
                dtype="aadhaar.jpg"
            elif doc == 2:
                dtype = "pancard.jpg"
            elif doc ==3 :
                dtype= "ssccard.jpg"
            elif doc ==4 :
                dtype= "hsccard.jpg"


            try:
                import os

                with open(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+id+"_"+dtype), 'rb') as f:
                    my_file = f.read()
                #if my_file.is_file():
                return HttpResponse(my_file, content_type="image/jpeg")
            except FileNotFoundError:
                from datetime import datetime
                if doc == 1:
                    datatype=doc_data.objects.get(user_name_id=id,docType="Aadhaar Card")
                elif doc == 2:
                    datatype=doc_data.objects.get(user_name_id=id,docType="PAN Verification Record")
                elif doc ==3 :
                    datatype=doc_data.objects.get(user_name_id=id,docType="SSC Marksheet - X")
                elif doc ==4 :
                    datatype=doc_data.objects.get(user_name_id=id,docType="HSC Marksheet - XII")
                from dateutil.tz import tzoffset
                from datetime import datetime
                now = datetime.now(tzoffset('EDT', +4 * 60 * 60))
                p = now.isoformat()
                hash_string = "fPxIFCoUJMH3HPBB10Eo" + p
                my_str_as_bytes = str.encode(hash_string)
                sha_signature = hashlib.sha256(my_str_as_bytes).hexdigest()
                msg = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n' \
                      '<PullDocRequest xmlns:ns2="http://tempuri.org/" ver="1.0" ts="' + p + '"' \
                ' txn="'+datatype.txn+'" orgId="com.000webhostapp.testsih" appId="SRS" keyhash="' + sha_signature + '">' \
                '<DocDetails>' \
                '<URI>'+datatype.uri+'</URI>' \
                ' </DocDetails>' \
                '</PullDocRequest>'

                url="https://devpartners.digitallocker.gov.in/public/requestor/api/pulldoc/1/xml"
                import requests
                import xml.etree.ElementTree
                headers = {'Name':'Content-Type', 'value': 'application/xml', 'Content-Type': 'application/xml'}
                file = requests.post(url,msg,headers=headers).text

                xdoc=xml.etree.ElementTree.fromstring(file)
                document = xdoc.find('DocDetails').find('docContent').text
                import base64

                return HttpResponse((base64.b64decode(document)), content_type=datatype.contentType)

    return HttpResponseRedirect('/')