from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views

from django.views.decorators.csrf import csrf_exempt

from django.urls import path, re_path

app_name = 'bank'

urlpatterns = [
    
    re_path(r'^$',(views.index),name='index'),
    
    re_path(r'^logout/$', auth_views.LogoutView, {'next_page': '/'}, name='logout'),
    re_path(r'^signup/$',views.signup,name='signup'),
    
    re_path(r'^login/$',views.login,name='login'),
    re_path(r'^add/$',views.add,name='add'),
    re_path(r'^del/$',views.del_ca,name='del_ca'),

    re_path(r'^dashboard/(?P<string>.+)/$',views.dashboard,name='dashboard'),
    re_path(r'^current-affairs/detail/(?P<user_year_month>.+)/(?P<user_page_no>[0-9]+)/$',views.ca,name='ca'),
    re_path(r'^current/(?P<string>.+)/(?P<params>[0-9]+)/$',views.current,name='current'),
    re_path(r'^cuttent_affirs/(?P<string>.+)/$',views.cuttent_affirs_single,name='cuttent_affirs'),
    re_path(r'^english/word/(?P<string>.+)/(?P<no>[0-9]+)/$',views.word,name='word'),
    re_path(r'^math/(?P<string>.+)/(?P<params>[0-9]+)/$',views.math_all,name='math'),
    re_path(r'^job/(?P<string>.+)/(?P<after_string>.+)/(?P<params>[0-9]+)/$',views.job_view,name='job'),
    re_path(r'^reasoning/(?P<string>.+)/(?P<params>[0-9]+)/$',views.reasoning_all,name='reasoning'),
    re_path(r'^reasoning/(?P<string>.+)/$',views.reasoning_single,name='reasoning_single'),
    re_path(r'^closetest/(?P<string>.+)/(?P<params>[0-9]+)/$',views.close_all,name='close'),
     re_path(r'^error_correction/(?P<string>.+)/(?P<params>[0-9]+)/$',views.error_all,name='error'),


     re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    re_path(r'^formula/(?P<string>.+)/$',views.formula,name='formula'),
    
    re_path(r'^gktoday/(?P<subject>.+)/(?P<folder>.+)/(?P<html>.+)/(?P<no>[0-9]+)/$',views.gk,name='gk'),
    re_path(r'^gk/(?P<subject>.+)/$',views.gk_index,name='gk_index'),
    
    re_path(r'^current-affairs/mcq/(?P<user_year_month>.+)/(?P<user_page_no>[0-9]+)/$',views.mcq_current,name='mcq_current'),
    re_path(r'^subject/(?P<subject>.+)/(?P<topic>.+)/(?P<subtopic>.+)/(?P<chapter>.+)/(?P<user_page_no>[0-9]+)/$',views.subject,name='history'),
    re_path(r'^database/$',views.database,name='database'),
    
    
    
]
