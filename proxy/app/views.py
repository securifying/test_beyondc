from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
import jwt
import requests
# Create your views here.
key = 'secret'

HttpResponseRedirect.allowed_schemes.append('beyondc')

service_mappers = {"service1.local":"http://localhost:9001","service2.local":"http://localhost:9002"}

def proxy_router(request):

	proxied_host = request.META.get("HTTP_HOST")
	if proxied_host == "service1.local" or proxied_host == "service2.local":
		header_dict = dict(request.headers.items())
		r = requests.get(service_mappers.get(proxied_host))
		return HttpResponse(r.content)
	# 	if "Authorization" not in header_dict.keys():
	# 		link = "beyondc://service1?uuid=" + uuid.uuid4().__str__()
	# 		return HttpResponseRedirect(link)

	# 	else:
	# 		with open('/tmp/file.token','r') as f:
	# 			payload = f.read()

	# 		try:
	# 			token = jwt.decode(payload,key, algorithm='HS256')
	# 			revoked = bool(token.get('revoked'))
				
	# 			if not revoked:
	# 				return redirect(service_mappers.get(proxied_host))

	# 			else:
	# 				return HttpResponse("You are not authorized!")

	# 		except Exception as e:
	# 			return HttpResponse("You are not authorized!")


	# 	return redirect(service_mappers.get(proxied_host))

	# else:
	# 	return HttpResponse("Service not in proxy list") 


@csrf_exempt
def jwt_acceptor(request):
	if request.method == "POST":
		data = str(request.body)
		with open('/tmp/file.token','w') as f:
			f.write(data)

		return HttpResponse("sent!")
