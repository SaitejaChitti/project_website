from django.shortcuts import render,redirect
from django.db import models
from django.db import connection
from django.views.decorators.cache import cache_control
from django.http.response import HttpResponse
import requests

# Create your views here.
def delete_session(request):
    try:
        del request.session['userid']
        del request.session['password']
        return redirect(index)
    except:
        return redirect(index)
def index(request):
    return render(request,"index.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin(request):
    id=request.POST["name"]
    pword=request.POST["pword"]
    response=requests.post('http://localhost:5000/login',{'username':id,'password':pword})
    user=response.json()
    for k,v in user.items():
        if k in 'message':
            return redirect(index)
        if k  in 'access_token' :
            request.session['userid'] = id
            request.session['password'] = pword
            return render(request,'admin.html',{'user':v})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def super_admin(request):
    if request.method == "POST":
        id=request.POST["name"]
        pword=request.POST["pword"]
        if (id in "100") &( pword in "cbit"): #static userid,password
            request.session['superuserid'] = id
            return render(request,"super_admin.html")
        else:
            return redirect(index)
    else:
        return render(request,"super_admin.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewadmin(request):
    response=requests.get('http://localhost:5000/adminlogin')
    data=response.json()
    admin={}
    if "message" in data:
        print(data)
        return redirect(super_admin)
    else:
        for i in data:
            admin[i['clubname']]=i['username']
        return render(request,"viewadmins.html",{'data':admin})
