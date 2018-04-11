"""SRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views,generic

urlpatterns = [
    url(r'^generic$', generic.tim, name = 'generic'),
    url(r'^checkfile$', generic.checkfile, name = 'checkfile'),
    url(r'^uploaddoc_generic$',generic.uploaddoc_generic,name='uploaddoc_generic'), 
    path('admin/', admin.site.urls),
    url(r'^signup$', views.signup, name = 'index'),
    url(r'^verifyotp$', views.index, name = 'index'),
    path('removesave/<int:ID>/', views.removesave),
    url(r'^$', views.index, name='index'),
    url(r'^jobopenings$', views.myview_job, name='jobopening'),
    url(r'^status$', views.myview_status, name='status'),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^savedata$', views.savedata, name = 'savedata'),
    url(r'^uploaddoc', views.uploaddoc, name = 'uploaddoc'),
    url(r'^applicantdetails$', views.applicant_details, name = 'applicant_details'),
    url(r'^profile$', views.profile, name = 'profile'),
    url(r'^meetourteam$', views.meetourteam, name = 'meetourteam'),
    url(r'^mapplicantdetails$', views.mapplicantdetails, name = 'mapplicantdetails'),
    url(r'^adminpage$', views.adminpage, name = 'adminpage'),
    path('recievedapplication', views.recievedapplication),
    url(r'^addjob$', views.add_job, name = 'add_job'),
    url(r'^uploaddata$', views.savedata, name = 'aadhaar'),
    url(r'^changestatus$', views.change_status, name = 'change_status'),
    url(r'^removejob$', views.remove_job, name = 'remove_job'),
    url(r'^viewsavejob$', views.view_save_job, name = 'view_save_job'),
    path('savejobs/<int:ID>/', views.savejobs),
    path('apply/<int:ID>/', views.apply_to_job),
    #path('changestatus', views.change_status),
    path('cancel/<int:PID>/<int:ID>', views.cancel_job),
    path('retrievedoc/<str:id>/<int:doc>', views.retrievedoc),
    path('file/<int:type>', views.showdoc),
    #url(r'^.*$', views.index, name = 'index'),
]