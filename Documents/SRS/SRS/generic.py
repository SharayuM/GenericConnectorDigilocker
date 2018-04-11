import hashlib
import time

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse

from requests import sessions,session

import datetime,time
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
from passlib.hash import pbkdf2_sha256

def encrypt_string(format_iso_now):

    hash_string="SRSvpVGVsKqQeZ3Qm5yDH8T"+format_iso_now
    my_str_as_bytes = str.encode(hash_string)
    sha_signature=hashlib.sha256(my_str_as_bytes).hexdigest()

    return sha_signature
def tim(request):
	import datetime,time
	now = datetime.datetime.now()
	unixtime = time.mktime(now.timetuple())
	c=int(unixtime)
	print("generic")
	import os
	hash = encrypt_string(str(c))
	return render(request, 'generic.html', {"hash":hash,"timestamp":c})

@csrf_exempt
def uploaddoc_generic(request):
	print(str(request.POST['source']))
	if str(request.POST['source'])=="U":
		return HttpResponse(json.dumps({'verified': 'false'}))

	request.session['txn']=request.POST['txn']
	request.session['uri']=request.POST['uri']
	request.session['contentType']=request.POST['contentType']
	print(request.POST['contentType'])
	return HttpResponse(json.dumps({'verified': 'true'}))


def checkfile(request):		
	from dateutil.tz import tzoffset
	from datetime import datetime
	now = datetime.now(tzoffset('EDT', +4 * 60 * 60))
	p = now.isoformat()
	hash_string = "fPxIFCoUJMH3HPBB10Eo" + p
	print("generic222222")
	my_str_as_bytes = str.encode(hash_string)
	sha_signature = hashlib.sha256(my_str_as_bytes).hexdigest()
	msg = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n' \
	      '<PullDocRequest xmlns:ns2="http://tempuri.org/" ver="1.0" ts="' + p + '"' \
	' txn="'+request.session['txn']+'" orgId="com.000webhostapp.testsih" appId="SRS" keyhash="' + sha_signature + '">' \
	'<DocDetails>' \
	'<URI>'+request.session['uri']+'</URI>' \
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
	return HttpResponse((base64.b64decode(document)), content_type=request.session['contentType'])



