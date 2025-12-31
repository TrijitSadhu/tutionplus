

from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView,RedirectView
from .models import current_affairs_slide
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse,reverse_lazy, resolve
from django.shortcuts import redirect,render_to_response

from django.template import RequestContext
import urllib
from .models import current_affairs_slide
from .models import total
from .models import total_english
from .models import total_math
from .models import total_english
from .models import math
from .models import user_save
from .models import total_reasoning
from .models import total_close
from .models import close
from .models import topic
from .models import reasoning
import datetime
from .models import total_error
from .models import error
from .models import current_affairs
from .models import the_hindu_word_list1
from .models import the_economy_word_list1
from .models import the_hindu_word_list2
from .models import the_economy_word_list2
from .models import the_economy_word_Header2
from .models import the_economy_word_Header1
from .models import the_hindu_word_Header1
from .models import the_hindu_word_Header2
from .models import total_job
from .models import total_job_state
from .models import total_job_category
from .models import total_mcq
from .models import home
from .models import mcq
from .models import mcq_info_2018
from .models import mcq_info_2019
from .models import current_affairs_info_2018
from .models import current_affairs_info_2019
from .models import total_history
from .models import history
from .models import total_polity
from .models import polity
from .models import total_geography
from .models import geography
from .models import total_economics
from .models import economics
from .models import total_physics
from .models import physics
from .models import total_chemistry
from .models import chemistry
from .models import total_biology
from .models import biology

import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

from .forms import UserForm
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.db import models

from django.contrib.auth.models import User
from .forms import Login
import sys
import os
from django.urls import reverse
import datetime as dt     
import time 
from datetime import timedelta
from datetime import date
from .models import job

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.

def index(request):
    userform = UserForm(request.POST or None)
    login = Login(request.POST or None)
    hindu=0
    e=0
    header1=None
    header2=None
    header_e1=None
    header_e2=None
    word1_obj=home.objects.values('word1_day')[0]
    word1_day=(word1_obj['word1_day'])
    
    word2_obj=home.objects.values('word2_day')[0]
    word2_day=(word2_obj['word2_day'])

    word_e1_obj=home.objects.values('word_e1_day')[0]
    word_e1_day=(word_e1_obj['word_e1_day'])

    word_e2_obj=home.objects.values('word_e2_day')[0]
    word_e2_day=(word_e2_obj['word_e2_day'])

    
    word1 = the_hindu_word_list1.objects.values('word','meaning','synonym','example','word_img').filter(day=word1_day)
    word2 = the_hindu_word_list2.objects.values('word','meaning','example','word_img','synonym').filter(day=word2_day)
    if(word1.count()>0):
        hindu=1
        header1 = the_hindu_word_Header1.objects.values('Heading_for_list1','link').filter(day=word1_day)
        if(header1==None):
            header1=None
    else:
        word1=None
            
                
    if(word2.count()>0):
        hindu=2
        header2 = the_hindu_word_Header2.objects.values('Heading_for_list2','link').filter(day=word2_day)
        if(header2==None):
            header2=None

    else:
        word2=None        


    word_e1 = the_economy_word_list1.objects.values('word','meaning','example','word_img','synonym').filter(day=word_e1_day)
    word_e2 = the_economy_word_list2.objects.values('word','meaning','example','word_img','synonym').filter(day=word_e2_day)
        
    if(word_e1.count()>0):
        e=1
        header_e1 = the_economy_word_Header1.objects.values('Heading_for_list1','link').filter(day=word_e1_day)
        if(header_e1==None):
            header_e1=None
    else:
        word_e1=None        
    if(word_e2.count()>0):
        e=2
        header_e2 = the_economy_word_Header2.objects.values('Heading_for_list2','link').filter(day=word_e2_day)
            
        if(header_e2==None):
            header_e2=None
    else:
        word_e2=None

    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')

    mathh = math.objects.values().filter(home=True).all().order_by('day','creation_time')[:4]
    reasoningh = reasoning.objects.values().filter(home=True).all().order_by('day','creation_time')
    cloze = close.objects.values('question','page').filter(home=True).order_by('day','creation_time')


        
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    j = {
                        "r": "home/car.html",
                        "form": form
                    }
                    context = {
                            "form": form,
                            }
                    slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-id')[:10][::-1]
                    return HttpResponseRedirect('/')
        context = {
            "form": form,
        }
        return render(request, 'home/car.html', context)

   
    else:
        slide = current_affairs.objects.values('link','url','upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day')[:10]
        return render(request,'home/new.html',{'close':cloze,'job': jobs,'reasoning':reasoningh,'math':mathh,'word_e2_day':word_e2_day,'word_e1_day':word_e1_day,'word2_day':word2_day,'word1_day':word1_day,'word1':word1,'word_e1':word_e1,'word2':word2,'word_e2':word_e2,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2,'p':'','slide': slide,'form':userform,'login':login})


