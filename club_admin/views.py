from django.shortcuts import render,redirect
from django.db import models
from django.db import connection
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
import requests
# Create your views here.
alert = 0
flag=0
alert2=0
flag2=0

#@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delete_session(request):
    
    d = request.GET.get("logout")
    if(d == 'slogout'):

        try:
            
            del request.session['suserid']
            del request.session['spassword']
            logout(request)
            return redirect(index)
        except:
            logout(request)
            return redirect(index)
    else:
        try:
            
            del request.session['userid']
            del request.session['password']
            logout(request)
            return redirect(adminlog)
        except:
            logout(request)
            return redirect(adminlog)
#@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def index(request):
    global alert
    global flag
    try:
        a=request.session['suserid']
        b=request.session['spassword']
        return render(request,'super_admin.html')
    except:
        response=requests.get('http://localhost:5000/clubnames')
        club_names=response.json()
        clubs=[]
        for i in club_names:
            clubs.append(i['clubname'].capitalize()+"_Club")
        if(flag==1):
            alert = 1
            flag = 0
        else:
            alert = 0
        return render(request,'index2.html',{'club':clubs,'alert':alert})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admin(request):
    global alert2
    global flag2
    id=request.POST["id"]
    pword=request.POST["pword"]
    
    global admintoken
    response = requests.post('http://localhost:5000/adminlog',data={'username':id,'password':pword})
    print(response)
    result = response.json()
    print(result)
    try:
        admintoken=result['access_token']
        
        request.session['userid'] =id
        request.session['password']=pword
        alert2 = 0
        return render(request,"admin.html")
    except:
        alert2 = 1
        flag2 = 1
        return redirect(adminlog)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def super_admin(request):
    global alert
    global flag
    id=request.POST["sid"]
    pword=request.POST["spword"]
    global sadmintoken
    response = requests.post('http://localhost:5000/login',data={'username':id,'password':pword})
    result = response.json()
    try:
        sadmintoken=result['access_token']
        
        request.session['suserid'] =id
        request.session['spassword']=pword
        alert = 0
        return render(request,"super_admin.html")
    except:
        alert = 1
        flag = 1
        return redirect(index)



def adminlog(request):
    
    global alert2
    global flag2
    try:
        a=request.session['userid']
        b=request.session['password']
        return render(request,'admin.html')
    except:

        if(flag2==1):
            alert2 = 1
            flag2 = 0
        else:
            alert2 = 0
        return render(request,'admin2.html',{'alert':alert2})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewadmin(request):
    global admintoken
    response=requests.get('http://localhost:5000/addclub',headers = {'Authorization':f'Bearer {admintoken}'})
    data=response.json()
    admin={}
    for i in data:
        admin[i["clubname"]]=i["username"]
    return render(request,"viewadmins.html",{'data':admin})
    
   