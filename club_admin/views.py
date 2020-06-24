from django.shortcuts import render,redirect
from django.db import models
from django.db import connection
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
import requests
from password_generator import PasswordGenerator

# Create your views here.
alert = 0
flag=0
alert2=0
flag2=0
global sadmintoken
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
        return redirect(super_admin)
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

#@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admin(request):
    global alert2
    global flag2
    global admintoken
    try:
        id=request.POST["id"]
        pword=request.POST["pword"]
        response = requests.post('http://localhost:5000/adminlog',data={'username':id,'password':pword})
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
    except:
        return render(request,"admin.html")

#@cache_control(no_cache=True,no_store = True)
def super_admin(request):
    global alert
    global flag
    try:
        id2=request.session['suserid']
        return render(request,'super_admin.html')
    except:
        try:
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
        except:
            return render(request,'super_admin.html')



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

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewadmin(request):
    response=requests.get('http://localhost:5000/adminlogin',headers = {'Authorization':f'Bearer {sadmintoken}'})
    data=response.json()
    admin={}
    for i in data:
        admin[i["clubname"]]=i["username"]
    return render(request,"viewadmins.html",{'data':admin})

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addadmins(request):
    global sadmintoken
    id=int(request.POST["id"])
    name=request.POST["name"]
    cname=request.POST["cname"]
    pwo=PasswordGenerator()
    pword=pwo.generate()

    params = dict(uid=id,username=name,password=pword,clubname=cname)
    response=requests.post('http://localhost:5000/addclub',data=params,headers ={'Authorization':f'Bearer {sadmintoken}'})
    print(response)
    return redirect(viewadmin)
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addadmin(request):
    return render(request,'addadmin.html')
def deladmin(request):
    global sadmintoken
    response=requests.get('http://localhost:5000/adminlogin',headers = {'Authorization':f'Bearer {sadmintoken}'})
    data=response.json()
    admin={}
    for i in data:
        admin[i["clubname"]]=i["username"]
    return render(request,'deleteadmin.html',{'data':admin})
def deleteadmin(request):
    admin_name=request.GET.get("admin_name")
    club_name =request.GET.get("club_name")
    global sadmintoken
    response = requests.post('http://localhost:5000/clubmembers',data={'clubname':club_name},headers = {'Authorization':f'Bearer {sadmintoken}'})
    data = response.json()
    for i in range(0,len(data)):
        d=dict()
        d['stuid']=data[i]['stuid']
        d['name']=data[i]['name']
        d['branch']=data[i]['branch']
        d['crole']=data[i]['crole']
        data[i] = d
    print(data)
    return render(request,'confirmdelete.html',{'data':data,'club':club_name,'admin':admin_name})

def confirmdelete(request):
    admin_name =request.GET.get("admin_name")
    global sadmintoken
    response = requests.post('http://localhost:5000/del',data={'username':admin_name},headers = {'Authorization':f'Bearer {sadmintoken}'})
    return redirect(super_admin)
def checkclub(request):
    global sadmintoken
    response=requests.get('http://localhost:5000/adminlogin',headers = {'Authorization':f'Bearer {sadmintoken}'})
    data=response.json()
    admin={}
    for i in data:
        admin[i["clubname"]]=i["username"]
    return render(request,'checkclub.html',{'data':admin})

def checkoutclub(request):
    admin_name=request.GET.get("admin_name")
    club_name =request.GET.get("club_name")
    global sadmintoken
    response = requests.post('http://localhost:5000/clubmembers',data={'clubname':club_name},headers = {'Authorization':f'Bearer {sadmintoken}'})
    data = response.json()
    for i in range(0,len(data)):
        d=dict()
        d['stuid']=data[i]['stuid']
        d['name']=data[i]['name']
        d['branch']=data[i]['branch']
        d['crole']=data[i]['crole']
        data[i] = d
    print(data)
    return render(request,'checkoutclub.html',{'data':data,'club':club_name,'admin':admin_name})