def ca(request,user_year_month,user_page_no):
    userform = UserForm(request.POST or None)
    tag_page=user_year_month
    user_year_month=user_year_month.replace('current-affairs-','')
    user_year_month=user_year_month.split('-')
    category=0
    today=0
    user_month='January'
    page_var='January_page'#just emni emni ...only for mcq category initilization
    if "category"  in user_year_month:
        category=1
        user_year=user_year_month[1]
        user_category=user_year
        user_category=user_category.replace("-","_")
        obj=total.objects.values(user_category)
        t= int(obj[0][user_category])
        print('cat'+str(t))
        #t=int(obj[0].total_current_affairs_page)
    elif "today"  in user_year_month:
        today=1
        user_year=user_year_month[1]
        obj=total.objects.all()
        t=int(obj[0].total_current_affairs_page)
        print('cat'+str(t))
        #t=int(obj[0].total_current_affairs_page)
        
    else:    
        user_month=user_year_month[0].title()
        user_year=user_year_month[1]
        month_real=user_month
        if(month_real =='January'):     
            user_date='01'
        elif(month_real == 'February'):
            user_date='02'
        elif(month_real =='March'):
            user_date='03'
        elif(month_real =='April'):
            user_date='04'
        elif(month_real =='May'):
            user_date='05'
        elif(month_real =='June'):
            user_date='06'
        elif(month_real =='July'):
            user_date='07'
        elif(month_real =='August'):
            user_date='08'
        elif(month_real =='September'):
            user_date='09'
        elif(month_real =='October'):
            user_date='10'
        elif(month_real =='November'):
            user_date='11'
        elif(month_real =='December'):
            user_date='12'   
        user_date=user_year+'-'+user_date+'-'+user_page_no
        print('dat='+user_date)
        print('year='+user_year)
        print('month='+user_month)
        page_var=user_month.title() +'_page'
        if user_year=='2018':     
            obj=current_affairs_info_2018.objects.values(page_var)
            t= int(obj[0][page_var])
            print('date wise'+ str(t))
        elif user_year=='2019':     
            obj=current_affairs_info_2019.objects.values(page_var)
            t= int(obj[0][page_var])
            print('date wise 2019'+ str(t))
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        params=int(user_page_no)
        params_int=int(params)
        mul=int(int(params))*3
        p=int(mul)-3
        obj=total.objects.all()
        next=0
        previous=0
        #t=int(obj[0].total_current_affairs_page)
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):

                print('this')
                
                                                                       
                page=[first,second,one,tow,three,four,five]
                if t==5:
                    page=[1,2,3,4,5]
                elif t==4:
                    page=[1,2,3,4]
                elif t==3:
                    page=[1,2,3]
                elif t==2:
                    page=[1,2]
                elif t==1:
                    page=[1]
                    
                    
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    
                    if(diff_from_top>=4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,last]
                    else:
                        print("access")
                        mile=0
                        page=[one,tow,three,four,five,dot,last]
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
                            
    current_affairs_2018_info = current_affairs_info_2018.objects.values('month_list',page_var,'January','February','March','April','May','June','July','August','September','October','November','December')
    #ultimate_date=(current_affairs_2018_info[0][user_month]).split('///')
    #ultimate_date=ultimate_date[int(user_page_no)]
    #ultimate_date=ultimate_date[0:2]
    #print('df'+ultimate_date)
    current_affairs_2019_info = current_affairs_info_2019.objects.values('month_list',page_var,'January','February','March','April','May','June','July','August','September','October','November','December')
    print('2019='+str(current_affairs_2019_info))
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
 
    #jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
    if today==1:
        #current_affairs_all = current_affairs.objects.values('year_now','month','question','option_1','option_2','option_3','option_4','option_5','extra').order_by('-day','-creation_time')[p:mul]
        slide = current_affairs.objects.values('year_now','month','link','url','upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
        
    elif category==1:
        slide = current_affairs.objects.values('year_now','month','link','url','upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').filter(**{user_category: True}).order_by('-day','-creation_time')[p:mul]
        #return render(request,'home/current_affairs.html',{'current_affairs_all': current_affairs_all,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':'current-affairs-category-'+user_category})
        return render(request,'home/current_descriptive.html',{'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'current_affairs_2019_info': current_affairs_2019_info,
                                                           'current_affairs_2018_info': current_affairs_2018_info,'job': jobs,'slide': slide,
                                                           'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,
                                                           'next':next,'previous':previous,'tag_page':tag_page})


    else:
        #date wise..      
        slide = current_affairs.objects.values('year_now','month','link','url','upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').filter(year_now=user_year,month=user_month,day=user_date).order_by('-day','-creation_time')
        #return render(request,'home/current_affairs.html',{'current_affairs_2019_info': current_affairs_2019_info,'current_affairs_2018_info': current_affairs_2018_info,'current_affairs_all': current_affairs_all,'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})
        return render(request,'home/current_descriptive.html',{'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'current_affairs_2019_info': current_affairs_2019_info,
                                                           'current_affairs_2018_info': current_affairs_2018_info,'job': jobs,
                                                           'slide': slide,'form':userform,'login':login,'p':diff_from_top,'page':page,
                                                           'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})
        
   
                
    return render(request,'home/current_descriptive.html',{'current_affairs_2019_info': current_affairs_2019_info,'current_affairs_2018_info': current_affairs_2018_info,
                                                       'slide': slide,'user_year':user_year,'user_month':user_month,
                                                       'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,
                                                       'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})
            
                

def signup(request):
    userform = UserForm(request.POST or None)
    if request.method == 'POST' or request.is_ajax():
        
        username=request.POST['username']
        
        email=request.POST['email']
        print(email)
        
        if User.objects.filter(username=username).exists():
            message='username already exists'
            return HttpResponse(message)
        if User.objects.filter(email=email).exists():
            message='Email already exists'
            return HttpResponse(message)
            
        form = UserForm(request.POST)
        if form.is_valid():
           
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.is_active = False
            user.set_password(password)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your  account.'
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            toemail = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[toemail])
            email.send()
            
               
            context = {
            "form": form,
            }
            message='true'
            return HttpResponse(message)
        else:
            message='Please Insert a valid Input'
            return HttpResponse(message)
            
        return render(request, 'home/signup.html', context)

   
    else:
        return render(request,'home/signup.html',{'form':userform})       
       
def login(request):
    log_in = Login(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        
       username=request.POST['username']
        
       password=request.POST['password']
       p=User.objects.filter(username=username)
       
       if User.objects.filter(username=username).exists():
           
          user = authenticate(username=username, password=password)
          
             
          if user is not None:
             if user.is_active:
                auth_login(request,user)
                return HttpResponse('true')
             else:
                 message='Contact us'
                 return HttpResponse(message)
          else:
                 message='wrong password'
                 return HttpResponse(message)      
       else:
            message='Email does not exists'
            return HttpResponse(message)

    

   
    else:
        return render(request,'home/signup.html',{'login':log_in})       
  




def add(request):
    log_in = Login(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        
       new_id=request.POST['link']
        
       username=request.POST['user_name']
       img_url=request.POST['im_url']
       h=request.POST['head']
       usr_check = user_save.objects.filter(user_id=username,headline=h).all()

       if  not usr_check.exists():
           u=user_save(user_id=username,headline=h,img_link=img_url,link_id=new_id)
           u.save()
          
           message='success'
           return HttpResponse(message)
       
           '''file_path = './user/'+username+'/'
           directory = os.path.dirname(file_path)
           try:
                if os.path.isdir (directory):
                   file_path = './user/'+username+'/'+new_id
                   open(file_path, 'w').close()
                   message='success'
                   return HttpResponse(message)
                else:
                    file_path = './user/'+username+'/'
                    directory = os.path.dirname(file_path)
                    os.makedirs((directory))
                    file_path = './user/'+username+'/'+new_id+'.txt'
                    directory = os.path.dirname(file_path)
                    os.makedirs((directory))
                    message='success'
                    return HttpResponse(message)

                               
           except:
               message='Retry or re login'
               return HttpResponse(new_id)'''
           
       else:
           message='Already Added'
           return HttpResponse(message)
           

    

   
    else:
        return render(request,'home/signup.html',{'login':login})


def del_ca(request):
    log_in = Login(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        
       ca_id=request.POST['link']
        
       username=request.POST['user']
       
       usr_check = user_save.objects.filter(user_id=username,link_id=ca_id).all()
       print(usr_check)
       if  usr_check.exists():
           instance = user_save.objects.get(user_id=username,link_id=ca_id)
           instance.delete()

           '''u=user_save(user_id=username,headline=h,img_link=img_url,link_id=new_id)
           u.save()
           print(u)'''
           message='success'
           return HttpResponse(message)
       
           '''file_path = './user/'+username+'/'
           directory = os.path.dirname(file_path)
           try:
                if os.path.isdir (directory):
                   file_path = './user/'+username+'/'+new_id
                   open(file_path, 'w').close()
                   message='success'
                   return HttpResponse(message)
                else:
                    file_path = './user/'+username+'/'
                    directory = os.path.dirname(file_path)
                    os.makedirs((directory))
                    file_path = './user/'+username+'/'+new_id+'.txt'
                    directory = os.path.dirname(file_path)
                    os.makedirs((directory))
                    message='success'
                    return HttpResponse(message)

                               
           except:
               message='Retry or re login'
               return HttpResponse(new_id)'''
           
       else:
           message='Already Deleted'
           return HttpResponse(message)
           

    

   
    else:
        return render(request,'home/signup.html',{'login':login})




def dashboard(request,string):
    userform = UserForm(request.POST or None)
    log_in = Login(request.POST or None)
    if request.method == 'POST' or request.is_ajax():
        
       
        
       
       return render(request,'home/dashboard.html',{'login': login,'login':log_in})

       
       '''file_path = './user/'+username+'/'
       directory = os.path.dirname(file_path)
       try:
            if os.path.isdir (directory):
               array=[]
               list =os.listdir(file_path)
               for files in list:
                   array.append(files)
                   message='success'
               return HttpResponse (json.dumps(array[::-1]), content_type="application/json")
            else:
                
                message='no'
                return HttpResponse(message)

                           
       except:
               message='Retry or re login'
               return HttpResponse(message)'''
                           

    

   
    else:
        username=request.POST.get(string)
        usr = user_save.objects.filter(user_id=string).values('headline','date_added','img_link','link_id').all().order_by('-id')
        
        
        return render(request,'home/dashboard.html',{'usr':usr,'login':log_in})
  

def url_redirect(request,params):

    mul=params*3
    p=mul-2

    slide = current_affairs.objects.values_list('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-id')[:10][::-1]
    return render(request,'home/current_home.html',{'slide': slide})
    
    
    
def current(request,params,string):
    userform = UserForm(request.POST or None)
    page=['2','3']
    field_name = string
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        params_int=int(params)
        mul=int(int(params))*3
        p=int(mul)-3
        field_name=string
        obj=total.objects.values(field_name)
    
        t= int(obj[0][field_name])
        
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
                
                
                


    slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').filter(**{field_name: True}).order_by('-day','-creation_time')[p:mul]
    return render(request,'home/ca.html',{'job': jobs,'slide': slide,'form':userform,'login':login,'p':t,'page':page,'params':params_int,'next':next,'previous':previous})





def cuttent_affirs_single(request,string):
    userform = UserForm(request.POST or None)
    page=['2','3']
    field_name = string
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        id=string
        
       
                        
                
                
                
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')


    slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').filter(new_id=id)
    return render(request,'home/ca.html',{'job': jobs,'slide': slide,'form':userform,'login':login,'p':12})    
    

    
       

def word(request,string,no):
    userform = UserForm(request.POST or None)
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        obj=total_english.objects.values('total_page')[0]
        next=0
        previous=0
        t=int(obj['total_page'])
        today=time.strftime("%Y-%m-%d")
        if(string=='page'):
            if(int(no)<=t):
                day = the_hindu_word_list1.objects.values('day').distinct().order_by('-day')[:int(no)]
                string = day[int(no)-1]['day']
                s='2017-06-09'
                params=no
                params_int=int(params)
        else:
            day = the_hindu_word_list1.objects.values('day').distinct().filter(day__range=(string,today)).count()
            params=int(day)
            params_int=int(params)
            
            
        
        mul=int(int(params))*3
        p=int(mul)-3
        obj=total_english.objects.values('total_page')[0]
        next=0
        previous=0
        t=int(obj['total_page'])
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
        
            
        

        
            
        hindu=0
        e=0
        header1=None
        header2=None
        header_e1=None
        header_e2=None
        list_day = the_hindu_word_list1.objects.values('day').distinct()[0:30]
        
        word1 = the_hindu_word_list1.objects.values('word','meaning','synonym','example','word_img').filter(day=string)
        word2 = the_hindu_word_list2.objects.values('word','meaning','example','word_img','synonym').filter(day=string)
        if(word1.count()>0):
            hindu=1
            header1 = the_hindu_word_Header1.objects.values('Heading_for_list1').filter(day=string)
            if(header1==None):
                header1=None
        else:
            word1=None
            
                
        if(word2.count()>0):
            hindu=2
            header2 = the_hindu_word_Header2.objects.values('Heading_for_list2').filter(day=string)
            if(header2==None):
                header2=None

        else:
            word2=None        


        word_e1 = the_economy_word_list1.objects.values('word','meaning','example','word_img','synonym').filter(day=string)
        word_e2 = the_economy_word_list2.objects.values('word','meaning','example','word_img','synonym').filter(day=string)
        
        if(word_e1.count()>0):
            e=1
            header_e1 = the_economy_word_Header1.objects.values('Heading_for_list1').filter(day=string)
            if(header_e1==None):
                header_e1=None
        else:
            word_e1=None        
        if(word_e2.count()>0):
            e=2
            header_e2 = the_economy_word_Header2.objects.values('Heading_for_list2').filter(day=string)
            
            if(header_e2==None):
                header_e2=None
        else:
            word_e2=None         


        ''' if(hindu==1 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==1 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==0 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==0 and e==2):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':word_e2,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})'''
    
            
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
    return render(request,'home/english.html',{'job': jobs,'form':userform,'login':login,'params':params_int,'p':day,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':word2,'word_e2':word_e2,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2,'list_day':list_day})




def math_all(request,string,params):
    userform = UserForm(request.POST or None)
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        if (string=='profit-and-loss'):
            string=string.replace('profit-and-loss', 'profit_n_loss', 1)

        elif(string=='squre-and-cube'):
            string=string.replace('squre-and-cube', 'squre_n_cube', 1)

        elif(string=='ratio-and-proportion'):
            string=string.replace('ratio-and-proportion', 'ratio_n_proportion', 1)
        elif(string=='time-and-work'):
            string=string.replace('time-and-work', 'time_n_work', 1)

        elif(string=='time-and-distance'):
            string=string.replace('time-and-distance', 'time_n_distance', 1)

        elif(string=='boats-and-stream'):
            string=string.replace('boats-and-stream', 'boats_n_stream', 1)

        elif(string=='alligation-and-mixture'):
            string=string.replace('alligation-and-mixture', 'alligation_n_mixture', 1)

        elif(string=='volume-and-surface-area'):
            string=string.replace('volume-and-surface-area', 'volume_n_surface_area', 1)

        else:
            string=string.replace('-', '_')
            
        
        params_int=int(params)
        mul=int(int(params))*5
        p=int(mul)-5
        field_name=string
        field_page='total_'+string+'_page'
        t=1
        if(string=='profit_n_loss'):
            obj=total_math.objects.values(field_page)
    
            t= int(obj[0][field_page])
        
        obj=total_math.objects.values(field_page)
        t= int(obj[0][field_page])
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        
        today=time.strftime("%Y-%m-%d")
        
        
        params_int=int(params)
        
        mul=int(int(params))*5
        p=int(mul)-5
        
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):

                print('this')
                
                                                                       
                page=[first,second,one,tow,three,four,five]
                if t==5:
                    page=[1,2,3,4,5]
                elif t==4:
                    page=[1,2,3,4]
                elif t==3:
                    page=[1,2,3]
                elif t==2:
                    page=[1,2]
                elif t==1:
                    page=[1]
                    
                    
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    
                    if(diff_from_top>=4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,last]
                    else:
                        print("access")
                        mile=0
                        page=[one,tow,three,four,five,dot,last]
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]        

        
            
       

        ''' if(hindu==1 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==1 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==0 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==0 and e==2):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':word_e2,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})'''
        
    
            
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
    mathh = math.objects.values().filter(chapter=string).all().order_by('day')[p:mul]

    return render(request,'home/math.html',{'job': jobs,'form':userform,'login':login,'params':params_int,'p':2,'page':page,'params':params,'next':next,'previous':previous,'math':mathh,'chapter':string.replace('_',' '),'tag_page':string})



    
def job_view(request,params,after_string,string):
    userform = UserForm(request.POST or None)
    page=['2','3']
    field_name = string
    login = Login(request.POST or None)

    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        params_int=int(params)
        mul=int(int(params))*10
        p=int(mul)-10
        if(string=='home'):
            field_name='total_other_page'
            obj=total_job.objects.values(field_name)
            t= int(obj[0][field_name])
        elif(string=='state'):    
            field_name='total_'+after_string+'_page'
            obj=total_job_state.objects.values(field_name)
            t= int(obj[0][field_name])

        elif(string=='qualification'):    
            field_name='total_'+after_string+'_page'
            obj=total_job_category.objects.values(field_name)
            t= int(obj[0][field_name])

        elif(string=='all'):    
            field_name='total_'+after_string+'_page'
            obj=total_job_category.objects.values(field_name)
            t= int(obj[0][field_name])

        elif(string=='goto'):    
            t=0     
        elif(string=='category'):    
            field_name='total_'+after_string+'_page'
            obj=total_job.objects.values(field_name)
            t= int(obj[0][field_name])     
        
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
                
                
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
        top_list = job.objects.values('heading','new_id','first_day','last_day','ca_img','apply_link','detail_link').filter(top=True).order_by('-day','-creation_time')[:8]
        
        if(string=='home'):
      
        
            enddate = date.today() + timedelta(days=5)
            bank = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='bank',last_day__lte=enddate).order_by('-day','-creation_time')
            ssc = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='ssc',last_day__lte=enddate).order_by('-day','-creation_time')
            upsc = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='upsc',last_day__lte=enddate).order_by('-day','-creation_time')
            rail = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='rail',last_day__lte=enddate).order_by('-day','-creation_time')
            defence = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='defence',last_day__lte=enddate).order_by('-day','-creation_time')
            other = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category='other',last_day__lte=enddate).order_by('-day','-creation_time')[:3]
            
            return render(request,'home/job.html',{'string':'category','after_string':'other','top_list':top_list,'bank': bank,'ssc': ssc,'upsc': upsc,'rail': rail,'defence': defence,'other': other,'form':userform,'login':login,'p':bank,'page':page,'params':params_int,'next':next,'previous':previous})

        elif(string=='category'):
            enddate = date.today() + timedelta(days=5)
            field_name=after_string
            if(field_name=='bank'):
                flag=1
                bank = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'bank': bank,'form':userform,'login':login,'p':bank,'page':page,'params':params_int,'next':next,'previous':previous})

            elif(field_name=='ssc'):
                flag=2;
                ssc = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'ssc': ssc,'form':userform,'login':login,'p':ssc,'page':page,'params':params_int,'next':next,'previous':previous})

            elif(field_name=='upsc'):
                flag=3;
                upsc = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'upsc': upsc,'form':userform,'login':login,'p':upsc,'page':page,'params':params_int,'next':next,'previous':previous})
    
            elif(field_name=='rail'):
                flag=4;
                rail = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'rail': rail,'form':userform,'login':login,'p':rail,'page':page,'params':params_int,'next':next,'previous':previous})

            elif(field_name=='defence'):
                flag=5;
                defence = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'defence': defence,'form':userform,'login':login,'p':defence,'page':page,'params':params_int,'next':next,'previous':previous})

            elif(field_name=='other'):
                flag=6;
                other = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]

                return render(request,'home/job.html',{'string':string,'after_string':field_name,'top_list':top_list,'other': other,'form':userform,'login':login,'p':other,'page':page,'params':params_int,'next':next,'previous':previous})

            
            
            #jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(category=field_name).order_by('-day','-creation_time')[p:mul]
        
            #return render(request,'home/job.html',{'flag':flag,'top_list':top_list,'job': jobs,'form':userform,'login':login,'p':jobs,'page':page,'params':params_int,'next':next,'previous':previous})




        elif(string=='state'):
           
            field_name=after_string
            enddate = date.today() + timedelta(days=5)
            
            jobs = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(state=field_name).order_by('-day','-creation_time')[p:mul]
            return render(request,'home/job.html',{'string':string,'after_string':field_name.replace("_", " ").title(),'top_list':top_list,'job': jobs,'form':userform,'login':login,'p':jobs,'page':page,'params':params_int,'next':next,'previous':previous})

        elif(string=='qualification'):
           
            field_name=after_string
            enddate = date.today() + timedelta(days=5)
            
            jobs = job.objects.values('apply_link','detail_link','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(**{field_name: True}).order_by('-day','-creation_time')[p:mul]
            return render(request,'home/job.html',{'string':string,'after_string':field_name.replace("_", " ").title(),'top_list':top_list,'job': jobs,'form':userform,'login':login,'p':jobs,'page':page,'params':params_int,'next':next,'previous':previous})
        
    
        elif(string=='goto'):
           
            field_name=after_string
            
            
            jobs = job.objects.values('apply_link','detail_link','category','extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(new_id=field_name)
            t1= (jobs[0]['category'])
            related = job.objects.values('ca_img','heading','new_id',).filter(category=t1).exclude(new_id=field_name).order_by('-day','-creation_time')[:5]
            
            return render(request,'home/job.html',{'job': jobs,'related':related,'string':string,'after_string':field_name.replace("_", " ").replace("===", ", posted on: ").title(),'top_list':top_list,'job': jobs,'form':userform,'login':login,'p':related,'page':page,'params':params_int,'next':next,'previous':previous})
                
    
        

        


    #return render(request,'home/job.html',{'slide': slide,'form':userform,'login':login,'p':bank,'page':page,'params':params_int,'next':next,'previous':previous})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        # return redirect('home')
        return render(request,'home/thanks.html')
        
        #return HttpResponse('<h2 style="color:blue">Thank you for your email confirmation. Now you can login your account.</h2>')
    else:
        return HttpResponse('<h1>Activation link is invalid!</h1>')











def reasoning_all(request,string,params):
    userform = UserForm(request.POST or None)
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        
        params_int=int(params)
        mul=int(int(params))*5
        p=int(mul)-5
        field_name=string
        field_page='total_'+string+'_page'
        
        obj=total_reasoning.objects.values(field_page)
    
        t= int(obj[0][field_page])
        
        
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        
        today=time.strftime("%Y-%m-%d")
        
        
        params_int=int(params)
        
        mul=int(int(params))*5
        p=int(mul)-5
        
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
        
            
        

        
            
       


        
    
            
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
    reasoningh = reasoning.objects.values().filter(chapter=string).all().order_by('day','creation_time')[p:mul]

    return render(request,'home/reasoning.html',{'job': jobs,'form':userform,'login':login,'params':params_int,'p':2,'page':page,'params':params,'next':next,'previous':previous,'reasoning':reasoningh})






def reasoning_single(request,string):
    userform = UserForm(request.POST or None)
    page=['2','3']
    field_name = string
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        id=string
        
       
                        
                
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
                
                


    slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').filter(new_id=id)
    reasoningh = reasoning.objects.values().filter(new_id=id).all()
    
    return render(request,'home/reasoning_single.html',{'job': jobs,'reasoning':reasoningh,'form':userform,'login':login,'p':12})


def close_all(request,string,params):
    userform = UserForm(request.POST or None)
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        
        params_int=int(params)
        mul=int(int(params))*5
        p=int(mul)-5
        field_name=string
        field_page='total_'+string+'_page'
        
        obj=total_close.objects.values(field_page)
    
        t= int(obj[0][field_page])
        
        
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        
        today=time.strftime("%Y-%m-%d")
        
        
        params_int=int(params)
        
        mul=int(int(params))*1
        p=int(mul)-1
        
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
        
            
        

        
            
       


        
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
    
            
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
    closee = close.objects.all().order_by('day','creation_time')[p:mul]

    return render(request,'home/close.html',{'job': jobs,'form':userform,'login':login,'params':params_int,'p':2,'page':page,'params':params,'next':next,'previous':previous,'close':closee})



def error_all(request,string,params):
    userform = UserForm(request.POST or None)
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        
        params_int=int(params)
        mul=int(int(params))*5
        p=int(mul)-5
        field_name=string
        field_page='total_'+string+'_page'
        
        obj=total_error.objects.values(field_page)
    
        t= int(obj[0][field_page])
        
        
        next=0
        previous=0
        #t=105
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        
        today=time.strftime("%Y-%m-%d")
        
        
        params_int=int(params)
        
        mul=int(int(params))*5
        p=int(mul)-5
        
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1
        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):
                                                                       
                page=[first,second,one,tow,three,four,five]
                
            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]
               
               
               
                elif(mile==1):
                    mile1=(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
                
            
                    

          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):
                    if(diff_from_top>4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,dot,last]       
                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]
                    
                    

                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):
                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]
               
               
               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]

                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]



            elif(diff_from_bottom<10):
                if(diff_from_top>10):
                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5
                            
                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]
                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]
               
               
               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]
                       
                   
                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
        
            
        

        
            
       

        ''' if(hindu==1 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==1 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==0):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':None,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==2 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':word1,'word_e1':word_e1,'word2':word2,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})
        elif(hindu==0 and e==1):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':None,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})

        elif(hindu==0 and e==2):
             return render(request,'home/english.html',{'form':userform,'login':login,'p':header1,'page':page,'params':word1,'next':next,'previous':previous,'word1':None,'word_e1':word_e1,'word2':None,'word_e2':word_e2,'header1':header1,'header2':header2,'header_e1':header_e1,'header_e2':header_e2})'''
        
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
    
            
                


    #slide = current_affairs.objects.values('upper_heading','yellow_heading','key_1','key_2','key_3','day','new_id','paragraph','all_key_points','ca_img').order_by('-day','-creation_time')[p:mul]
    errorr = error.objects.values().filter(chapter=string).all().order_by('day','creation_time')[p:mul]

    return render(request,'home/error.html',{'job': jobs,'form':userform,'login':login,'params':params_int,'p':2,'page':page,'params':params,'next':next,'previous':previous,'error':errorr})







