from django.shortcuts import render,redirect
from django.db import models
from django.db import connection
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
def admin(request):
    id=request.POST["name"]
    pword=request.POST["pword"]
    request.session['userid'] = id
    request.session['password'] = pword
    return render(request,'admin.html')
def super_admin(request):
    id=request.POST["name"]
    pword=request.POST["pword"]
    if (id in "100") &( pword in "cbit"): #static userid,password
        return render(request,"super_admin.html")
    else:
        return render(request,"index.html")
