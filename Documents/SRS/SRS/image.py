import os
import io
from PIL import Image
from .models import user_details, user, jobs, applied_jobs
from io import StringIO
# import glob, os
# from IPython.core.display import Image
def check_login(username,Password):
    try:
        from .models import user
        from passlib.hash import pbkdf2_sha256
        user=user.objects.get(user_name=username)
        if pbkdf2_sha256.verify(Password,user.password):
            return 1
        else:
                return 0
    except:
        return 0









# [a,p,o,cnt]
def sign_up(username,password,mobile):
    try:
        print("creating user")
        user.objects.create(user_name=username,password=password,mobile_no=mobile)
        return 0
    except:
        return 1

def savejob(request):
    try:
        jobs.objects.create(job_name = request.POST.get('JobName'), job_description = request.POST.get('jobdescription'),date_of_joining = request.POST.get('DOJ'), location = request.POST.get('location'))

        return 1
    except:
        return 0

def savedetails(request,dtype):
    uinstance = user.objects.get(user_name=request.session['username'])
    try:
        udata = user_details.objects.get(user_name_id=request.session['username'])
        if dtype ==1:
            udata.first_name=request.POST.get('FirstName')
            udata.middle_name=request.POST.get('MiddleName')
            udata.last_name=request.POST.get('LastName')
            udata.address=request.POST.get('Address')
            udata.state=request.POST.get('State')
            udata.gender=request.POST.get('Gender')

            udata.experience =request.POST.get('experience')
            udata.skills=request.POST.get('Skills')
            udata.current_company=request.POST.get('company')
            udata.current_salary=request.POST.get('CurrentSalary')
            udata.current_designation=request.POST.get('currentdesignation')
            udata.save()
            upload(request.session['username'],1,request.FILES['profilephoto'])


        elif dtype==2:
            upload(request.session['username'],2,request.FILES['aadhaarcard'])
        elif dtype == 3:
            upload(request.session['username'],3,request.FILES['pancard'])
        elif dtype==4:
            upload(request.session['username'],4,request.FILES['ssccard'])
        else:
            upload(request.session['username'],5,request.FILES['hsccard'])
    except:
        if dtype ==1:
            user_details.objects.create(user_name_id=request.session['username'], first_name=request.POST.get('FirstName'),
                                    middle_name=request.POST.get('MiddleName'), last_name=request.POST.get('LastName'),
                                    address=request.POST.get('Address'),
                                    state=request.POST.get('State'), gender=request.POST.get('Gender'),experience=request.POST.get('experience'),skills=request.POST.get('Skills'),current_company=request.POST.get('company'),current_salary=request.POST.get('CurrentSalary'),
                                        current_designation=request.POST.get('currentdesignation'))
            upload(request.session['username'],1,request.FILES['profilephoto'])

        elif dtype==2:
            upload(request.session['username'],2,request.FILES['aadhaarcard'])
        elif dtype == 3:
            upload(request.session['username'],3,request.FILES['pancard'])
        elif dtype==4:
            upload(request.session['username'],4,request.FILES['ssccard'])
        else:
            upload(request.session['username'],5,request.FILES['hsccard'])


def upload(username, doc, myfile):

                                                                                           
    
    #img = Image.open('6.jpg')
    
    # wpercent = (basewidth/float(img.size[0]))
    # hsize = int((float(img.size[1])*float(wpercent)))
    # img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    # img.save('sompic.jpg')
    # im2 = Image.open(filename +"."+extension).convert("RGB")  
    # im2.save(filename + ".webp","WEBP")
    # im2 = Image.open(filename+".webp")
    # im2.save(filename+".jpg","jpeg")



    if(doc==1):  #1 implies profilepic
        #Image.warnings.simplefilter('error', Image.DecompressionBombWarning)
        basewidth = 600
        Image.MAX_IMAGE_PIXELS = 100000000 
        body = myfile.read()
        myfile.seek(0)
        img = Image.open(myfile)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)

        #img = pil_image.convert('RGB')
        img.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.jpg"),"jpeg")

        im2 = Image.open(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.jpg")).convert("RGB")  
        im2.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.webp"),"WEBP")
        im2 = Image.open(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.webp"))
        im2.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.jpg"),"jpeg")
        os.remove(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_profile.webp"))
    elif(doc==2):  #2 implies aadhaarcard
        body = myfile.read()
        myfile.seek(0)
        pil_image = Image.open(myfile)
        img = pil_image.convert('RGB')
        img.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_aadhaar.jpg"),"jpeg")
    elif(doc==3):  #3 implies pancard
        body = myfile.read()
        myfile.seek(0)
        pil_image = Image.open(myfile)
        img = pil_image.convert('RGB')
        img.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_pancard.jpg"),"jpeg")
    elif(doc==4):  #4 implies ssccard
        body = myfile.read()
        myfile.seek(0)
        pil_image = Image.open(myfile)
        img = pil_image.convert('RGB')
        img.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_ssccard.jpg"),"jpeg")
    elif(doc==5):  #5 implies hsccard
        body = myfile.read()
        myfile.seek(0)
        pil_image = Image.open(myfile)
        img = pil_image.convert('RGB')
        img.save(os.path.join("/home/sharayu/1544/SRS/static/SIHImages/"+username+"_hsccard.jpg"),"jpeg")