def formula(request,string):
    userform = UserForm(request.POST or None)
    
    field_name = string
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')

    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
        if (field_name == "profit-and-loss"):
            return render(request,'math/profit-and-loss.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "squre-and-cube"):
            return render(request,'math/squre-and-cube.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "simplification"):
            return render(request,'math/simplification.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "average"):
            return render(request,'math/average.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "percentage"):
            return render(request,'math/percentage.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "problem-on-age"):
            return render(request,'math/problem-on-age.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "ratio-and-proportion"):
            return render(request,'math/ratio-and-proportion.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "partnership"):
            return render(request,'math/partnership.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "time-and-work"):
            return render(request,'math/time-and-work.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "pipe-cistern"):
            return render(request,'math/pipe-cistern.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "time-and-distance"):
            return render(request,'math/time-and-distance.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "boats-and-stream"):
            return render(request,'math/boats-and-stream.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "alligation-and-mixture"):
            return render(request,'math/alligation-and-mixture.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "simple-interest"):
            return render(request,'math/simple-interest.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "compound-interest"):
            return render(request,'math/compound-interest.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "volume-and-surface-area"):
            return render(request,'math/volume-and-surface-area.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "probability"):
            return render(request,'math/probability.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "permutation-combination"):
            return render(request,'math/permutation-combination.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "bar-graph"):
            return render(request,'math/bar-graph.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "pie-charts"):
            return render(request,'math/pie-charts.html',{'job': jobs,'form':userform,'login':login,})
        elif (field_name == "line-graph"):
            return render(request,'math/line-graph.html',{'job': jobs,'form':userform,'login':login,})



     
   
    

    
        
        

    
    return render(request,'home/reasoning_single.html',{'job': jobs,'form':userform,'login':login,})

def gk(request,subject,folder,html,no):
    userform = UserForm(request.POST or None)
    
    
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')

    login = Login(request.POST or None)
    address = subject +'/'+ folder +'/'+html+'/'+html +'-'+ str(no)+'.html'
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
       return render(request,address,{'job': jobs,'form':userform,'login':login,})

     
   
    

    
        
        

    
    return render(request,'home/reasoning_single.html',{'job': jobs,'form':userform,'login':login,})



def gk_index(request,subject):
    userform = UserForm(request.POST or None)
    
    
    jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')

    login = Login(request.POST or None)
    address = subject +'/'+subject+'.html'
    if request.method == 'POST' and request.is_ajax():
        pass
   
    else:
       return render(request,address,{'job': jobs,'form':userform,'login':login,})

     
   
    

    
        
        

    
    return render(request,'home/reasoning_single.html',{'job': jobs,'form':userform,'login':login,})


def mcq_current(request,user_year_month,user_page_no):
    userform = UserForm(request.POST or None)
    tag_page=user_year_month
    user_year_month=user_year_month.replace('current-affairs-','')
    user_year_month=user_year_month.split('-')
    category=0
    user_month='January'
    page_var='January_page'#just emni emni ...only for mcq category initilization
    if "category"  in user_year_month:
        category=1
        user_year=user_year_month[1]
        user_category=user_year
        user_category=user_category.replace("-","_")
        obj=total_mcq.objects.values(user_category)
        t= int(obj[0][user_category])
        print('cat'+str(t))
        #t=int(obj[0].total_current_affairs_page)
        
    else:    
        user_month=user_year_month[0].title()
        user_year=user_year_month[1]
        month_real=user_month
        if(month_real =='January'):     
            user_date='01'
        elif(month_real == 'February'):
            user_date='02'
        elif(month_real =='March'):
            user_date='03'
        elif(month_real =='April'):
            user_date='04'
        elif(month_real =='May'):
            user_date='05'
        elif(month_real =='June'):
            user_date='06'
        elif(month_real =='July'):
            user_date='07'
        elif(month_real =='August'):
            user_date='08'
        elif(month_real =='September'):
            user_date='09'
        elif(month_real =='October'):
            user_date='10'
        elif(month_real =='November'):
            user_date='11'
        elif(month_real =='December'):
            user_date='12'   
        user_date=user_year+'-'+user_date+'-'+user_page_no
        print('dat='+user_date)
        print('year='+user_year)
        print('month='+user_month)
        page_var=user_month.title() +'_page'
        if user_year=='2018':     
            obj=mcq_info_2018.objects.values(page_var)
            t= int(obj[0][page_var])
            print('date wise'+ str(t))
        elif user_year=='2019':     
            obj=mcq_info_2019.objects.values(page_var)
            t= int(obj[0][page_var])
            print('date wise 2019'+ str(t))
    
    page=['2','3']
    login = Login(request.POST or None)
    #name = NameForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass   
    else:        
        params=int(user_page_no)
        params_int=int(params)
        mul=int(int(params))*3        
        p=int(mul)-3        
        next=0
        previous=0
        print('tttttttt'+str(t))
        #t=5
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):                                                                       
                page=[first,second,one,tow,three,four,five]
                if t==5:
                    page=[1,2,3,4,5]
                elif t==4:
                    page=[1,2,3,4]
                elif t==3:
                    page=[1,2,3]
                elif t==2:
                    page=[1,2]
                elif t==1:
                    page=[1]            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]               
                elif(mile==1):
                    mile1=int(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):                    
                    if(diff_from_top>=4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,last]
                    else:
                        print("access")
                        mile=0
                        page=[one,tow,three,four,five,dot,last]                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]

            elif(diff_from_bottom<10):
                if(diff_from_top>10):                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]
                    
                        
    mcq_2018_info = mcq_info_2018.objects.values('month_list',page_var,'January','February','March','April','May','June','July','August','September','October','November','December')
    #ultimate_date=(mcq_2018_info[0][user_month]).split('///')
    #ultimate_date=ultimate_date[int(user_page_no)]
    #ultimate_date=ultimate_date[0:2]
    #print('df'+ultimate_date)
    mcq_2019_info = mcq_info_2019.objects.values('month_list',page_var,'January','February','March','April','May','June','July','August','September','October','November','December')
     
    #jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
    if user_year=='latest':
        mcq_all = mcq.objects.values('ans','year_now','month','question','option_1','option_2','option_3','option_4','option_5','extra').order_by('-day','-creation_time')[p:mul]
        
    elif category==1:
        mcq_all = mcq.objects.values('ans','year_now','month','question','option_1','option_2','option_3','option_4','option_5','extra').filter(**{user_category: True}).order_by('-day','-creation_time')[p:mul]
        return render(request,'home/mcq.html',{'mcq_2019_info': mcq_2019_info,'mcq_2018_info': mcq_2018_info,'mcq_all': mcq_all,'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':'current-affairs-category-'+user_category})


    else:
               
        mcq_all = mcq.objects.values('ans','year_now','month','question','option_1','option_2','option_3','option_4','option_5','extra').filter(year_now=user_year,month=user_month,day=user_date).order_by('-day','-creation_time')
        return render(request,'home/mcq.html',{'mcq_2019_info': mcq_2019_info,'mcq_2018_info': mcq_2018_info,'mcq_all': mcq_all,'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})
        
   
                
    return render(request,'home/mcq.html',{'mcq_2019_info': mcq_2019_info,'mcq_2018_info': mcq_2018_info,'mcq_all': mcq_all,'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})


#.............................subject.......................


def subject(request,subject,topic,subtopic,chapter,user_page_no):
    userform = UserForm(request.POST or None)
    
    
    category=0
    user_month='January'
    page_var='January_page'#just emni emni ...only for mcq category initilization
    if "_"  in subtopic:
        category=1
        subtopic2=subtopic.split('_')[1]
        subtopic=subtopic.split('_')[0]
        user_category=user_year
        user_category=user_category.replace("-","_")
    else:
        subtopic2='None'
        
        #print('cat'+str(t))
        #t=int(obj[0].total_current_affairs_page)
    if subject=='history':
        obj=total_history.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='geography':
        obj=total_geography.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='polity':
        obj=total_polity.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='economics':
        obj=total_economics.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='physics':
        obj=total_physics.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='biology':
        obj=total_biology.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])
    if subject=='chemistry':
        obj=total_chemistry.objects.values('chapter_'+chapter)
        t= int(obj[0]['chapter_'+chapter])

    
    page=['2','3']
    login = Login(request.POST or None)
    if request.method == 'POST' and request.is_ajax():
        pass   
    else:        
        params=int(user_page_no)
        params_int=int(params)
        mul=int(int(params))*3        
        p=int(mul)-3        
        next=0
        previous=0
        print('tttttttt'+str(t))
        #t=5
        if(t>params_int):
            next=params_int+1
        if(params_int>1):
            previous=params_int-1        
        left=int(int(params)-2)
        right=int(int(params)+2)
        diff_from_top=int(t-right)
        diff_from_bottom=int(left-1)
        if(((t-params_int)<= 4) or (params_int<=5)):
          if(((t-params_int)<= 4)):
            one=t-4
            tow=t-3
            three=t-2
            four=t-1
            five=t
            first=1
            second='...'
            dot='...'
            if(diff_from_bottom<10):                                                                       
                page=[first,second,one,tow,three,four,five]
                if t==5:
                    page=[1,2,3,4,5]
                elif t==4:
                    page=[1,2,3,4]
                elif t==3:
                    page=[1,2,3]
                elif t==2:
                    page=[1,2]
                elif t==1:
                    page=[1]            
            else:
                mile=int(diff_from_bottom/10)
                if(mile>=2):
                   mile1=int(mile)*10
                   mile2=mile1-10
                   page=[first,second,mile2,mile1,dot,one,tow,three,four,five]               
                elif(mile==1):
                    mile1=int(t/10)*10
                    page=[first,dot,mile1,dot,one,tow,three,four,five]
          else:
                one=1
                tow=2
                three=3
                four=4
                five=5
                
                last=t
                dot='...'
                if(diff_from_top<10):                    
                    if(diff_from_top>=4):
                       es_mile=int((params_int/10)+10)
                       if (es_mile<t):
                           mile=es_mile
                           page=[one,tow,three,four,five,dot,mile,dot,last]
                       else:
                           mile=0
                           page=[one,tow,three,four,five,dot,last]
                    else:
                        print("access")
                        mile=0
                        page=[one,tow,three,four,five,dot,last]                
                else:
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                       mile1=int((params_int/10))*10+10
                       mile2=mile1+10
                       page=[one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[one,tow,three,four,five,dot,mile1,dot,last]                    
        else:
            first=1
            dot='...'
            one=params_int-2
            tow=params_int-1
            three=params_int
            four=params_int+1
            five=params_int+2
            last=t
            if(diff_from_top<10):
                if(diff_from_bottom>10):                    
                    mile=int(diff_from_bottom/10)
                    if(mile>=2):
                       mile1=int(mile)*10
                       mile2=mile1-10
                       page=[first,dot,mile2,mile1,dot,one,tow,three,four,five,dot,last]               
                    elif(mile==1):
                        mile1=(t/10)*10
                        page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]

            elif(diff_from_bottom<10):
                if(diff_from_top>10):                    
                    mile=int(diff_from_top/10)
                    if(mile>=2):
                        
                        mile1=(int(right/10))*10+10
                        mile2=int(mile1)+10
                        if(right==mile1):
                            mile1=mile1+5                        
                        page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                    elif(mile==1):
                        mile1=(params_int/10)+10
                        page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                else:
                    page=[first,dot,one,tow,three,four,five,dot,last]                    
            else:
                sign_bottom=0
                sign_top=0
                mile_bottom=int(diff_from_bottom/10)
                if(mile_bottom>=2):
                    mile1_bottom=int(mile_bottom)*10
                    mile2_bottom=mile1_bottom-10
                    sign_bottom=1
                    #page=[first,dot,mile1,mile2,dot,one,tow,three,four,five,dot,last]               
                elif(mile_bottom==1):
                    mile1_bottom=(mile_bottom)*10
                    #page=[first,dot,mile1,dot,one,tow,three,four,five,last]
                    
                mile_top=int(diff_from_top/10)
                if(mile_top>=2):
                    mile1_top=(int(right/10))*10+10
                    mile2_top=int(mile1_top)+10
                    sign_top=1
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,mile2,dot,last]                   
                elif(mile_top==1):
                    mile1_top=(int(right/10))*10+10
                    #page=[first,dot,one,tow,three,four,five,dot,mile1,dot,last]
                    
                if(sign_bottom==1 and sign_top==1):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                elif(sign_bottom==0 and sign_top==1):
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,mile2_top,dot,last]
                    
                elif(sign_bottom==1 and sign_top==0):
                    page=[first,dot,mile2_bottom,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

                else:
                    page=[first,dot,mile1_bottom,dot,one,tow,three,four,five,dot,mile1_top,dot,last]

    
     
    #jobs = job.objects.values('extra_day','first_day','last_day','heading','eligibility','age','amount','day','new_id','des','ca_img').filter(home=True).order_by('-day','-creation_time')
    if subject=='history':
        mcq_all = history.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_history.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_history') or (key=='total_history_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/history.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})
            
        
    elif subject=='polity':
        mcq_all = polity.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_polity.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_polity') or (key=='total_polity_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/polity.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})
    elif subject=='economics':
        mcq_all = economics.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_economics.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_economics') or (key=='total_economics_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/economics.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})

    elif subject=='geography':
        mcq_all = geography.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_geography.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_geography') or (key=='total_geography_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/geography.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})

    elif subject=='physics':
        mcq_all = physics.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_physics.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_physics') or (key=='total_physics_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/physics.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})

    elif subject=='chemisry':
        mcq_all = chemisry.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_chemisry.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_chemisry') or (key=='total_chemisry_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/chemisry.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})

    elif subject=='biology':
        mcq_all = biology.objects.values('ans','topic','subtopic','subtopic_2','year_exam','question','option_1','option_2','option_3','option_4','option_5','extra').filter(chapter=chapter).order_by('-day','-creation_time')[p:mul]
        a=total_biology.objects.values()
        chapter_list=[]
        for key, value in a[0].items():
            if (key == 'total_biology') or (key=='total_biology_page')or (key=='id'):
                pass
            else:
                if value >=1:
                    chapter_list.append(key)
        print(chapter_list)
           
        return render(request,'home/biology.html',{'chapter':chapter,'chapter_list':chapter_list,'mcq_all': mcq_all,'subject':subject,'topic':topic,'subtopic':subtopic,'subtopic2':subtopic2,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':chapter})


        
   
                
    return render(request,'home/mcq.html',{'mcq_2019_info': mcq_2019_info,'mcq_2018_info': mcq_2018_info,'mcq_all': mcq_all,'user_year':user_year,'user_month':user_month,'user_day':user_page_no,'form':userform,'login':login,'p':diff_from_top,'page':page,'params':params_int,'next':next,'previous':previous,'tag_page':tag_page})


